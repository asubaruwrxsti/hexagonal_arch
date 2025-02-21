from flask import Flask
import os
import importlib

app = Flask(__name__)

# Set static folder
app.static_folder = 'public'

# Register routes
routes_folder = os.path.join(os.path.dirname(__file__), 'routes')
for filename in os.listdir(routes_folder):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'routes.{filename[:-3]}'
        module = importlib.import_module(module_name)

        found_blueprint = False
        try:
            for attr_name in ['blueprint', filename[:-3] + '_bp']:
                if hasattr(module, attr_name):
                    app.register_blueprint(getattr(module, attr_name))
                    print(f"Registered blueprint: {module_name} with {attr_name}")
                    found_blueprint = True
                    break
                    
            if not found_blueprint:
                print(f"WARNING: No blueprint found in {module_name}")
        except Exception as e:
            print(f"ERROR: {e}")

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
                    
                    middleware_instance = attr()
                    middleware_instance.register(app)
                    print(f"Registered middleware: {module_name}.{attr_name}")
                    found_middleware = True
            
            if not found_middleware:
                print(f"WARNING: No middleware found in {module_name}")
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    app.run()