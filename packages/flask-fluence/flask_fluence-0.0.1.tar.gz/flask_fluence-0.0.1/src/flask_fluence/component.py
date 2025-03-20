from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


class Component:
    template: str | None = None
    render: Callable | None = None


def component(cls: type) -> type:
    return cls
