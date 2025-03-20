from os import listdir
from os.path import join, dirname
from flask import Flask
from importlib import import_module
from flask.blueprints import Blueprint
from .callback_middleware import CallbackMiddleware
from .http.router_middleware import RouterMiddleware as Router

class BlueprintMiddleware:
    def __init__(self, app: Flask, path: str) -> None:
        self.app = app
        self.path = path

        # load routes defined from users
        routes_folder = join(dirname(dirname(dirname(__file__))), self.path, 'routes')
        for filename in listdir(routes_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f"app.routes.{filename[:-3]}"
                import_module(module_name)

    def register(self):
        for route in Router._method_route().items():
            controller_name = route[0]
            blueprint = Blueprint(controller_name, controller_name)

            obj = import_module(f"{self.path}.controllers.{controller_name}_controller")
            view_func = getattr(obj, f"{controller_name.title()}Controller")
            instance_controller = view_func()

            CallbackMiddleware(self.app, controller_name, instance_controller).register()

            for resource in route[1]:
                blueprint.add_url_rule(
                    rule=resource.path,
                    endpoint=resource.action,
                    view_func=getattr(instance_controller, resource.action),
                    methods=resource.method,
                )

            self.app.register_blueprint(blueprint)
