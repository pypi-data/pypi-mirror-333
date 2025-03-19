import warnings

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.allocate import Allocate
from classiq.interface.model.bind_operation import BindOperation
from classiq.interface.model.handle_binding import HandleBinding, SlicedHandleBinding
from classiq.interface.model.model import Model, SerializedModel
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_expressions.arithmetic_operation import (
    ArithmeticOperation,
    ArithmeticOperationKind,
)
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_lambda_function import QuantumLambdaFunction
from classiq.interface.model.quantum_type import QuantumBitvector, QuantumNumeric
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq import RegisterUserInput
from classiq.open_library.functions.grover import grover_search, phase_oracle

_OUTPUT_VARIABLE_NAME = "result"

_PREDICATE_FUNCTION_NAME = "expr_predicate"


def _arithmetic_oracle_ios(
    definitions: list[tuple[str, RegisterUserInput]], handle_name: str
) -> list[HandleBinding]:
    cursor = 0
    ios: list[HandleBinding] = []
    for _, reg in definitions:
        ios.append(
            SlicedHandleBinding(
                base_handle=HandleBinding(name=handle_name),
                start=Expression(expr=f"{cursor}"),
                end=Expression(expr=f"{cursor + reg.size}"),
            )
        )
        cursor += reg.size
    return ios


def _construct_arithmetic_oracle(
    predicate_function: str,
    definitions: list[tuple[str, RegisterUserInput]],
) -> QuantumFunctionCall:
    predicate_var_binding = _arithmetic_oracle_ios(definitions, "state")
    predicate_var_binding.append(HandleBinding(name="oracle"))
    return QuantumFunctionCall(
        function="phase_oracle",
        positional_args=[
            QuantumLambdaFunction(
                pos_rename_params=["state", "oracle"],
                body=[
                    QuantumFunctionCall(
                        function=predicate_function,
                        positional_args=predicate_var_binding,
                    ),
                ],
            ),
            HandleBinding(name="packed_vars"),
        ],
    )


def grover_main_port_declarations(
    definitions: list[tuple[str, RegisterUserInput]],
    direction: PortDeclarationDirection,
) -> list[PortDeclaration]:
    return [
        PortDeclaration(
            name=name,
            quantum_type=QuantumNumeric(
                size=Expression(expr=f"{reg.size}"),
                is_signed=Expression(expr=f"{reg.is_signed}"),
                fraction_digits=Expression(expr=f"{reg.fraction_places}"),
            ),
            direction=direction,
        )
        for name, reg in definitions
    ]


def construct_grover_model(
    definitions: list[tuple[str, RegisterUserInput]],
    expression: str,
    num_reps: int = 1,
) -> SerializedModel:
    warnings.warn(
        "Function 'construct_grover_model' has been deprecated and will no longer"
        "be supported starting on 03/02/2025 the earliest\nHint: It is now possible to "
        "implement the Grover algorithm in pure Qmod. For example, see the Grover notebook on the "
        "Classiq library at https://github.com/Classiq/classiq-library/blob/main/algorithms/grover/3_sat_grover/3_sat_grover.ipynb",
        category=DeprecationWarning,
        stacklevel=2,
    )
    predicate_port_decls = grover_main_port_declarations(
        definitions, PortDeclarationDirection.Inout
    )
    predicate_port_decls.append(
        PortDeclaration(
            name="res",
            quantum_type=QuantumBitvector(length=Expression(expr="1")),
            direction=PortDeclarationDirection.Inout,
        )
    )
    num_qubits = sum(reg.size for _, reg in definitions)

    grover_model = Model(
        functions=[
            NativeFunctionDefinition(
                name=_PREDICATE_FUNCTION_NAME,
                positional_arg_declarations=predicate_port_decls,
                body=[
                    ArithmeticOperation(
                        expression=Expression(expr=expression),
                        result_var=HandleBinding(name="res"),
                        operation_kind=ArithmeticOperationKind.InplaceXor,
                    ),
                ],
            ),
            NativeFunctionDefinition(
                name="main",
                positional_arg_declarations=grover_main_port_declarations(
                    definitions, PortDeclarationDirection.Output
                ),
                body=[
                    VariableDeclarationStatement(name="packed_vars"),
                    Allocate(
                        size=Expression(expr=f"{num_qubits}"),
                        target=HandleBinding(name="packed_vars"),
                    ),
                    QuantumFunctionCall(
                        function="grover_search",
                        positional_args=[
                            Expression(expr=f"{num_reps}"),
                            QuantumLambdaFunction(
                                pos_rename_params=["packed_vars"],
                                body=[
                                    _construct_arithmetic_oracle(
                                        _PREDICATE_FUNCTION_NAME,
                                        definitions,
                                    )
                                ],
                            ),
                            HandleBinding(name="packed_vars"),
                        ],
                    ),
                    BindOperation(
                        in_handles=[HandleBinding(name="packed_vars")],
                        out_handles=[
                            HandleBinding(name=name) for name, _ in definitions
                        ],
                    ),
                ],
            ),
            *[f for f in grover_search.create_model().functions if f.name != "main"],
            *[f for f in phase_oracle.create_model().functions if f.name != "main"],
        ],
    )
    return grover_model.get_model()
