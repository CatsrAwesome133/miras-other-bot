import random as r
for i in range(10):
    print(r.random())

print(any (i in "hello there" for i in ["hello", "abc"]))