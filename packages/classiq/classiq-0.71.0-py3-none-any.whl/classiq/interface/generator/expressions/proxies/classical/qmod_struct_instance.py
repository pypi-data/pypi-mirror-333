import types
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from classiq.interface.generator.expressions.expression_types import ExpressionValue
    from classiq.interface.generator.types.struct_declaration import StructDeclaration


class QmodStructInstance:
    def __init__(
        self,
        struct_declaration: "StructDeclaration",
        fields: Mapping[str, "ExpressionValue"],
    ) -> None:
        struct_declaration.validate_fields(fields)
        self.struct_declaration = struct_declaration
        self._fields = fields

    @property
    def type_name(self) -> str:
        return f"Struct {self.struct_declaration.name}"

    @property
    def fields(self) -> Mapping[str, Any]:
        return types.MappingProxyType(self._fields)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        fields = ", ".join(
            f"{field_name}={field_value}"
            for field_name, field_value in self._fields.items()
        )
        return f"{self.struct_declaration.name}({fields})"
