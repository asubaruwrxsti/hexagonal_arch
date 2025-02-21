from abc import ABC, abstractmethod
from fastapi import FastAPI

class RouterPort(ABC):
    @abstractmethod
    def register_routes(self, app: FastAPI) -> None:
        pass