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
from typing import Dict

from stellanow_cli.core.enums import FieldType
from stellanow_cli.core.filed_type_mapper import FieldTypeMapper


class TypeScriptFieldTypeMapper(FieldTypeMapper):
    @property
    def type_mappings(self) -> Dict[FieldType, str]:
        return {
            FieldType.DECIMAL: "number",
            FieldType.INTEGER: "number",
            FieldType.BOOLEAN: "boolean",
            FieldType.STRING: "string",
            FieldType.DATE: "string",  # Assuming ISO string for simplicity
            FieldType.DATETIME: "string",  # Assuming ISO string for simplicity
            FieldType.MODEL: "any",  # Fallback, overridden by specific model types
            FieldType.ANY: "any",
        }