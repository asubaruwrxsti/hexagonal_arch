from fastapi import FastAPI
from adapters.incoming.route_adapter import FastAPIRouteAdapter
from adapters.incoming.middleware_adapter import FastAPIMiddlewareAdapter

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
    uvicorn.run(app, host="0.0.0.0", port=8000)