funcs = []

for i in range(10):
    funcs.append(lambda x: x * i)

for j in range(10):
    print(funcs[j](5))