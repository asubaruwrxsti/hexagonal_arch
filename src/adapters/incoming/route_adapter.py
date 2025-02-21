from fastapi import FastAPI, APIRouter
from core.ports.incoming.router_port import RouterPort
import os
import importlib

class FastAPIRouteAdapter(RouterPort):
    def __init__(self):
        self.routes_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'routes')
        if not os.path.exists(self.routes_path):
            os.makedirs(self.routes_path)

    def register_routes(self, app: FastAPI) -> None:
        if not os.path.exists(self.routes_path):
            return
            
        for filename in os.listdir(self.routes_path):
            if filename.endswith('.py') and filename != '__init__.py':
                module_name = f'routes.{filename[:-3]}'
                self._register_module(app, module_name)

    def _register_module(self, app: FastAPI, module_name: str) -> None:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'router') and isinstance(module.router, APIRouter):
                app.include_router(module.router)
        except ImportError as e:
            print(f"Error importing module {module_name}: {str(e)}")