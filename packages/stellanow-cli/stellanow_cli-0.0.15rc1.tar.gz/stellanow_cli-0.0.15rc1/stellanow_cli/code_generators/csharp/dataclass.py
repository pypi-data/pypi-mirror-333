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
from dataclasses import dataclass
from typing import Dict

from stellanow_api_internals.datatypes.workflow_mgmt import (
    StellaEntity,
    StellaField,
    StellaModelDetailed,
    StellaModelField,
)

from stellanow_cli.code_generators.common.types import CommentDefinition as CommonCommentDefinition
from stellanow_cli.code_generators.csharp.field_type_mapper import CSharpFieldTypeMapper
from stellanow_cli.code_generators.csharp.reserved_words import csharp_escape_reserved_words
from stellanow_cli.core.utils.string_utils import camel_to_snake, snake_to_camel, snake_to_lower_camel


@dataclass
class CSharpField:
    original_name: str
    csharp_name: str
    type: str
    is_model: bool

    @classmethod
    def from_stella_field(cls, field: StellaField | StellaModelField, model_details: Dict[str, StellaModelDetailed]):
        csharp_mapper = CSharpFieldTypeMapper()
        field_type = csharp_mapper.map_field_type(field, model_details)
        is_model = field_type.endswith("Model")
        return cls(
            original_name=field.name,
            csharp_name=csharp_escape_reserved_words(snake_to_camel(camel_to_snake(field.name))),
            type=field_type,
            is_model=is_model,
        )

    def to_constructor_parameter_declaration(self):
        return f"{self.type} {self.csharp_name}"


@dataclass
class CSharpEntity:
    original_name: str
    csharp_name: str

    @classmethod
    def from_stella_field(cls, entity: StellaEntity):
        return cls(
            original_name=entity.name,
            csharp_name=csharp_escape_reserved_words(snake_to_lower_camel(entity.name)) + "Id",
        )

    def to_entity_type_declaration(self):
        return f'new EntityType("{self.original_name}", {self.csharp_name})'

    def to_constructor_parameter_declaration(self):
        return f"string {self.csharp_name}"


@dataclass
class CSharpModel:
    original_name: str
    csharp_name: str


@dataclass
class CommentDefinition(CommonCommentDefinition):
    start: str = '"""'
    middle: str = ''
    end: str = '"""'
    single: str = "#"
