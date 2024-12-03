import hashlib

data = "ckczppom"

result = None
index = 0

while not result or not result.hexdigest().startswith("000000"): #5 zeroes for part 1, 6 for part 2
    index += 1
    result = hashlib.md5((data + str(index)).encode())

print(f"At index {index}, the md5 hash starts with {result.hexdigest()[:15]}")

