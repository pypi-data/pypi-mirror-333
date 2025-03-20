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
from pathlib import Path
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader, Template
from stellanow_api_internals.datatypes.workflow_mgmt import StellaEventDetailed, StellaModelDetailed

from stellanow_cli.code_generators.common.types import CommentDefinition
from stellanow_cli.core.utils.string_utils import camel_to_snake, snake_to_camel


class CodeGenerator(ABC):
    def __init__(self):
        self.env = self._create_jinja_environment()

    @classmethod
    def _create_jinja_environment(cls) -> Environment:
        current_file_path = Path(__file__).parent
        language_templates_path = current_file_path / f"../{cls.get_language()}/templates"
        shared_templates_path = current_file_path / "templates"  # Shared templates directory

        env = Environment(
            loader=FileSystemLoader([language_templates_path, shared_templates_path]),
            extensions=["jinja2.ext.do"]
        )
        env.filters["camel_to_snake"] = camel_to_snake
        env.filters["snake_to_camel"] = snake_to_camel
        return env

    @classmethod
    def load_template(cls, template_name: str) -> Template:
        env = cls._create_jinja_environment()
        return env.get_template(f"{template_name}.template")

    @classmethod
    def get_message_diff(
        cls, event: StellaEventDetailed, existing_code: str, model_details: Dict[str, StellaModelDetailed]
    ) -> List[str]:
        return cls._get_diff(cls.generate_message_class, event, existing_code, model_details)

    @classmethod
    def get_model_diff(
        cls, model: StellaModelDetailed, existing_code: str, models_details: Dict[str, StellaModelDetailed]
    ) -> List[str]:
        return cls._get_diff(cls.generate_model_class, model, existing_code, models_details)

    @classmethod
    @abstractmethod
    def generate_message_class(
        cls, event: StellaEventDetailed, model_details: Dict[str, StellaModelDetailed], **kwargs
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    def generate_model_class(
        cls, model: StellaModelDetailed, model_details: Dict[str, StellaModelDetailed], **kwargs
    ) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_file_name_for_event_name(event_name: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_file_name_for_model_name(model_name: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_language() -> str:
        pass

    @classmethod
    @abstractmethod
    def _get_diff(
        cls, generate_method, item, existing_code: str, model_details: Dict[str, StellaModelDetailed]
    ) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_comments_def() -> CommentDefinition:
        pass
