n = int(input())
list1 = [int(input()) for _ in range(n)]
m = int(input())
list2 = [int(input()) for _ in range(m)]

set1 = set(list1)
set2 = set(list2)
common = set1 & set2  # или set1.intersection(set2)
print(len(common))