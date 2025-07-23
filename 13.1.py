import random

def generate_matrix(rows, cols):
    """Генерирует матрицу заданного размера со случайными числами от -100 до 100"""
    return [[random.randint(-100, 100) for _ in range(cols)] for _ in range(rows)]

def add_matrices(matrix_1, matrix_2):
    """Складывает две матрицы одинаковой размерности"""
    if len(matrix_1) != len(matrix_2) or len(matrix_1[0]) != len(matrix_2[0]):
        raise ValueError("Матрицы должны быть одинакового размера")
    return [
        [matrix_1[i][j] + matrix_2[i][j] for j in range(len(matrix_1[0]))]
        for i in range(len(matrix_1))
    ]

def print_matrix(matrix):
    """Выводит матрицу в удобочитаемом формате"""
    for row in matrix:
        print(row)

# Пример использования:
rows = 10
cols = 10

# Генерация двух случайных матриц 10x10
matrix_1 = generate_matrix(rows, cols)
matrix_2 = generate_matrix(rows, cols)

print("Матрица 1:")
print_matrix(matrix_1)
print("\nМатрица 2:")
print_matrix(matrix_2)

# Сложение матриц
matrix_3 = add_matrices(matrix_1, matrix_2)
print("\nРезультат сложения (Матрица 3):")
print_matrix(matrix_3)