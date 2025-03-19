import dataclasses
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from typing_extensions import Self

from classiq.interface.enum_utils import StrEnum
from classiq.interface.exceptions import (
    ClassiqExpansionError,
    ClassiqInternalExpansionError,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.classical_type import ClassicalType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.classical_parameter_declaration import (
    ClassicalParameterDeclaration,
)
from classiq.interface.model.handle_binding import (
    HandleBinding,
    NestedHandleBinding,
    SlicedHandleBinding,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import ArgValue
from classiq.interface.model.quantum_function_declaration import PositionalArg
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumType
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.model_expansions.capturing.mangling_utils import (
    demangle_handle,
    mangle_captured_var_name,
)
from classiq.model_expansions.transformers.model_renamer import (
    HandleRenaming,
    SymbolRenaming,
)
from classiq.model_expansions.transformers.var_splitter import SymbolPart

if TYPE_CHECKING:
    from classiq.model_expansions.closure import FunctionClosure


INITIALIZED_VAR_MESSAGE = "Variable '{}' should be uninitialized here"
UNINITIALIZED_VAR_MESSAGE = "Variable '{}' should be initialized here"


class PortDirection(StrEnum):
    Input = "input"
    Inout = "inout"
    Output = "output"
    Outin = "outin"

    def negate(self) -> "PortDirection":
        if self == PortDirection.Input:
            return PortDirection.Output
        if self == PortDirection.Output:
            return PortDirection.Input
        return self

    @staticmethod
    def load(direction: PortDeclarationDirection) -> "PortDirection":
        if direction == PortDeclarationDirection.Input:
            return PortDirection.Input
        if direction == PortDeclarationDirection.Output:
            return PortDirection.Output
        if direction == PortDeclarationDirection.Inout:
            return PortDirection.Inout
        raise ClassiqInternalExpansionError

    def dump(self) -> PortDeclarationDirection:
        if self == PortDirection.Input:
            return PortDeclarationDirection.Input
        if self == PortDirection.Output:
            return PortDeclarationDirection.Output
        if self == PortDirection.Inout:
            return PortDeclarationDirection.Inout
        raise ClassiqInternalExpansionError


@dataclass(frozen=True)
class _Captured:
    defining_function: "FunctionClosure"
    is_propagated: bool

    def change_defining_function(
        self, new_defining_function: "FunctionClosure"
    ) -> Self:
        return dataclasses.replace(self, defining_function=new_defining_function)

    def set_propagated(self) -> Self:
        return dataclasses.replace(self, is_propagated=True)

    def update_propagation(self, other_captured_handle: Self) -> Self:
        if self.is_propagated and not other_captured_handle.is_propagated:
            return dataclasses.replace(self, is_propagated=False)
        return self


@dataclass(frozen=True)
class _CapturedHandle(_Captured):
    handle: HandleBinding
    quantum_type: QuantumType
    direction: PortDirection

    @property
    def mangled_name(self) -> str:
        return mangle_captured_var_name(
            self.handle.identifier,
            self.defining_function.name,
            self.defining_function.depth,
        )

    @property
    def port(self) -> PortDeclaration:
        return PortDeclaration(
            name=self.mangled_name,
            quantum_type=self.quantum_type,
            direction=self.direction.dump(),
        )

    def is_same_var(self, other: "_CapturedHandle") -> bool:
        return self.handle.name == other.handle.name and _same_closure(
            self.defining_function, other.defining_function
        )

    def change_direction(self, new_direction: PortDirection) -> "_CapturedHandle":
        return dataclasses.replace(self, direction=new_direction)

    def set_symbol(
        self, handle: HandleBinding, quantum_type: QuantumType
    ) -> "_CapturedHandle":
        return dataclasses.replace(self, handle=handle, quantum_type=quantum_type)


@dataclass(frozen=True)
class _CapturedClassicalVar(_Captured):
    name: str
    classical_type: ClassicalType
    defining_function: "FunctionClosure"

    @property
    def mangled_name(self) -> str:
        return mangle_captured_var_name(
            self.name,
            self.defining_function.name,
            self.defining_function.depth,
        )

    @property
    def parameter_declaration(self) -> ClassicalParameterDeclaration:
        return ClassicalParameterDeclaration(
            name=self.mangled_name, classical_type=self.classical_type
        )


HandleState = tuple[str, "FunctionClosure", bool]


@dataclass
class CapturedVars:
    _captured_handles: list[_CapturedHandle] = field(default_factory=list)
    _handle_states: list[HandleState] = field(default_factory=list)
    _captured_classical_vars: list[_CapturedClassicalVar] = field(default_factory=list)

    def capture_handle(
        self,
        handle: HandleBinding,
        quantum_type: QuantumType,
        defining_function: "FunctionClosure",
        direction: PortDeclarationDirection,
    ) -> None:
        self._capture_handle(
            _CapturedHandle(
                handle=handle,
                quantum_type=quantum_type,
                defining_function=defining_function,
                direction=PortDirection.load(direction),
                is_propagated=False,
            )
        )

    def _capture_handle(self, captured_handle: _CapturedHandle) -> None:
        if (
            isinstance(captured_handle.handle, NestedHandleBinding)
            and captured_handle.direction != PortDirection.Inout
        ):
            verb = (
                "free"
                if captured_handle.direction == PortDirection.Input
                else "allocate"
            )
            raise ClassiqExpansionError(
                f"Cannot {verb} partial variable {str(captured_handle.handle)!r}"
            )

        # A handle should be in either _captured_handles or _handle_states, but never
        # both

        new_handle_states = []
        for var_name, defining_function, handle_state in self._handle_states:
            if captured_handle.handle.name == var_name and _same_closure(
                captured_handle.defining_function, defining_function
            ):
                # verify variable state
                self._conjugate_direction(
                    handle_state, captured_handle.direction, var_name
                )
            else:
                new_handle_states.append((var_name, defining_function, handle_state))
        self._handle_states = new_handle_states

        new_captured_handles = []
        for existing_captured_handle in self._captured_handles:
            if not existing_captured_handle.is_same_var(captured_handle):
                new_captured_handles.append(existing_captured_handle)
                continue
            captured_handle = captured_handle.update_propagation(
                existing_captured_handle
            )
            if existing_captured_handle.handle == captured_handle.handle:
                captured_handle = captured_handle.change_direction(
                    self._conjugate_direction(
                        existing_captured_handle.direction,
                        captured_handle.direction,
                        str(captured_handle.handle),
                    )
                )
            elif captured_handle.handle.overlaps(existing_captured_handle.handle):
                captured_handle = self._intersect_handles(
                    existing_captured_handle, captured_handle
                )
            else:
                new_captured_handles.append(existing_captured_handle)
        new_captured_handles.append(captured_handle)
        self._captured_handles = new_captured_handles

    def _conjugate_direction(
        self,
        source_direction: PortDirection | bool,
        target_direction: PortDirection,
        var_name: str,
    ) -> PortDirection:
        if isinstance(source_direction, bool):
            source_direction = (
                PortDirection.Inout if source_direction else PortDirection.Outin
            )

        if source_direction == PortDirection.Input:
            if target_direction == PortDirection.Output:
                return PortDirection.Inout
            if target_direction == PortDirection.Outin:
                return PortDirection.Input
            raise ClassiqExpansionError(UNINITIALIZED_VAR_MESSAGE.format(var_name))

        if source_direction == PortDirection.Output:
            if target_direction == PortDirection.Input:
                return PortDirection.Outin
            if target_direction in (
                PortDirection.Output,
                PortDirection.Outin,
            ):
                raise ClassiqExpansionError(INITIALIZED_VAR_MESSAGE.format(var_name))
            return PortDirection.Output

        if source_direction == PortDirection.Inout:
            if target_direction in (PortDirection.Input, PortDirection.Inout):
                return target_direction
            raise ClassiqExpansionError(INITIALIZED_VAR_MESSAGE.format(var_name))

        if source_direction == PortDirection.Outin:
            if target_direction in (PortDirection.Output, PortDirection.Outin):
                return target_direction
            raise ClassiqExpansionError(UNINITIALIZED_VAR_MESSAGE.format(var_name))

        raise ClassiqInternalExpansionError(f"Unexpected direction {source_direction}")

    def _intersect_handles(
        self,
        existing_captured_handle: _CapturedHandle,
        captured_handle: _CapturedHandle,
    ) -> _CapturedHandle:
        if captured_handle.handle in existing_captured_handle.handle:
            if existing_captured_handle.direction in (
                PortDirection.Input,
                PortDirection.Outin,
            ):
                raise ClassiqExpansionError(
                    UNINITIALIZED_VAR_MESSAGE.format(captured_handle.handle)
                )
            return existing_captured_handle

        if existing_captured_handle.handle in captured_handle.handle:
            if captured_handle.direction in (
                PortDirection.Output,
                PortDirection.Outin,
            ):
                raise ClassiqExpansionError(
                    INITIALIZED_VAR_MESSAGE.format(captured_handle.handle)
                )
            return captured_handle

        sliced_handle, quantum_type, other_handle = self._get_sliced_handle(
            existing_captured_handle, captured_handle
        )
        if not isinstance(other_handle, SlicedHandleBinding):
            return captured_handle.set_symbol(sliced_handle, quantum_type)

        merged_handle, merged_quantum_type = self._merge_sliced_handles(
            sliced_handle, other_handle, quantum_type
        )
        return captured_handle.set_symbol(merged_handle, merged_quantum_type)

    @staticmethod
    def _get_sliced_handle(
        existing_captured_handle: _CapturedHandle,
        captured_handle: _CapturedHandle,
    ) -> tuple[SlicedHandleBinding, QuantumBitvector, HandleBinding]:
        handle_1 = existing_captured_handle.handle
        quantum_type_1 = existing_captured_handle.quantum_type
        handle_2 = captured_handle.handle
        quantum_type_2 = captured_handle.quantum_type
        if isinstance(handle_1, SlicedHandleBinding):
            sliced_handle = handle_1
            other_handle = handle_2
            quantum_type = quantum_type_1
        elif isinstance(handle_2, SlicedHandleBinding):
            sliced_handle = handle_2
            other_handle = handle_1
            quantum_type = quantum_type_2
        else:
            raise ClassiqInternalExpansionError(
                f"Unexpected overlapping handles {handle_1} and {handle_2}"
            )
        if not isinstance(quantum_type, QuantumBitvector):
            raise ClassiqInternalExpansionError
        return sliced_handle, quantum_type, other_handle

    @staticmethod
    def _merge_sliced_handles(
        handle_1: SlicedHandleBinding,
        handle_2: SlicedHandleBinding,
        quantum_type: QuantumBitvector,
    ) -> tuple[HandleBinding, QuantumBitvector]:
        if (
            not handle_1.start.is_evaluated()
            or not handle_1.end.is_evaluated()
            or not handle_2.start.is_evaluated()
            or not handle_2.end.is_evaluated()
        ):
            raise ClassiqInternalExpansionError

        new_start = min(handle_1.start.to_int_value(), handle_2.start.to_int_value())
        new_end = max(handle_1.end.to_int_value(), handle_2.end.to_int_value())
        merged_handle = SlicedHandleBinding(
            base_handle=handle_1.base_handle,
            start=Expression(expr=str(new_start)),
            end=Expression(expr=str(new_end)),
        )
        merged_quantum_type = QuantumBitvector(
            element_type=quantum_type.element_type,
            length=Expression(expr=str(new_end - new_start)),
        )
        return merged_handle, merged_quantum_type

    def capture_classical_var(
        self,
        var_name: str,
        var_type: ClassicalType,
        defining_function: "FunctionClosure",
    ) -> None:
        self._capture_classical_var(
            _CapturedClassicalVar(
                name=var_name,
                classical_type=var_type,
                defining_function=defining_function,
                is_propagated=False,
            )
        )

    def _capture_classical_var(
        self, captured_classical_var: _CapturedClassicalVar
    ) -> None:
        for existing_captured_classical_var in self._captured_classical_vars:
            if (
                existing_captured_classical_var.name == captured_classical_var.name
                and _same_closure(
                    existing_captured_classical_var.defining_function,
                    captured_classical_var.defining_function,
                )
            ):
                return
        self._captured_classical_vars.append(captured_classical_var)

    def update(self, other_captured_vars: "CapturedVars") -> None:
        for captured_handle in other_captured_vars._captured_handles:
            self._capture_handle(captured_handle)
        for captured_classical_var in other_captured_vars._captured_classical_vars:
            self._capture_classical_var(captured_classical_var)

    def negate(self) -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle.change_direction(captured_handle.direction.negate())
                for captured_handle in self._captured_handles
            ],
            _captured_classical_vars=self._captured_classical_vars,
        )

    def filter_vars(self, current_function: "FunctionClosure") -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle
                for captured_handle in self._captured_handles
                if not _same_closure(
                    captured_handle.defining_function, current_function
                )
            ],
            _captured_classical_vars=[
                captured_classical_var
                for captured_classical_var in self._captured_classical_vars
                if not _same_closure(
                    captured_classical_var.defining_function, current_function
                )
            ],
        )

    def filter_var_decls(
        self, current_declarations: list[VariableDeclarationStatement]
    ) -> "CapturedVars":
        current_declared_vars = {decl.name for decl in current_declarations}
        return CapturedVars(
            _captured_handles=[
                captured_handle
                for captured_handle in self._captured_handles
                if (
                    current_declared_vars is not None
                    and captured_handle.handle.name not in current_declared_vars
                )
            ],
            _captured_classical_vars=self._captured_classical_vars,
        )

    def set_propagated(self) -> "CapturedVars":
        return CapturedVars(
            _captured_handles=[
                captured_handle.set_propagated()
                for captured_handle in self._captured_handles
            ],
            _captured_classical_vars=[
                captured_classical_var.set_propagated()
                for captured_classical_var in self._captured_classical_vars
            ],
        )

    def get_captured_parameters(self) -> list[PositionalArg]:
        decls: list[PositionalArg]
        decls = [
            captured_classical_var.parameter_declaration
            for captured_classical_var in self._captured_classical_vars
        ]
        decls += [captured_handle.port for captured_handle in self._captured_handles]
        return decls

    def get_captured_args(self, current_function: "FunctionClosure") -> list[ArgValue]:
        args: list[ArgValue]
        args = [
            Expression(
                expr=(
                    captured_classical_var.name
                    if _same_closure(
                        current_function, captured_classical_var.defining_function
                    )
                    else captured_classical_var.mangled_name
                )
            )
            for captured_classical_var in self._captured_classical_vars
        ]
        args += [
            (
                captured_handle.handle
                if _same_closure(current_function, captured_handle.defining_function)
                else HandleBinding(name=captured_handle.mangled_name)
            )
            for captured_handle in self._captured_handles
        ]
        return args

    def get_captured_mapping(self) -> SymbolRenaming:
        mapping: SymbolRenaming
        mapping = {
            captured_handle.handle: [
                SymbolPart(
                    source_handle=captured_handle.handle,
                    target_var_name=captured_handle.mangled_name,
                    target_var_type=captured_handle.quantum_type,
                )
            ]
            for captured_handle in self._captured_handles
            if not captured_handle.is_propagated
        }
        mapping |= {
            (handle := HandleBinding(name=captured_classical_var.name)): [
                HandleRenaming(
                    source_handle=handle,
                    target_var_name=captured_classical_var.mangled_name,
                )
            ]
            for captured_classical_var in self._captured_classical_vars
            if not captured_classical_var.is_propagated
        }
        return mapping

    def init_var(self, var_name: str, defining_function: "FunctionClosure") -> None:
        self._handle_states.append((var_name, defining_function, False))

    def init_params(self, func: "FunctionClosure") -> None:
        ports = {
            param.name: param.direction
            for param in func.positional_arg_declarations
            if isinstance(param, PortDeclaration)
        }
        new_handle_states = [
            handle_state
            for handle_state in self._handle_states
            if handle_state[0] not in ports
        ]
        for var_name, direction in ports.items():
            new_handle_states.append(
                (
                    var_name,
                    func,
                    PortDirection.load(direction)
                    in (PortDirection.Input, PortDirection.Inout),
                )
            )
        self._handle_states = new_handle_states

    def _get_handle_states(self) -> list[HandleState]:
        return self._handle_states + list(
            {
                (
                    captured_handle.handle.name,
                    captured_handle.defining_function.depth,
                ): (
                    captured_handle.handle.name,
                    captured_handle.defining_function,
                    captured_handle.direction
                    in (PortDirection.Output, PortDirection.Inout),
                )
                for captured_handle in self._captured_handles
            }.values()
        )

    def set_parent(self, parent: "CapturedVars") -> None:
        self._handle_states += parent._get_handle_states()

    def get_state(self, var_name: str, defining_function: "FunctionClosure") -> bool:
        for name, func, state in self._handle_states:
            if name == var_name and _same_closure(func, defining_function):
                return state
        for captured_handle in self._captured_handles:
            if captured_handle.handle.name == var_name and _same_closure(
                captured_handle.defining_function, defining_function
            ):
                return captured_handle.direction in (
                    PortDirection.Output,
                    PortDirection.Inout,
                )
        raise ClassiqInternalExpansionError(
            f"Cannot find {var_name!r} from {defining_function.name!r}"
        )

    def clone(self) -> "CapturedVars":
        return CapturedVars(
            _captured_handles=list(self._captured_handles),
            _handle_states=list(self._handle_states),
            _captured_classical_vars=list(self._captured_classical_vars),
        )

    def set(
        self,
        other: "CapturedVars",
        source_func: "FunctionClosure",
        target_func: "FunctionClosure",
    ) -> None:
        self._captured_handles = []
        for captured_handle in other._captured_handles:
            if _same_closure(captured_handle.defining_function, source_func):
                self._captured_handles.append(
                    captured_handle.change_defining_function(target_func)
                )
            else:
                self._captured_handles.append(captured_handle)
        self._handle_states = []
        for var, defining_function, state in other._handle_states:
            if _same_closure(defining_function, source_func):
                self._handle_states.append((var, target_func, state))
            else:
                self._handle_states.append((var, defining_function, state))
        self._captured_classical_vars = []
        for captured_classical_var in other._captured_classical_vars:
            if _same_closure(captured_classical_var.defining_function, source_func):
                self._captured_classical_vars.append(
                    captured_classical_var.change_defining_function(target_func)
                )
            else:
                self._captured_classical_vars.append(captured_classical_var)


def _same_closure(closure_1: "FunctionClosure", closure_2: "FunctionClosure") -> bool:
    return closure_1.depth == closure_2.depth


def validate_args_are_not_propagated(
    args: Sequence[ArgValue], captured_vars: Sequence[ArgValue]
) -> None:
    if not captured_vars:
        return
    captured_handles = {
        demangle_handle(handle)
        for handle in captured_vars
        if isinstance(handle, HandleBinding)
    }
    arg_handles = {
        demangle_handle(arg) for arg in args if isinstance(arg, HandleBinding)
    }
    if any(
        arg_handle.overlaps(captured_handle)
        for arg_handle in arg_handles
        for captured_handle in captured_handles
    ):
        captured_handles_str = {str(handle) for handle in captured_handles}
        arg_handles_str = {str(handle) for handle in arg_handles}
        vars_msg = f"Explicitly passed variables: {arg_handles_str}, captured variables: {captured_handles_str}"
        raise ClassiqExpansionError(
            f"Cannot capture variables that are explicitly passed as arguments. "
            f"{vars_msg}"
        )


def validate_captured_directions(
    captured_vars: CapturedVars, report_outin: bool = True
) -> None:
    captured_inputs = [
        captured_handle.handle.name
        for captured_handle in captured_vars._captured_handles
        if captured_handle.direction == PortDirection.Input
    ]
    captured_outputs = [
        captured_handle.handle.name
        for captured_handle in captured_vars._captured_handles
        if captured_handle.direction
        in (
            (PortDirection.Output, PortDirection.Outin)
            if report_outin
            else (PortDirection.Output,)
        )
    ]
    if len(captured_inputs) > 0:
        raise ClassiqExpansionError(
            f"Captured quantum variables {captured_inputs!r} cannot be used as inputs"
        )
    if len(captured_outputs) > 0:
        raise ClassiqExpansionError(
            f"Captured quantum variables {captured_outputs!r} cannot be used as outputs"
        )


def validate_end_state(func: "FunctionClosure", captured_vars: CapturedVars) -> None:
    for param in func.positional_arg_declarations:
        if isinstance(param, PortDeclaration):
            state = captured_vars.get_state(param.name, func)
            expected_state = param.direction in (
                PortDeclarationDirection.Output,
                PortDeclarationDirection.Inout,
            )
            if state != expected_state:
                status = "initialized" if expected_state else "uninitialized"
                raise ClassiqExpansionError(
                    f"At the end of function {func.name}, variable {param.name!r} "
                    f"should be {status}"
                )
