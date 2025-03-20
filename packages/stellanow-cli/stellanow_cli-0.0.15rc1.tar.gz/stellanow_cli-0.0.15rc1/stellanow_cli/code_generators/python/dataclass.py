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
from stellanow_cli.code_generators.python.field_type_mapper import PythonFieldTypeMapper
from stellanow_cli.code_generators.python.reserved_words import python_escape_reserved_words
from stellanow_cli.core.utils.string_utils import snake_to_lower_camel


@dataclass
class PythonField:
    original_name: str
    python_name: str
    type: str
    is_model: bool

    @classmethod
    def from_stella_field(cls, field: StellaField | StellaModelField, model_details: Dict[str, StellaModelDetailed]):
        python_mapper = PythonFieldTypeMapper()
        field_type = python_mapper.map_field_type(field, model_details)
        is_model = field_type.endswith("Model")
        return cls(
            original_name=field.name,
            python_name=python_escape_reserved_words(snake_to_lower_camel(field.name)),
            type=field_type,
            is_model=is_model,
        )


@dataclass
class PythonEntity:
    original_name: str
    python_name: str

    @classmethod
    def from_stella_entity(cls, entity: StellaEntity):
        return cls(
            original_name=entity.name,
            python_name=python_escape_reserved_words(entity.name) + "EntityId",
        )


@dataclass
class CommentDefinition(CommonCommentDefinition):
    start: str = '"""'
    middle: str = ''
    end: str = '"""'
    single: str = "#"
