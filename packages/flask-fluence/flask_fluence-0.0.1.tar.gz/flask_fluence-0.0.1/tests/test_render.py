from flask import Flask

from flask_fluence.render import render_component


def test_render_static():
    class Hello:
        template = "Hello world!"

    obj = Hello()

    app = Flask(__name__)
    with app.app_context():
        result = render_component(obj)
        assert result == "Hello world!"
