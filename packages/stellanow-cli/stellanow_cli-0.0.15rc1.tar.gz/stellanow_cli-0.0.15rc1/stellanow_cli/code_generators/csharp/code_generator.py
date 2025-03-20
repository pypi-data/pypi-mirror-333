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
from stellanow_cli.code_generators.csharp.dataclass import CommentDefinition, CSharpEntity, CSharpField
from stellanow_cli.core.enums import StellaLanguage
from stellanow_cli.core.utils.string_utils import remove_comments, snake_to_camel
from stellanow_cli.exceptions.cli_exceptions import (
    StellaNowCLINamespaceNotFoundException,
    StellaNowCLINoEntityAssociatedWithEventException,
)


class CsharpCodeGenerator(CodeGenerator):
    @classmethod
    def generate_message_class(
        cls, event: StellaEventDetailed, model_details: Dict[str, StellaModelDetailed], **kwargs
    ) -> str:
        template = CsharpCodeGenerator.load_template(f"message")

        namespace = kwargs.get("namespace", "StellaNowSDK.Messages")

        fields = [CSharpField.from_stella_field(field=field, model_details=model_details) for field in event.fields]
        entities = [CSharpEntity.from_stella_field(entity) for entity in event.entities]

        if not entities:
            raise StellaNowCLINoEntityAssociatedWithEventException()

        has_model_fields = any(field.is_model for field in fields)

        rendered = template.render(
            className=snake_to_camel(event.name),
            eventName=event.name,
            constructorArguments=", ".join(
                [
                    ", ".join([entity.to_constructor_parameter_declaration() for entity in entities]),
                    ", ".join([field.to_constructor_parameter_declaration() for field in fields]),
                ]
            ),
            entitiesList=", ".join([entity.to_entity_type_declaration() for entity in entities]),
            entities=entities,
            fields=fields,
            namespace=namespace,
            hasModelFields=has_model_fields,
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
        template = CsharpCodeGenerator.load_template(f"model")

        namespace = kwargs.get("namespace", "StellaNowSDK.Messages")

        fields = [
            CSharpField.from_stella_field(field=field, model_details=model_details) for field in model.fields.root
        ]

        rendered = template.render(
            className=snake_to_camel(model.name),
            fields=fields,
            namespace=namespace,
            modelJson=json.dumps(model.model_dump(), indent=4),
            modelId=model.id,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            commentDef=cls.get_comments_def()
        )

        return rendered

    @staticmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        return f"{snake_to_camel(event_name)}Message.cs"

    @staticmethod
    def get_file_name_for_model_name(model_name: str) -> str:
        return f"{snake_to_camel(model_name)}Model.cs"

    @staticmethod
    def get_language() -> str:
        return StellaLanguage.CSHARP.value

    @classmethod
    def _get_diff(
        cls, generate_method, item, existing_code: str, models_details: Dict[str, StellaModelDetailed]
    ) -> List[str]:
        namespace_search = re.search(r"namespace (.*);", existing_code)
        if namespace_search is None:
            raise StellaNowCLINamespaceNotFoundException()

        namespace = namespace_search.group(1)

        new_code = generate_method(item, models_details, namespace=namespace)

        existing_code_no_comments = remove_comments(existing_code)
        new_code_no_comments = remove_comments(new_code)

        diff = difflib.unified_diff(
            existing_code_no_comments.splitlines(keepends=True), new_code_no_comments.splitlines(keepends=True)
        )

        return [
            line
            for line in diff
            if line.startswith("- ") or line.startswith("+ ") and not (line.startswith("---") or line.startswith("+++"))
        ]

    @staticmethod
    def get_comments_def() -> CommentDefinition:
        return CommentDefinition()
