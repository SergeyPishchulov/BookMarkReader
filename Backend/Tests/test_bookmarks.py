import random
import string

from fastapi.testclient import TestClient

from bookmarkdto import BookmarkDto
from main import app

client = TestClient(app)


def test_bookmark_is_achievable_after_creating():
    file_name = 'example_for_testing.txt'
    with open(f"TestFileSource/{file_name}", "rb") as f:
        book = client.post("/books", files={"files": (file_name, f)}).json()
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
    dto = BookmarkDto(book_id=book['id'],
                      quote=random_string,
                      comment="C")
    cr_response = client.post(f'/books/{book["id"]}/bookmarks', dto.json())
    bkmks_by_book = client.get(f"books/{book['id']}/bookmarks").json()
    assert any(d['quote'] == dto.quote for d in bkmks_by_book)
    all_bkmks = client.get(f"/bookmarks").json()
    print("^" * 10)
    print(all_bkmks)
    assert any(d['quote'] == dto.quote for d in all_bkmks)
