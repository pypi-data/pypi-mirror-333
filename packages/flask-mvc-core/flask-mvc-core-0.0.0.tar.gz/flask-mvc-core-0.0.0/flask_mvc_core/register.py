import importlib
import sys
from os.path import dirname, join
from os import listdir

_registered_routes = []

def register(func):
    """Decorador para registrar rotas automaticamente."""
    _registered_routes.append(func)
    return func

class Register:
    @staticmethod
    def routes(app):
        """Carrega automaticamente todas as rotas registradas."""
        route_dir = join(dirname(dirname(dirname(__file__))), "routes")
        if route_dir not in sys.path:
            sys.path.append(route_dir)

        # Carregar todos os módulos de rotas automaticamente
        for filename in listdir(route_dir):
            if filename.endswith(".py") and filename not in ["__init__.py", "register.py"]:
                module_name = f"routes.{filename[:-3]}"
                
                try:
                    importlib.import_module(module_name)
                except Exception as e:
                    print(f"Erro ao carregar {module_name}: {e}")

        for func in _registered_routes:
            func(app)
