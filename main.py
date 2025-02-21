from fastapi import FastAPI
import os
import importlib

app = FastAPI()

# Register routes
routes_folder = os.path.join(os.path.dirname(__file__), 'routes')
for filename in os.listdir(routes_folder):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'routes.{filename[:-3]}'
        module = importlib.import_module(module_name)

        found_router = False
        try:
            for attr_name in ['router', filename[:-3] + '_router']:
                if hasattr(module, attr_name):
                    app.include_router(getattr(module, attr_name))
                    print(f"Registered router: {module_name} with {attr_name}")
                    found_router = True
                    break
        except Exception as e:
            print(f"ERROR: {e}")

        if not found_router:
            print(f"WARNING: No router found in {module_name}!")

# Register middleware
middleware_folder = os.path.join(os.path.dirname(__file__), 'middleware')
for filename in os.listdir(middleware_folder):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'middleware.{filename[:-3]}'
        module = importlib.import_module(module_name)

        found_middleware = False
        try:
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    attr.__module__ == module.__name__ and 
                    hasattr(attr, 'register')):
                    
                    middleware_instance = attr(app)
                    middleware_instance.register(app)
                    print(f"Registered middleware: {module_name}.{attr_name}")
                    found_middleware = True
        except Exception as e:
            print(f"ERROR: {e}")

        if not found_middleware:
            print(f"WARNING: No middleware found in {module_name}!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)