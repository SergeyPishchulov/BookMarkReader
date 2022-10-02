from typing import List

from bookmarkdto import BookmarkDto
# from main import Services
from . import router
from fastapi import Depends, APIRouter

bookmark_router = APIRouter()


@bookmark_router.get("/bookmarks", response_model=List[BookmarkDto])
async def get_bookmarks():
    # user = services.user_repo.get_default_user()
    # bkmks_orms = services.bookmark_repo.get_bookmarks_by_user(user)
    # print(bkmks_orms[0])
    # return bkmks_orms
    return 1
    # return [BookmarkDto.from_orm(x) for x in bkmks_orms]
