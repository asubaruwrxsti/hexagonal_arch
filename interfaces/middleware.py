class Middleware:
    def register(self, app):
        raise NotImplementedError("Subclasses must implement the register method")