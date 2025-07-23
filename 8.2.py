N = int(input())
arr = list(map(int, input().split()))
new_arr = [arr[-1]] + arr[:-1]
print(' '.join(map(str, new_arr)))