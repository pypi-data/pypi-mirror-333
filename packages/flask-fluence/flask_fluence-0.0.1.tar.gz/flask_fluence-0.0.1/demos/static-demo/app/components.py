from flask_fluence import Component, component

__all__ = []


@component
class HelloWorld(Component):
    template = """
    <div class="border rounded p-3">
        Hello World!
    </div>
    """
