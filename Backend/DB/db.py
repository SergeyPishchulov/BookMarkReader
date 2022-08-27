from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from DB.models import Base, User
from config import DATABASE_URI
from sqlalchemy.orm.session import close_all_sessions


def recreate_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# Base.metadata.reflect()
# Base.metadata.tables['summary_inherited']('summary_inherited').add_is_dependent_on(summary)
# https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/

def get_session() -> Session:
    close_all_sessions()

    engine = create_engine(DATABASE_URI)

    # Base.metadata.create_all(engine)
    # Base.metadata.drop_all(engine)
    MSession = sessionmaker(bind=engine)

    recreate_database(engine)
    s = MSession()
    s.add(User(name="Ronaldo"))
    recv = s.query(User).filter_by(name="Ronaldo").first().name
    print(recv)
    s.commit()
    s.close()
    close_all_sessions()
    return s


get_session()
