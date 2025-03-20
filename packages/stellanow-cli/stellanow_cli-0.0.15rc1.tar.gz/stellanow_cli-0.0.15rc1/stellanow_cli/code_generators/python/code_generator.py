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
import difflib
import json
import re
from datetime import datetime
from typing import Dict, List

from stellanow_api_internals.datatypes.workflow_mgmt import StellaEventDetailed, StellaModelDetailed

from stellanow_cli.code_generators.common.code_generator import CodeGenerator
from stellanow_cli.code_generators.python.dataclass import CommentDefinition, PythonEntity, PythonField
from stellanow_cli.core.enums import StellaLanguage
from stellanow_cli.core.utils.string_utils import camel_to_snake, remove_comments, snake_to_camel
from stellanow_cli.exceptions.cli_exceptions import (
    StellaNowCLINamespaceNotFoundException,
    StellaNowCLINoEntityAssociatedWithEventException,
)


class PythonCodeGenerator(CodeGenerator):
    @classmethod
    def generate_message_class(
            cls, event: StellaEventDetailed, model_details: Dict[str, StellaModelDetailed], **kwargs
    ) -> str:
        template = PythonCodeGenerator.load_template(f"message")

        fields = [PythonField.from_stella_field(field, model_details) for field in event.fields]
        entities = [PythonEntity.from_stella_entity(entity) for entity in event.entities]

        if not entities:
            raise StellaNowCLINoEntityAssociatedWithEventException()

        has_model_fields = any(field.is_model for field in fields)
        referenced_models = {
            f"{field.type}Model" if not field.type.endswith("Model") else field.type
            for field in fields
            if field.is_model
        }

        rendered = template.render(
            className=snake_to_camel(event.name),
            eventName=event.name,
            entities=entities,
            fields=fields,
            hasModelFields=has_model_fields,
            referencedModels=referenced_models,
            eventJson=json.dumps(event.model_dump(), indent=4),
            eventId=event.id,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            commentDef=cls.get_comments_def()
        )

        return rendered

    @classmethod
    def generate_model_class(
        cls, model: StellaModelDetailed, model_details: Dict[str, StellaModelDetailed], **kwargs
    ) -> str:
        template = PythonCodeGenerator.load_template(f"model")
        fields = [PythonField.from_stella_field(field, model_details) for field in model.fields.root]

        referenced_models = {
            f"{field.type}Model" if not field.type.endswith("Model") else field.type
            for field in fields
            if field.is_model
        }

        className = snake_to_camel(model.name)
        if not className.endswith("Model"):
            className += "Model"

        rendered = template.render(
            className=className,
            fields=fields,
            referencedModels=referenced_models,
            modelJson=json.dumps(model.model_dump(), indent=4),
            modelId=model.id,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            commentDef=cls.get_comments_def()
        )

        return rendered

    @staticmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        return f"{camel_to_snake(event_name)}_message.py"

    @staticmethod
    def get_file_name_for_model_name(model_name: str) -> str:
        return f"{camel_to_snake(model_name)}_model.py"

    @staticmethod
    def get_language() -> str:
        return StellaLanguage.PYTHON.value

    @classmethod
    def _get_diff(
        cls, generate_method, item, existing_code: str, model_details: Dict[str, StellaModelDetailed]
    ) -> List[str]:
        module_search = re.search(r"module_name\s*=\s*['\"](.+?)['\"]", existing_code)
        if module_search is None:
            raise StellaNowCLINamespaceNotFoundException()

        module_name = module_search.group(1)

        new_code = generate_method(item, model_details, module_name=module_name)

        existing_code_no_comments = remove_comments(existing_code)
        new_code_no_comments = remove_comments(new_code)

        diff = difflib.unified_diff(
            existing_code_no_comments.splitlines(keepends=True),
            new_code_no_comments.splitlines(keepends=True),
        )

        return [
            line
            for line in diff
            if line.startswith("- ") or line.startswith("+ ") and not (line.startswith("---") or line.startswith("+++"))
        ]

    @staticmethod
    def get_comments_def() -> CommentDefinition:
        return CommentDefinition()
