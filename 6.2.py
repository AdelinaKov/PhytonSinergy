X = int(input())
count = 0
sqrt_X = int(X ** 0.5)
for i in range(1, sqrt_X + 1):
    if X % i == 0:
        if i * i == X:
            count += 1
        else:
            count += 2
print(count)