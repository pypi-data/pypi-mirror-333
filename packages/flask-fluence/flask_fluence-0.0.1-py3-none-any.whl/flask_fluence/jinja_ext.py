from jinja2_simple_tags import ContainerTag

from flask_fluence import render_component


class ComponentTag(ContainerTag):
    tags = {"component"}  # noqa: RUF012

    def render(self, component_name, **kwargs):  # noqa: PLR6301
        return render_component(component_name, **kwargs)
