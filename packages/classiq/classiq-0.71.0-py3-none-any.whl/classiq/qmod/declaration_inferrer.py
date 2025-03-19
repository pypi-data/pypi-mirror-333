import dataclasses
import sys
from collections.abc import Sequence
from enum import EnumMeta
from typing import (
    Any,
    Callable,
    Literal,
    Optional,
    get_args,
    get_origin,
    overload,
)

from typing_extensions import _AnnotatedAlias

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_qualifier import TypeQualifier
from classiq.interface.generator.types.enum_declaration import declaration_from_enum
from classiq.interface.generator.types.struct_declaration import StructDeclaration
from classiq.interface.model.classical_parameter_declaration import (
    AnonClassicalParameterDeclaration,
)
from classiq.interface.model.port_declaration import AnonPortDeclaration
from classiq.interface.model.quantum_function_declaration import (
    AnonPositionalArg,
    AnonQuantumOperandDeclaration,
    NamedParamsQuantumFunctionDeclaration,
    PositionalArg,
)

from classiq.qmod.builtins.enums import BUILTIN_ENUM_DECLARATIONS
from classiq.qmod.builtins.structs import BUILTIN_STRUCT_DECLARATIONS
from classiq.qmod.model_state_container import ModelStateContainer
from classiq.qmod.python_classical_type import PythonClassicalType
from classiq.qmod.qmod_variable import QVar, get_port_from_type_hint
from classiq.qmod.quantum_callable import QCallableList
from classiq.qmod.semantics.validation.type_hints import validate_annotation
from classiq.qmod.utilities import unmangle_keyword, version_portable_get_args

if sys.version_info[0:2] >= (3, 9):
    from typing import Annotated


class _PythonClassicalType(PythonClassicalType):
    def __init__(self, qmodule: Optional[ModelStateContainer]):
        super().__init__()
        self.qmodule = qmodule

    def register_enum(self, py_type: EnumMeta) -> None:
        if (
            self.qmodule is None
            or py_type.__name__ in BUILTIN_ENUM_DECLARATIONS
            or py_type.__name__ in self.qmodule.enum_decls
        ):
            return

        enum_decl = declaration_from_enum(py_type)
        self.qmodule.enum_decls[py_type.__name__] = enum_decl

    def register_struct(self, py_type: type) -> None:
        if (
            self.qmodule is None
            or py_type.__name__ in BUILTIN_STRUCT_DECLARATIONS
            or py_type.__name__ in self.qmodule.type_decls
        ):
            return

        struct_decl = StructDeclaration(
            name=py_type.__name__,
            variables={
                f.name: self.convert(f.type) for f in dataclasses.fields(py_type)
            },
        )
        self.qmodule.type_decls[py_type.__name__] = struct_decl


def python_type_to_qmod(
    py_type: type, *, qmodule: Optional[ModelStateContainer]
) -> Optional[ConcreteClassicalType]:
    return _PythonClassicalType(qmodule).convert(py_type)


def _extract_port_decl(name: Optional[str], py_type: Any) -> AnonPortDeclaration:
    quantum_type, direction, qualifier = get_port_from_type_hint(py_type)
    param = AnonPortDeclaration(
        name=None,
        direction=direction,
        quantum_type=quantum_type,
        type_qualifier=qualifier,
    )
    if name is not None:
        param = param.rename(name)
    return param


def _extract_operand_decl(
    name: Optional[str], py_type: Any, qmodule: Optional[ModelStateContainer]
) -> AnonQuantumOperandDeclaration:
    is_list = (get_origin(py_type) or py_type) is QCallableList
    if get_origin(py_type) is list:
        is_list = True
        py_type = version_portable_get_args(py_type)[0]
    type_args = version_portable_get_args(py_type)
    if len(type_args) > 0 and isinstance(type_args[0], list):  # Callable support
        type_args = tuple(type_args[0])
    param_decls = [_extract_operand_param(arg_type) for arg_type in type_args]
    param = AnonQuantumOperandDeclaration(
        name=name,
        positional_arg_declarations=_extract_positional_args(
            param_decls, qmodule=qmodule
        ),
        is_list=is_list,
    )
    if name is not None:
        param = param.rename(name)
    return param


def _extract_operand_param(py_type: Any) -> tuple[Optional[str], Any]:
    if get_origin(py_type) is not Annotated:
        return None, py_type

    args = get_args(py_type)
    _validate_annotations(args, py_type)
    param_name = _get_param_name(args)

    if param_name is None:
        if len(args) > 1:
            return None, _unpacked_annotated(args[0], args[1:])
        return None, args[0]

    if len(args) > 2:
        return param_name, _unpacked_annotated(args[0], args[1:-1])
    return param_name, args[0]


def _unpacked_annotated(arg_0: Any, args: Any) -> _AnnotatedAlias:
    return Annotated.__class_getitem__((arg_0, *args))  # type:ignore[attr-defined]


def _get_param_name(py_type_args: Any) -> Optional[str]:
    if isinstance(py_type_args[-1], str) and not isinstance(
        py_type_args[-1], (PortDeclarationDirection, TypeQualifier)
    ):
        return py_type_args[-1]
    elif py_type_args[-1] is Literal:
        return str(version_portable_get_args(py_type_args[-1])[0])  # type: ignore[arg-type]
    else:
        return None


def _validate_annotations(py_type_args: Any, py_type: Any) -> None:
    for arg in py_type_args[1:-1]:
        if (
            isinstance(arg, str) and not isinstance(arg, PortDeclarationDirection)
        ) or arg is Literal:
            raise ClassiqValueError(
                f"Operand parameter declaration must be of the form <param-type> or "
                f"Annotated[<param-type>, <param-name>]. Got {py_type}"
            )


@overload
def _extract_positional_args(
    args: Sequence[tuple[str, Any]], qmodule: Optional[ModelStateContainer]
) -> Sequence[PositionalArg]:
    pass


@overload
def _extract_positional_args(
    args: Sequence[tuple[Optional[str], Any]], qmodule: Optional[ModelStateContainer]
) -> Sequence[AnonPositionalArg]:
    pass


def _extract_positional_args(
    args: Sequence[tuple[Optional[str], Any]], qmodule: Optional[ModelStateContainer]
) -> Sequence[AnonPositionalArg]:
    result: list[AnonPositionalArg] = []
    for name, py_type in args:
        validate_annotation(py_type)
        if name == "return":
            continue
        name = unmangle_keyword(name)
        classical_type = python_type_to_qmod(py_type, qmodule=qmodule)
        if classical_type is not None:
            param = AnonClassicalParameterDeclaration(
                name=None,
                classical_type=classical_type,
            )
            if name is not None:
                param = param.rename(name)
            result.append(param)
        elif is_qvar(py_type):
            result.append(_extract_port_decl(name, py_type))
        else:
            result.append(_extract_operand_decl(name, py_type, qmodule=qmodule))
    return result


def infer_func_decl(
    py_func: Callable, qmodule: Optional[ModelStateContainer] = None
) -> NamedParamsQuantumFunctionDeclaration:
    return NamedParamsQuantumFunctionDeclaration(
        name=unmangle_keyword(py_func.__name__),
        positional_arg_declarations=_extract_positional_args(
            list(py_func.__annotations__.items()), qmodule=qmodule
        ),
    )


def is_qvar(type_hint: Any) -> Any:
    non_annotated_type = (
        type_hint.__origin__ if isinstance(type_hint, _AnnotatedAlias) else type_hint
    )
    type_ = get_origin(non_annotated_type) or non_annotated_type
    return issubclass(type_, QVar)
