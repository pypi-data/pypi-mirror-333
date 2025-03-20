from abc import ABC
from typing import Optional, Any
from flask import Flask, render_template

class Controller(ABC):
    _app: Flask = Flask(__name__)

    def __init__(self):
        self._app.config['DEBUG'] = False

    def render(self, view: str, **args: Optional[Any]) -> str:
        return render_template(f"{view}.html", **args)
