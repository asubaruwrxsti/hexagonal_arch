from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from core.ports.incoming.middleware_port import MiddlewarePort
from adapters.incoming.auth_middleware import AuthMiddleware
from core.domain.response import APIResponse
import logging
import uuid
from core.config import get_settings

settings = get_settings()

class FastAPIMiddlewareAdapter(MiddlewarePort):
    def register_middleware(self, app: FastAPI) -> None:
        # Configure CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_CREDENTIALS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        )

        # Add request ID middleware
        @app.middleware("http")
        async def add_request_id(request: Request, call_next):
            request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
            response = await call_next(request)
            if response and hasattr(response, 'headers'):
                response.headers["X-Request-ID"] = request_id
            return response

        # Add error handling middleware
        @app.middleware("http")
        async def error_handler(request: Request, call_next):
            try:
                response = await call_next(request)
                return response
            except Exception as e:
                logging.exception("Unhandled exception occurred")
                return APIResponse.error(
                    message=str(e)
                )
            
        # Add auth middleware
        @app.middleware("http")
        async def auth_middleware(request: Request, call_next):
            auth_middleware = AuthMiddleware(app)
            return await auth_middleware.dispatch(request, call_next)
