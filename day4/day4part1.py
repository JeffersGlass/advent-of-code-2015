import hashlib

data = "ckczppom"

result = None
index = 0

while not result or not result.hexdigest().startswith("00000"):
    index += 1
    result = hashlib.md5((data + str(index)).encode())

print(f"At index {index}, the md5 hash starts with {result.hexdigest()[:15]}")

