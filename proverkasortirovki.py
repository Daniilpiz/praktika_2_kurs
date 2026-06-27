#!/usr/bin/env python3
"""
Binary Tree Sort с меню, загрузкой из data.txt,
обязательным сравнением с sorted() и сравнением на наборах 1K, 10K, 100K.
"""

import sys
import os
import time
import random

class TreeNode:
    """Узел бинарного дерева поиска."""
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    """Вставка ключа в BST. Возвращает корень дерева."""
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

def inorder_traversal(root, sorted_list):
    """Симметричный обход: заполняет список отсортированными ключами."""
    if root is not None:
        inorder_traversal(root.left, sorted_list)
        sorted_list.append(root.key)
        inorder_traversal(root.right, sorted_list)

def binary_tree_sort(arr):
    """Сортировка массива через BST. Возвращает отсортированный список."""
    if not arr:
        return []
    root = None
    for item in arr:
        root = insert(root, item)
    result = []
    inorder_traversal(root, result)
    return result

def read_numbers_from_file():
    """Чтение чисел из файла. Enter → data.txt в папке скрипта."""
    filepath = input("Введите путь к файлу (Enter — data.txt в папке скрипта): ").strip()
    if not filepath:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, "data.txt")
        print(f"Используется файл по умолчанию: {filepath}")

    numbers = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                for token in line.split():
                    try:
                        num = float(token)
                        if num == int(num):
                            numbers.append(int(num))
                        else:
                            numbers.append(num)
                    except ValueError:
                        print(f"Предупреждение: пропущено нечисловое значение: '{token}'", file=sys.stderr)
        if not numbers:
            print(f"Ошибка: файл '{filepath}' не содержит чисел.")
            return None
        return numbers
    except FileNotFoundError:
        print(f"Ошибка: файл '{filepath}' не найден.")
        return None
    except PermissionError:
        print(f"Ошибка: нет прав для чтения файла '{filepath}'.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}.")
        return None

def manual_input():
    """Ручной ввод чисел через терминал."""
    print("\nВведите числа через пробел или по одному в строке.")
    print("Для завершения ввода нажмите Enter на пустой строке.\n")
    numbers = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            if numbers:
                break
            else:
                print("Вы ещё не ввели ни одного числа. Введите числа или нажмите Ctrl+C для выхода.")
                continue
        for token in line.split():
            try:
                num = float(token)
                numbers.append(int(num) if num == int(num) else num)
            except ValueError:
                print(f"Предупреждение: '{token}' — не число, пропущено.", file=sys.stderr)
    return numbers

def compare_sorts(data, show_array=True):
    """
    Сравнивает Binary Tree Sort и встроенную sorted() по времени и корректности.
    Если show_array=True, выводит полный отсортированный массив.
    """
    if not data:
        return
    
    data_copy = data[:]
    start = time.perf_counter()
    sorted_bt = binary_tree_sort(data_copy)
    bt_time = time.perf_counter() - start
    
    start = time.perf_counter()
    sorted_builtin = sorted(data)
    builtin_time = time.perf_counter() - start
    
    correct = (sorted_bt == sorted_builtin)
    
    print("\n" + "=" * 50)
    print("         Сравнение сортировок")
    print("=" * 50)
    print(f"Размер массива: {len(data)} элементов")
    print(f"Binary Tree Sort: {bt_time:.6f} сек")
    print(f"Встроенная sorted(): {builtin_time:.6f} сек")
    if correct:
        print("Результаты совпадают — сортировка выполнена верно.")
    else:
        print("ОШИБКА: результаты не совпадают!")
    print("-" * 50)
    if show_array:
        print("Отсортированный массив (полностью):")
        print(sorted_bt)
        print("-" * 50)

def compare_multiple_sizes():
    """Сравнение на наборах 1K, 10K, 100K чисел."""
    print("\n--- Сравнение на наборах разного размера ---")
    min_val = input("Минимальное значение (Enter = 0): ").strip()
    max_val = input("Максимальное значение (Enter = 99999): ").strip()
    
    min_val = int(min_val) if min_val else 0
    max_val = int(max_val) if max_val else 99999
    if min_val > max_val:
        min_val, max_val = max_val, min_val
    
    sizes = [1000, 10000, 100000, 1000000]  # 1K, 10K, 100K, 1M
    for size in sizes:
        print(f"\n>>> Генерация массива из {size} чисел...")
        data = [random.randint(min_val, max_val) for _ in range(size)]
        compare_sorts(data, show_array=False)  # без вывода массива
        print()

def write_output(numbers):
    """Запись отсортированных чисел в файл или вывод в консоль (полностью)."""
    print("\nСохранить результат в файл?")
    print("1. Да")
    print("2. Нет (вывести в консоль)")
    while True:
        choice = input("Ваш выбор (1/2): ").strip()
        if choice == '1':
            while True:
                filepath = input("Введите путь для сохранения (Enter — sorted_output.txt в папке скрипта): ").strip()
                if not filepath:
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    filepath = os.path.join(script_dir, "sorted_output.txt")
                    print(f"Путь не указан. Файл будет создан как '{filepath}'")
                try:
                    with open(filepath, 'w') as f:
                        for num in numbers:
                            f.write(f"{num}\n")
                    print(f"Результат успешно записан в '{filepath}' ({len(numbers)} чисел).")
                    return
                except PermissionError:
                    print(f"Ошибка: нет прав для записи в '{filepath}'. Попробуйте снова.")
                except Exception as e:
                    print(f"Ошибка при записи файла: {e}. Попробуйте снова.")
        elif choice == '2':
            print(f"\nОтсортированный массив ({len(numbers)} элементов):")
            print(numbers)
            return
        else:
            print("Неверный выбор. Введите 1 или 2.")

def show_menu():
    """Главное меню."""
    print("\n" + "=" * 50)
    print("           Binary Tree Sort")
    print("=" * 50)
    print("1. Загрузить числа из файла")
    print("2. Ввести числа вручную")
    print("3. Генерация случайных чисел")
    print("4. Выход")
    print("=" * 50)

def main():
    while True:
        show_menu()
        choice = input("Ваш выбор (1/2/3/4): ").strip()
        
        if choice == '1':
            print("\n--- Загрузка из файла ---")
            data = read_numbers_from_file()
            if data is None:
                continue
            print(f"\nИсходный массив ({len(data)} элементов):")
            print(data)
            sorted_data = binary_tree_sort(data)
            write_output(sorted_data)
            print("\nСравнение с встроенной сортировкой (sorted)...")
            compare_sorts(data, show_array=True)
            input("\nНажмите Enter для возврата в меню...")
            
        elif choice == '2':
            print("\n--- Ручной ввод ---")
            data = manual_input()
            if not data:
                print("Ошибка: нет данных для сортировки.")
                continue
            print(f"\nИсходный массив ({len(data)} элементов):")
            print(data)
            sorted_data = binary_tree_sort(data)
            write_output(sorted_data)
            print("\nСравнение с встроенной сортировкой (sorted)...")
            compare_sorts(data, show_array=True)
            input("\nНажмите Enter для возврата в меню...")
            
        elif choice == '3':
            compare_multiple_sizes()
            input("\nНажмите Enter для возврата в меню...")
            
        elif choice == '4':
            print("До свидания!")
            sys.exit(0)
        else:
            print("Неверный выбор. Введите 1, 2, 3 или 4.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)