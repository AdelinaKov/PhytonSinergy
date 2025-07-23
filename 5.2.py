word = input("Введите слово из маленьких латинских букв: ").lower()

vowels = {'a', 'e', 'i', 'o', 'u'}
vowel_count = 0
consonant_count = 0
vowel_stats = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

for letter in word:
    if letter in vowels:
        vowel_count += 1
        vowel_stats[letter] += 1
    else:
        consonant_count += 1

print(f"Гласных букв: {vowel_count}")
print(f"Согласных букв: {consonant_count}")

# Проверяем, есть ли все гласные
all_vowels_present = all(vowel_stats[v] > 0 for v in vowels)
if not all_vowels_present:
    print("False")
else:
    print("Все гласные присутствуют")