my_dict = {}

for num in range(10, -6, -1):
    my_dict[num] = num ** num

for key, value in my_dict.items():
    print(f"{key}: {value}")