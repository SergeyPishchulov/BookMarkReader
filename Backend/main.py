import pathlib
import uvicorn
from fastapi import FastAPI, APIRouter, Depends, Request, responses, status
from starlette.staticfiles import StaticFiles
from api.bookmarks import bookmark_router
from api.books import book_router
from services import Services, get_services
import mimetypes

mimetypes.init()
app = FastAPI()
mimetypes.add_type('application/javascript', '.js')
services = get_services()

app.include_router(book_router)
app.include_router(bookmark_router)


@app.get("/")
async def index(request: Request):
    return responses.RedirectResponse(
        '/static/index.html',
        status_code=status.HTTP_302_FOUND)


app.mount(f"/fs", StaticFiles(directory=f"{pathlib.Path(__file__).parent.resolve()}/FileStorage"),
          name="fs")
app.mount(f"/static", StaticFiles(directory=f"{pathlib.Path(__file__).parent.parent.resolve()}/Frontend/static"),
          name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
