# Copyright (c) 2021-2025, Abilian SAS

from __future__ import annotations

import inspect
from pathlib import Path
from typing import TYPE_CHECKING

from flask import current_app

from .lib.names import to_snake_case

if TYPE_CHECKING:
    from jinja2 import Environment, Template


def get_template(obj) -> Template:
    if template := get_template_from_attribute(obj):
        return template

    return get_template_from_file(obj)


def get_template_from_attribute(obj) -> Template | None:
    template = getattr(obj, "template", None)
    if template is None:
        return None

    jinja_env: Environment = current_app.jinja_env
    return jinja_env.from_string(template)


def get_template_from_file(obj) -> Template:
    template_name = to_snake_case(obj.__class__.__name__) + ".html"
    cls = obj.__class__.__mro__[0]
    template_file = Path(inspect.getfile(cls)).parent / template_name
    jinja_env: Environment = current_app.jinja_env
    return jinja_env.from_string(template_file.read_text())
