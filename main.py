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
        if hasattr(module, 'blueprint'):
            app.register_blueprint(getattr(module, 'blueprint'))
            print(f"Registered blueprint: {module_name}")
        print(f"Checked: {module_name}")
    print(f"Ended: {filename}")

# Register middleware
middleware_folder = os.path.join(os.path.dirname(__file__), 'middleware')
for filename in os.listdir(middleware_folder):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'middleware.{filename[:-3]}'
        module = importlib.import_module(module_name)
        if hasattr(module, 'register'):
            module.register(app)
            print(f"Registered middleware: {module_name}")
        print(f"Checked: {module_name}")
    print(f"Ended: {filename}")

if __name__ == "__main__":
    app.run()