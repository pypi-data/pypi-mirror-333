from typing import Optional, Union

from classiq.interface.exceptions import ClassiqError
from classiq.interface.executor.execution_preferences import ExecutionPreferences
from classiq.interface.generator.model.constraints import Constraints
from classiq.interface.generator.model.preferences.preferences import Preferences
from classiq.interface.model.model import MAIN_FUNCTION_NAME, SerializedModel

from classiq.qmod.classical_function import CFunc
from classiq.qmod.quantum_function import GenerativeQFunc, QFunc
from classiq.qmod.write_qmod import write_qmod


def create_model(
    entry_point: Union[QFunc, GenerativeQFunc],
    constraints: Optional[Constraints] = None,
    execution_preferences: Optional[ExecutionPreferences] = None,
    preferences: Optional[Preferences] = None,
    classical_execution_function: Optional[CFunc] = None,
    out_file: Optional[str] = None,
) -> SerializedModel:
    """
    Create a serialized model from a given Qmod entry function and additional parameters.

    Args:
        entry_point: The entry point function for the model, which must be a QFunc named 'main'.
        constraints: Constraints for the synthesis of the model. See Constraints (Optional).
        execution_preferences: Preferences for the execution of the model. See ExecutionPreferences (Optional).
        preferences: Preferences for the synthesis of the model. See Preferences (Optional).
        classical_execution_function: A function for the classical execution logic, which must be a CFunc (Optional).
        out_file: File path to write the Qmod model in native Qmod representation to (Optional).

    Returns:
        SerializedModel: A serialized model.

    Raises:
        ClassiqError: If the entry point function is not named 'main'.
    """

    if entry_point.func_decl.name != MAIN_FUNCTION_NAME:
        raise ClassiqError(
            f"The entry point function must be named 'main', got '{entry_point.func_decl.name}'"
        )

    model = entry_point.create_model(
        constraints,
        execution_preferences,
        preferences,
        classical_execution_function,
    )
    result = model.get_model()

    if out_file is not None:
        write_qmod(result, out_file)

    return result
