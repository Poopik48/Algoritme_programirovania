data = [float(x) for x in input("Введите числа через пробел: ").split()]

s = 0

for i, x in enumerate(data, start=1):
    if x < 0:
        s += i

print(f"Сумма индексов отрицательных чисел: {s}")