'''
Поиск элемента в упорядоченном списке
Дан отсортированный список чисел, например: [1, 2, 3, 45, 356, 569, 600, 705, 923]

Список может содержать миллионы элементов.

Необходимо написать функцию search(number: id) -> bool которая принимает число
number и возвращает True если это число находится в этом списке.

Требуемая сложность алгоритма O(log n).
'''


def search(numbers: list[int], target: int) -> bool:
    left, right = 0, len(numbers) - 1

    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return True
        if numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False


if __name__ == "__main__":
    numbers = [1, 2, 3, 45, 356, 569, 600, 705, 923]
    print(search(numbers, 356))
    print(search(numbers, 1000))
