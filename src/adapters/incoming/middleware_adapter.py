from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.ports.incoming.middleware_port import MiddlewarePort
from core.domain.response import APIResponse
import logging
import uuid

class FastAPIMiddlewareAdapter(MiddlewarePort):
    def register_middleware(self, app: FastAPI) -> None:
        # Configure CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
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
                error_response = APIResponse.error(
                    message=str(e)
                )
                return JSONResponse(
                    status_code=error_response.status_code,
                    content=error_response.dict()
                )