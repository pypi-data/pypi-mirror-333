import ast
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Generic,
    Optional,
    TypeVar,
    Union,
)

import sympy

from classiq.interface.debug_info.debug_info import (
    DebugInfoCollection,
    new_function_debug_info_by_node,
)
from classiq.interface.exceptions import ClassiqInternalExpansionError
from classiq.interface.generator.expressions.evaluated_expression import (
    EvaluatedExpression,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.proxies.classical.classical_proxy import (
    ClassicalProxy,
)
from classiq.interface.generator.expressions.proxies.classical.utils import (
    get_proxy_type,
)
from classiq.interface.generator.functions.classical_type import ClassicalType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_declaration import (
    NamedParamsQuantumFunctionDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumOperation, QuantumStatement

from classiq.model_expansions.closure import Closure, GenerativeClosure
from classiq.model_expansions.function_builder import (
    OperationBuilder,
    OperationContext,
)
from classiq.model_expansions.scope import QuantumSymbol, Scope
from classiq.model_expansions.sympy_conversion.sympy_to_python import (
    translate_sympy_quantum_expression,
)
from classiq.model_expansions.utils.counted_name_allocator import CountedNameAllocator
from classiq.model_expansions.visitors.variable_references import VarRefCollector
from classiq.qmod.quantum_function import GenerativeQFunc

if TYPE_CHECKING:
    from classiq.model_expansions.interpreters.base_interpreter import BaseInterpreter

QuantumStatementT = TypeVar(
    "QuantumStatementT", bound=QuantumStatement, contravariant=True
)


class Emitter(Generic[QuantumStatementT], ABC):
    def __init__(self, interpreter: "BaseInterpreter") -> None:
        self._interpreter = interpreter

        self._machine_precision = self._interpreter._model.preferences.machine_precision
        self._expanded_functions_compilation_metadata = (
            self._interpreter._expanded_functions_compilation_metadata
        )
        self._functions_compilation_metadata = (
            self._interpreter._functions_compilation_metadata
        )

    @abstractmethod
    def emit(self, statement: QuantumStatementT, /) -> bool:
        pass

    def _expand_operation(self, closure: Closure) -> OperationContext:
        return self._interpreter._expand_operation(closure)

    @property
    def _builder(self) -> OperationBuilder:
        return self._interpreter._builder

    @property
    def _current_scope(self) -> Scope:
        return self._builder.current_scope

    @property
    def _top_level_scope(self) -> Scope:
        return self._interpreter._top_level_scope

    @property
    def _expanded_functions(self) -> dict[str, NativeFunctionDefinition]:
        return self._interpreter._expanded_functions

    @property
    def _expanded_functions_by_name(self) -> dict[str, NativeFunctionDefinition]:
        return nameables_to_dict(list(self._interpreter._expanded_functions.values()))

    @property
    def _counted_name_allocator(self) -> CountedNameAllocator:
        return self._interpreter._counted_name_allocator

    @property
    def _debug_info(self) -> DebugInfoCollection:
        return self._interpreter._model.debug_info

    def _expand_generative_context(
        self,
        op: QuantumOperation,
        context_name: str,
        block_names: Union[None, str, list[str]] = None,
        func_decl: Optional[NamedParamsQuantumFunctionDeclaration] = None,
    ) -> OperationContext:
        if isinstance(block_names, str):
            block_names = [block_names]
        block_names = block_names or ["body"]
        func_decl = func_decl or NamedParamsQuantumFunctionDeclaration(
            name=context_name
        )
        gen_closure = GenerativeClosure(
            name=func_decl.name,
            scope=Scope(parent=self._interpreter._builder.current_scope),
            blocks={},
            generative_blocks={
                block_name: GenerativeQFunc(
                    op.get_generative_block(block_name), func_decl
                )
                for block_name in block_names
            },
        )
        context = self._interpreter._expand_operation(gen_closure)
        op.clear_generative_blocks()
        return context

    def _evaluate_expression(
        self, expression: Expression, preserve_bool_ops: bool = False
    ) -> Expression:
        evaluated_expression = self._interpreter.evaluate(expression)
        if isinstance(evaluated_expression.value, sympy.Basic):
            new_expression = Expression(
                expr=translate_sympy_quantum_expression(
                    evaluated_expression.value,
                    preserve_bool_ops=preserve_bool_ops,
                )
            )
        else:
            new_expression = Expression(expr=str(evaluated_expression.value))
        new_expression._evaluated_expr = EvaluatedExpression(
            value=evaluated_expression.value
        )
        return new_expression

    def emit_statement(self, statement: QuantumStatement) -> None:
        self._update_captured_classical_vars(statement)
        if isinstance(statement, QuantumOperation):
            self._update_captured_vars(statement)
        if statement.uuid not in self._interpreter._model.debug_info:
            self._interpreter._model.debug_info[statement.uuid] = (
                new_function_debug_info_by_node(statement)  # type:ignore[arg-type]
            )
        self._builder.emit_statement(statement)

    def _update_captured_classical_vars(self, stmt: QuantumStatement) -> None:
        for expr in stmt.expressions:
            for var_name, var_type in self._get_classical_vars_in_expression(expr):
                self._capture_classical_var(var_name, var_type)

    def _update_captured_vars(self, op: QuantumOperation) -> None:
        handles = (
            [(handle, PortDeclarationDirection.Input) for handle in op.inputs]
            + [(handle, PortDeclarationDirection.Output) for handle in op.outputs]
            + [(handle, PortDeclarationDirection.Inout) for handle in op.inouts]
        )
        for handle, direction in handles:
            self._capture_handle(handle, direction)

    def _capture_handle(
        self, handle: HandleBinding, direction: PortDeclarationDirection
    ) -> None:
        if handle.name not in self._current_scope:
            return
        defining_function = self._current_scope[handle.name].defining_function
        if defining_function is None:
            raise ClassiqInternalExpansionError
        symbol: QuantumSymbol = self._interpreter.evaluate(handle).value
        self._builder.current_block.captured_vars.capture_handle(
            handle=symbol.handle,
            quantum_type=symbol.quantum_type,
            defining_function=defining_function,
            direction=direction,
        )

    def _capture_classical_var(self, var_name: str, var_type: ClassicalType) -> None:
        if var_name not in self._current_scope:
            return
        defining_function = self._current_scope[var_name].defining_function
        if defining_function is None:
            raise ClassiqInternalExpansionError
        self._builder.current_block.captured_vars.capture_classical_var(
            var_name=var_name,
            var_type=var_type,
            defining_function=defining_function,
        )

    def _get_symbols_in_expression(self, expr: Expression) -> list[QuantumSymbol]:
        vrc = VarRefCollector(ignore_duplicated_handles=True)
        vrc.visit(ast.parse(expr.expr))
        handles = dict.fromkeys(
            handle
            for handle in vrc.var_handles
            if isinstance(self._current_scope[handle.name].value, QuantumSymbol)
        )
        return [self._interpreter.evaluate(handle).value for handle in handles]

    def _get_classical_vars_in_expression(
        self, expr: Expression
    ) -> list[tuple[str, ClassicalType]]:
        vrc = VarRefCollector(ignore_duplicated_handles=True, ignore_sympy_symbols=True)
        vrc.visit(ast.parse(expr.expr))
        return list(
            {
                handle.name: get_proxy_type(proxy)
                for handle in vrc.var_handles
                if handle.name in self._current_scope
                and isinstance(
                    proxy := self._current_scope[handle.name].value, ClassicalProxy
                )
            }.items()
        )
