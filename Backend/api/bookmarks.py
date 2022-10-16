from typing import List

from bookmarkdto import BookmarkDto
from services import Services, get_services
from fastapi import Depends, APIRouter

bookmark_router = APIRouter(prefix="/api")


@bookmark_router.get("/bookmarks", response_model=List[BookmarkDto])
async def get_bookmarks(services: Services = Depends(get_services)):
    user = services.user_repo.get_default_user()
    bkmks_orms = services.bookmark_repo.get_bookmarks_by_user(user)
    # print(bkmks_orms[0])
    return bkmks_orms
