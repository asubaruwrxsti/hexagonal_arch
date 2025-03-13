from typing import Optional
from core.domain.models import User
from core.ports.repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(model=User, session=session)

    def find_by_email(self, email: str) -> Optional[User]:
        return self.session.query(self.model).filter(self.model.email == email).first()
    
    def create_with_email_check(self, user_data):
        """Create a new user after checking if email is unique"""
        existing_user = self.find_by_email(user_data.email)
        if existing_user:
            return False, "User with that email already exists"
        
        user = self.create(user_data)
        return True, user
        
    def create(self, user_data):
        user = User(
            name=user_data.name,
            email=user_data.email,
        )
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user