import collections

pets = {
    1: {
        "Мухтар": {
            "Вид питомца": "Собака",
            "Возраст питомца": 9,
            "Имя владельца": "Павел"
        }
    },
    2: {
        "Каа": {
            "Вид питомца": "желторотый питон",
            "Возраст питомца": 19,
            "Имя владельца": "Саша"
        }
    }
}

def get_suffix(age):
    if age % 10 == 1 and age % 100 != 11:
        return "год"
    elif 2 <= age % 10 <= 4 and (age % 100 < 10 or age % 100 >= 20):
        return "года"
    else:
        return "лет"

def get_pet(ID):
    return pets[ID] if ID in pets.keys() else False

def pets_list():
    for ID, pet_info in pets.items():
        pet_name = list(pet_info.keys())[0]
        pet_data = pet_info[pet_name]
        age = pet_data["Возраст питомца"]
        suffix = get_suffix(age)
        print(f'ID: {ID}, Питомец: {pet_name}, Вид: {pet_data["Вид питомца"]}, Возраст: {age} {suffix}, Владелец: {pet_data["Имя владельца"]}')

def create():
    if pets:
        last = collections.deque(pets, maxlen=1)[0]
        new_id = last + 1
    else:
        new_id = 1
    pet_name = input("Введите имя питомца: ")
    pet_type = input("Введите вид питомца: ")
    age = int(input("Введите возраст питомца: "))
    owner = input("Введите имя владельца: ")
    pets[new_id] = {
        pet_name: {
            "Вид питомца": pet_type,
            "Возраст питомца": age,
            "Имя владельца": owner
        }
    }
    print(f"Добавлен новый питомец с ID {new_id}")

def read(ID):
    pet_info = get_pet(ID)
    if pet_info:
        pet_name = list(pet_info.keys())[0]
        pet_data = pet_info[pet_name]
        age = pet_data["Возраст питомца"]
        suffix = get_suffix(age)
        print(f'Это {pet_data["Вид питомца"]} по кличке "{pet_name}". Возраст питомца: {age} {suffix}. Имя владельца: {pet_data["Имя владельца"]}')
    else:
        print("Питомец с таким ID не найден")

def update(ID):
    pet_info = get_pet(ID)
    if pet_info:
        pet_name = list(pet_info.keys())[0]
        print(f"Текущая информация о питомце {pet_name}: {pet_info[pet_name]}")
        pet_type = input("Введите новый вид питомца (оставьте пустым, чтобы не изменять): ")
        age = input("Введите новый возраст питомца (оставьте пустым, чтобы не изменять): ")
        owner = input("Введите новое имя владельца (оставьте пустым, чтобы не изменять): ")
        if pet_type:
            pet_info[pet_name]["Вид питомца"] = pet_type
        if age:
            pet_info[pet_name]["Возраст питомца"] = int(age)
        if owner:
            pet_info[pet_name]["Имя владельца"] = owner
        print("Информация обновлена")
    else:
        print("Питомец с таким ID не найден")

def delete(ID):
    if ID in pets.keys():
        del pets[ID]
        print(f"Питомец с ID {ID} удален")
    else:
        print("Питомец с таким ID не найден")

# Основной цикл программы
command = ""
while command != "stop":
    print("\nДоступные команды: create, read, update, delete, list, stop")
    command = input("Введите команду: ").lower()
    if command == "create":
        create()
    elif command == "read":
        ID = int(input("Введите ID питомца: "))
        read(ID)
    elif command == "update":
        ID = int(input("Введите ID питомца: "))
        update(ID)
    elif command == "delete":
        ID = int(input("Введите ID питомца: "))
        delete(ID)
    elif command == "list":
        pets_list()
    elif command == "stop":
        print("Работа программы завершена")
    else:
        print("Неизвестная команда")