# Copyright (c) 2021-2025, Abilian SAS

from __future__ import annotations

from .component import Component, component
from .render import render_component
from .templates import get_template

__all__ = ["Component", "component", "get_template", "render_component"]
