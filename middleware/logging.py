from flask import request
from interfaces.middleware import Middleware as BaseMiddleware

class LoggingMiddleware(BaseMiddleware):
    def log_request_response(self, app):
        @app.before_request
        def log_request():
            app.logger.info(f"Request: {request.method} {request.url}")

        @app.after_request
        def log_response(response):
            app.logger.info(f"Response: {response.status}")
            return response

    def register(self, app):
        self.log_request_response(app)