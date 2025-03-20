from .templates import get_template


def render_component(obj, **kwargs):
    template = get_template(obj)
    return template.render(this=obj, **kwargs)
