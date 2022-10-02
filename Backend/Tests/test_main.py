import os
import shutil

from fastapi.testclient import TestClient

from main_old import app

client = TestClient(app)


def test_main_200():
    response = client.get("/")
    assert response.status_code == 200


def test_book_is_achievable_after_creating():
    file_name = 'example_for_testing.txt'
    with open(f"TestFileSource/{file_name}", "rb") as f:
        response_on_creat = client.post("/books", files={"files": (file_name, f)})
    assert response_on_creat.status_code == 200
    created = response_on_creat.json()
    response = client.get(f"/books/{created['id']}")
    assert response.status_code == 200
    got = response.json()
    assert got['id'] == created['id']


def test_2_books_with_same_file_are_different():
    "Expected different book ids, but same content"
    file_name = 'example_for_testing.txt'
    with open(f"TestFileSource/{file_name}", "rb") as f:
        created1 = client.post("/books", files={"files": (file_name, f)}).json()
    with open(f"TestFileSource/{file_name}", "rb") as f:
        created2 = client.post("/books", files={"files": (file_name, f)}).json()
    got1 = client.get(f"/books/{created1['id']}").json()
    got2 = client.get(f"/books/{created2['id']}").json()

    assert got1['id'] != got2['id']
    assert got1['content'] == got2['content']


def test_books_with_eq_names_and_diff_files_are_different():
    file_name = 'example_for_testing.txt'
    with open(f"TestFileSource/{file_name}", "rb") as f:
        created1 = client.post("/books", files={"files": (file_name, f)}).json()
    with open(f"TestFileSource/{file_name}", 'a') as f:
        f.write("EXTRA")
    with open(f"TestFileSource/{file_name}", "rb") as f:
        created2 = client.post("/books", files={"files": (file_name, f)}).json()

    got1 = client.get(f"/books/{created1['id']}").json()
    got2 = client.get(f"/books/{created2['id']}").json()

    print(got1)
    print(got2)

    # assert got1['id'] != got2['id']
    # assert got1['content'] != got2['content']
