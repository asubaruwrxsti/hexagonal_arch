from typing import Generic, Type, TypeVar, List, Optional
from sqlalchemy.orm import Session
from core.domain.models import Base

T = TypeVar('T', bound=Base) # type: ignore

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get(self, id: int) -> Optional[T]:
        return self.session.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[T]:
        return self.session.query(self.model).all()

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: int) -> None:
        obj = self.get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()