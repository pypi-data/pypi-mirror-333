from typing import Any, NewType, Optional, Union

import pydantic

from classiq.interface.analyzer.result import QasmCode
from classiq.interface.exceptions import ClassiqError, ClassiqValueError
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.model import MAIN_FUNCTION_NAME, Model, SerializedModel

from classiq import QuantumProgram
from classiq._internals import async_utils
from classiq._internals.api_wrapper import ApiWrapper
from classiq.qmod.quantum_function import GenerativeQFunc, QFunc

SerializedQuantumProgram = NewType("SerializedQuantumProgram", str)

CANT_PARSE_QUANTUM_PROGRAM_MSG = (
    "Can not parse quantum_program into GeneratedCircuit, \n"
)


def show(quantum_program: SerializedQuantumProgram, display_url: bool = True) -> None:
    """
    Displays the interactive representation of the quantum program in the Classiq IDE.

    Args:
        quantum_program:
            The serialized quantum program to be displayed.
        display_url:
            Whether to print the url

    Links:
        [Visualization tool](https://docs.classiq.io/latest/reference-manual/analyzer/quantum-program-visualization-tool/)
    """
    try:
        circuit = QuantumProgram.model_validate_json(quantum_program)
    except pydantic.ValidationError as exc:
        raise ClassiqValueError(CANT_PARSE_QUANTUM_PROGRAM_MSG) from exc
    circuit.show()  # type: ignore[attr-defined]


async def quantum_program_from_qasm_async(qasm: str) -> SerializedQuantumProgram:
    quantum_program = await ApiWrapper.get_generated_circuit_from_qasm(
        QasmCode(code=qasm)
    )
    return SerializedQuantumProgram(quantum_program.model_dump_json())


def quantum_program_from_qasm(qasm: str) -> SerializedQuantumProgram:
    """
    generate a quantum program from a QASM file.

    Args:
        qasm: A QASM2/3 string.

    Returns:
        SerializedQuantumProgram: Quantum program serialized as a string. (See: QuantumProgram)
    """
    return async_utils.run(quantum_program_from_qasm_async(qasm))


async def synthesize_async(
    serialized_model: SerializedModel,
) -> SerializedQuantumProgram:
    model = Model.model_validate_json(serialized_model)
    quantum_program = await ApiWrapper.call_generation_task(model)
    return SerializedQuantumProgram(quantum_program.model_dump_json(indent=2))


def synthesize(
    model: Union[SerializedModel, QFunc, GenerativeQFunc],
    auto_show: bool = False,
    constraints: Optional[Constraints] = None,
    preferences: Optional[Preferences] = None,
) -> SerializedQuantumProgram:
    """
    Synthesize a model with the Classiq engine to receive a quantum program.
    [More details](https://docs.classiq.io/latest/reference-manual/synthesis/)

    Args:
        model: The entry point of the Qmod model - a qfunc named 'main' (or alternatively the output of 'create_model').
        auto_show: Whether to 'show' the synthesized model (False by default).
        constraints: Constraints for the synthesis of the model. See Constraints (Optional).
        preferences: Preferences for the synthesis of the model. See Preferences (Optional).

    Returns:
        SerializedQuantumProgram: Quantum program serialized as a string. (See: QuantumProgram)
    """
    if isinstance(model, (QFunc, GenerativeQFunc)):
        func_name = model._py_callable.__name__
        if func_name != MAIN_FUNCTION_NAME:
            raise ClassiqError(
                f"The entry point function must be named 'main', got {func_name!r}"
            )
        model_obj = model.create_model(constraints=constraints, preferences=preferences)
        serialized_model = model_obj.get_model()
    else:
        serialized_model = model
    result = async_utils.run(synthesize_async(serialized_model))
    if auto_show:
        show(result)
    return result


def set_preferences(
    serialized_model: SerializedModel,
    preferences: Optional[Preferences] = None,
    **kwargs: Any,
) -> SerializedModel:
    """
    Overrides the preferences of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        preferences: The new preferences to be set for the model. Can be passed as keyword arguments.

    Returns:
        SerializedModel: The updated model with the new preferences applied.
    """
    if preferences is None:
        if kwargs:
            preferences = Preferences(**kwargs)
        else:
            raise ClassiqValueError(
                "Missing preferences. Either pass `Preferences` object or pass keywords"
            )

    model = Model.model_validate_json(serialized_model)
    model.preferences = preferences
    return model.get_model()


def update_preferences(
    serialized_model: SerializedModel, **kwargs: Any
) -> SerializedModel:
    """
    Updates the preferences of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        kwargs: key-value combination of preferences fields to update

    Returns:
        SerializedModel: The updated model with the new preferences applied.
    """
    model = Model.model_validate_json(serialized_model)

    for key, value in kwargs.items():
        setattr(model.preferences, key, value)
    return model.get_model()


def set_constraints(
    serialized_model: SerializedModel,
    constraints: Optional[Constraints] = None,
    **kwargs: Any,
) -> SerializedModel:
    """
    Overrides the constraints of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        constraints: The new constraints to be set for the model. Can be passed as keyword arguments.

    Returns:
        SerializedModel: The updated model with the new constraints applied.
    """
    if constraints is None:
        if kwargs:
            constraints = Constraints(**kwargs)
        else:
            raise ClassiqValueError(
                "Missing constraints. Either pass `Constraints` object or pass keywords"
            )

    model = Model.model_validate_json(serialized_model)
    model.constraints = constraints
    return model.get_model()


def update_constraints(
    serialized_model: SerializedModel, **kwargs: Any
) -> SerializedModel:
    """
    Updates the constraints of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        kwargs: key-value combination of constraints fields to update

    Returns:
        SerializedModel: The updated model with the new constraints applied.
    """
    model = Model.model_validate_json(serialized_model)

    for key, value in kwargs.items():
        setattr(model.constraints, key, value)
    return model.get_model()


def set_execution_preferences(
    serialized_model: SerializedModel,
    execution_preferences: Optional[ExecutionPreferences] = None,
    **kwargs: Any,
) -> SerializedModel:
    """
    Overrides the execution preferences of a (serialized) model and returns the updated model.

    Args:
        serialized_model: A serialization of the defined model.
        execution_preferences: The new execution preferences to be set for the model. Can be passed as keyword arguments.
    Returns:
        SerializedModel: The model with the attached execution preferences.

    For more examples please see: [set_execution_preferences](https://docs.classiq.io/latest/reference-manual/executor/?h=set_execution_preferences#usage)
    """
    if execution_preferences is None:
        if kwargs:
            execution_preferences = ExecutionPreferences(**kwargs)
        else:
            raise ClassiqValueError(
                "Missing execution_preferences. Either pass `ExecutionPreferences` object or pass keywords"
            )

    model = Model.model_validate_json(serialized_model)
    model.execution_preferences = execution_preferences
    return model.get_model()


def update_execution_preferences(
    serialized_model: SerializedModel, **kwargs: Any
) -> SerializedModel:
    """
    Updates the execution_preferences of a (serialized) model and returns the updated model.

    Args:
        serialized_model: The model in serialized form.
        kwargs: key-value combination of execution_preferences fields to update

    Returns:
        SerializedModel: The updated model with the new execution_preferences applied.
    """
    model = Model.model_validate_json(serialized_model)

    for key, value in kwargs.items():
        setattr(model.execution_preferences, key, value)

    return model.get_model()


__all__ = [
    "SerializedModel",
    "SerializedQuantumProgram",
    "set_constraints",
    "set_execution_preferences",
    "set_preferences",
    "synthesize",
    "update_constraints",
    "update_execution_preferences",
    "update_preferences",
]
