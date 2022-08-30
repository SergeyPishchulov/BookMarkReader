import hashlib


def md5(fname)-> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# print(md5('main2.py'))
# print(md5('main.py'))
