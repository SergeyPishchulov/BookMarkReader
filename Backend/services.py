import logging

from DB.BookMarkRepo import BookMarkRepo
from DB.BookRepo import BookRepo
from DB.UserRepo import UserRepo
from sqlalchemy.orm.session import Session


class Services:
    def __init__(self, s: Session):
        self.book_repo = BookRepo(s)
        self.user_repo = UserRepo(s)
        self.bookmark_repo = BookMarkRepo(s)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        # fh = logging.FileHandler(filename='./Logs/server.log', mode='w')  # DELETE in the begining
        formatter = logging.Formatter(
            "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        # fh.setFormatter(formatter)
        logger.addHandler(ch)  # Exporting logs to the screen
        # logger.addHandler(fh)  # Exporting logs to a file
        self.logger = logger
