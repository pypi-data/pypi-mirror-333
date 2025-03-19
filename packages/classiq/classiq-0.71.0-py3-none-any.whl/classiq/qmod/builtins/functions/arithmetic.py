from typing import Literal

from classiq.qmod.qfunc import qfunc
from classiq.qmod.qmod_parameter import CArray, CReal
from classiq.qmod.qmod_variable import Output, QArray, QBit, QNum


@qfunc(external=True)
def unitary(
    elements: CArray[CArray[CReal]],
    target: QArray[QBit, Literal["log(get_field(elements[0], 'len'), 2)"]],
) -> None:
    """
    [Qmod core-library function]

    Applies a unitary matrix on a quantum state.

    Args:
        elements:  A 2d array of complex numbers representing the unitary matrix. This matrix must be unitary.
        target: The quantum state to apply the unitary on. Should be of corresponding size.
    """
    pass


@qfunc(external=True)
def add(
    left: QArray[QBit],
    right: QArray[QBit],
    result: Output[
        QArray[
            QBit, Literal["Max(get_field(left, 'len'), get_field(right, 'len')) + 1"]
        ]
    ],
) -> None:
    pass


@qfunc(external=True)
def modular_add(left: QArray[QBit], right: QArray[QBit]) -> None:
    pass


@qfunc(external=True)
def modular_add_constant(left: CReal, right: QNum) -> None:
    pass


@qfunc(external=True)
def integer_xor(left: QArray[QBit], right: QArray[QBit]) -> None:
    pass


@qfunc(external=True)
def real_xor_constant(left: CReal, right: QNum) -> None:
    pass
