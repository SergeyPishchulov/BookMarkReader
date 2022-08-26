from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User

from config import DATABASE_URI
from sqlalchemy.orm.session import close_all_sessions


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


close_all_sessions()

engine = create_engine(DATABASE_URI)

# Base.metadata.create_all(engine)
# Base.metadata.drop_all(engine)
Session = sessionmaker(bind=engine)

recreate_database()
s = Session()
u = User()
s.add(u)
s.add(User())
s.commit()
s.close()
close_all_sessions()
