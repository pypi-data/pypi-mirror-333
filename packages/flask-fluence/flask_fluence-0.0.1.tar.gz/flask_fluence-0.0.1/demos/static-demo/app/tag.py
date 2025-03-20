from jinja2_simple_tags import ContainerTag

from flask_fluence import render_component


class ComponentTag(ContainerTag):
    tags = {"component"}

    def render(self, component_name, **kwargs):
        return render_component(component_name, **kwargs)
