data = [20, -3, 7, -1, 0]

s = 0

for i, x in enumerate(data, 1):
    if x < 0:
        s += i

print(s)