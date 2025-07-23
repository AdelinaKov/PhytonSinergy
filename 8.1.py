N = int(input())
numbers = [int(input()) for _ in range(N)]
print('\n'.join(map(str, reversed(numbers))))