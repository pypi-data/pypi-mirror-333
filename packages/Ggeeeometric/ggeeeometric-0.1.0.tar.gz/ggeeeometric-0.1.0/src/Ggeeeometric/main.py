def generate_geometric_progression(n, first_term, ratio):
    """
    n Количество элементов в прогрессии.
    first_term Первый элеменент.
    ratio Шаг (знаменатель).
    """
    progression = [first_term * (ratio ** i) for i in range(n)]
    return progression

def sum_geometric_progression(n, first_term, ratio):
    # Вычисляет сумму геометрической прогрессии.

    if ratio == 1:
        return n * first_term
    else:
        return first_term * (1 - ratio ** n) / (1 - ratio)

def nth_term_of_geometric_progression(n, first_term, ratio):
    # Находит n-й член геометрической прогрессии.
    return first_term * (ratio ** n)

def is_geometric_progression(sequence):
    """
    Проверяет, является ли последовательность геометрической прогрессией.

    :sequence: Последовательность чисел.
    """
    if len(sequence) < 2:
        return False
    ratio = sequence[1] / sequence[0]
    for i in range(1, len(sequence)):
        if sequence[i] / sequence[i-1] != ratio:
            return False
    return True

def print_geometric_progression(progression, title="Геометрическая прогрессия"):
    """
    Красиво выводит геометрическую прогрессию.

    :progression: Список элементов прогрессии.
    :title: Заголовок
    """
    print(f"{title}: [", end="")
    print(", ".join(map(str, progression)), end="")
    print("]")

