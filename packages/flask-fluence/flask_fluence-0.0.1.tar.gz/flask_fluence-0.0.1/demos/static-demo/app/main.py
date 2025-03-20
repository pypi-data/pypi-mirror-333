from __future__ import annotations

from flask import Flask, render_template
from flask_super import scan_package

from flask_fluence import render_component
from flask_fluence.jinja_ext import ComponentTag

scan_package("app")


def create_app() -> Flask:
    app = Flask(__name__)

    app.jinja_env.add_extension(ComponentTag)

    @app.context_processor
    def inject_component_renderer():
        return dict(component=render_component)

    @app.get("/")
    def index():
        return render_template("index.html")

    return app


def make_context(obj, kwargs):
    # Injects all class attributes and instance attributes into the context
    # This needs to be more carefully controlled in a real application
    ctx = {**vars(obj)}
    for k, v in vars(obj.__class__).items():
        ctx[k] = getattr(obj, k)
    ctx = {**ctx, **kwargs}
    return ctx
