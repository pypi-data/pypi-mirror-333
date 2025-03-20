"""
Copyright (C) 2022-2025 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""
from abc import ABC, abstractmethod
from typing import Dict, Union

# Assuming these imports are defined elsewhere in your codebase
from stellanow_api_internals.datatypes.workflow_mgmt import (
    StellaField,
    StellaFieldType,
    StellaModelDetailed,
    StellaModelField,
)

from stellanow_cli.core.enums import FieldType
from stellanow_cli.core.utils.string_utils import snake_to_camel


class FieldTypeMapper(ABC):
    @property
    @abstractmethod
    def type_mappings(self) -> Dict[FieldType, str]:
        """Return the type mappings for the specific language."""

    def map_field_type(
        self,
        field: Union[StellaField, StellaModelField],
        model_details: Dict[str, StellaModelDetailed],
    ) -> str:
        if isinstance(field.fieldType, dict):
            field_type = StellaFieldType(**field.fieldType)
        else:
            field_type = field.fieldType

        value_type = FieldType(field_type.value)

        if value_type == FieldType.MODEL:
            if field_type.modelRef:
                model_name = snake_to_camel(model_details[field_type.modelRef].name)
                return f"{model_name}Model"
            else:
                return self.type_mappings[FieldType.MODEL]

        return self.type_mappings.get(value_type, self.default_type())

    def default_type(self) -> str:
        return self.type_mappings.get(FieldType.MODEL, "object")
