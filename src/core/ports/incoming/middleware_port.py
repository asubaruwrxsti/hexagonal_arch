from abc import ABC, abstractmethod
from fastapi import FastAPI

class MiddlewarePort(ABC):
    @abstractmethod
    def register_middleware(self, app: FastAPI) -> None:
        """Register middleware with the FastAPI application"""
        pass