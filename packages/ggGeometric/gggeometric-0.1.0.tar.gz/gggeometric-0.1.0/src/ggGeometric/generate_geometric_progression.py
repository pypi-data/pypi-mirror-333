def generate_geometric_progression(n, first_term, ratio):
    """
    Генерирует геометрическую прогрессию.

    :n: Количество элементов в прогрессии.
    :first_term: Первый элемент прогрессии.
    :ratio: Шаг (знаменатель) прогрессии.
    """
    progression = [first_term * (ratio ** i) for i in range(n)]
    return progression