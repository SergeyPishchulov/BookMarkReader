from sqlalchemy.orm.session import Session
from typing import Optional
from DB.models import User, BookFile, Book


class UserRepo:
    def __init__(self, s: Session):
        self.s = s

    def get_default_user(self) -> Optional[User]:
        return self.s.query(User).filter_by(name="Ronaldo").first()
