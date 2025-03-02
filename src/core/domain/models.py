from sqlalchemy import Column, Integer, String
from src.adapters.outgoing.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"

    def __repr__(self):
        return str(self)