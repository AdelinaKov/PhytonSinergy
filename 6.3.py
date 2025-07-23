A = int(input())
B = int(input())
result = []
for num in range(A, B + 1):
    if num % 2 == 0:
        result.append(str(num))
print(' '.join(result))