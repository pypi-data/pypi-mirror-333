import dataclasses
import inspect
from enum import EnumMeta
from typing import (
    Any,
    ForwardRef,
    Literal,
    Optional,
    get_args,
    get_origin,
)

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.functions.classical_type import (
    Bool,
    ClassicalArray,
    ClassicalList,
    Integer,
    Real,
)
from classiq.interface.generator.functions.concrete_types import ConcreteClassicalType
from classiq.interface.generator.functions.type_name import Enum, Struct

from classiq.qmod.cparam import CArray, CBool, CInt, CReal
from classiq.qmod.utilities import version_portable_get_args

CARRAY_ERROR_MESSAGE = (
    "CArray accepts one or two generic parameters in the form "
    "`CArray[<element-type>]` or `CArray[<element-type>, <size>]`"
)


class PythonClassicalType:
    def convert(self, py_type: type) -> Optional[ConcreteClassicalType]:
        if py_type is int:
            return Integer().set_generative()
        elif py_type is CInt:
            return Integer()
        elif py_type in (float, complex):
            return Real().set_generative()
        elif py_type is CReal:
            return Real()
        elif py_type is bool:
            return Bool().set_generative()
        elif py_type is CBool:
            return Bool()
        elif get_origin(py_type) is list:
            element_type = self.convert(get_args(py_type)[0])
            if element_type is not None:
                return ClassicalList(element_type=element_type).set_generative()
        elif get_origin(py_type) is CArray:
            array_args = version_portable_get_args(py_type)
            if len(array_args) == 1:
                return ClassicalList(element_type=self.convert(array_args[0]))
            elif len(array_args) == 2:
                return ClassicalArray(
                    element_type=self.convert(array_args[0]),
                    size=get_type_hint_expr(array_args[1]),
                )
            raise ClassiqValueError(CARRAY_ERROR_MESSAGE)
        elif inspect.isclass(py_type) and dataclasses.is_dataclass(py_type):
            self.register_struct(py_type)
            return Struct(name=py_type.__name__)
        elif inspect.isclass(py_type) and isinstance(py_type, EnumMeta):
            self.register_enum(py_type)
            return Enum(name=py_type.__name__)
        elif py_type in (CArray, list):
            raise ClassiqValueError(CARRAY_ERROR_MESSAGE)
        return None

    def register_struct(self, py_type: type) -> None:
        pass

    def register_enum(self, py_type: EnumMeta) -> None:
        pass


def get_type_hint_expr(type_hint: Any) -> str:
    if isinstance(type_hint, ForwardRef):  # expression in string literal
        return str(type_hint.__forward_arg__)
    if get_origin(type_hint) == Literal:  # explicit numeric literal
        return str(get_args(type_hint)[0])
    else:
        return str(type_hint)  # implicit numeric literal
