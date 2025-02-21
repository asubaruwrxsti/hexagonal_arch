from fastapi import FastAPI
from adapters.incoming.route_adapter import FastAPIRouteAdapter
from adapters.incoming.middleware_adapter import FastAPIMiddlewareAdapter
import yaml
from pathlib import Path

def create_app() -> FastAPI:
    app = FastAPI()
    
    # Initialize adapters
    route_adapter = FastAPIRouteAdapter()
    middleware_adapter = FastAPIMiddlewareAdapter()
    
    # Register routes and middleware
    route_adapter.register_routes(app)
    middleware_adapter.register_middleware(app)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    config_path = Path(__file__).parent.parent / "uvicorn.yaml"

    with open(config_path) as f:
        config = yaml.safe_load(f)

    config.pop('app', None)
    uvicorn.run("main:app", **config)