def sum_values_by_key(dictionary):
    """
    Суммирует значения по одинаковым ключам в словаре.
    param dictionary Входной словарь.
    return Словарь с суммой значений для каждого ключа.
    """
    if not isinstance(dictionary, dict):
        raise TypeError("Входные данные должны быть словарем.")

    result = {}
    for key, value in dictionary.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"Значение для ключа '{key}' не является числом.")
        if key in result:
            result[key] += value
        else:
            result[key] = value
    return result

def sum_keys_by_value(dictionary):
    """
    Суммирует ключи по одинаковым значениям в словаре.
    param dictionary Входной словарь.
    return Словарь с суммой ключей для каждого значения.
    """
    if not isinstance(dictionary, dict):
        raise TypeError("Входные данные должны быть словарем.")

    result = {}
    for key, value in dictionary.items():
        if not isinstance(key, (int, float)):
            raise ValueError(f"Ключ '{key}' не является числом.")
        if value in result:
            result[value] += key
        else:
            result[value] = key
    return result

def is_dict_valid_for_sum_values(dictionary):
    """
    Проверяет, что все значения в словаре являются числами.
    param dictionary Входной словарь.
    return True, если все значения — числа, иначе False.
    """
    if not isinstance(dictionary, dict):
        return False
    return all(isinstance(value, (int, float)) for value in dictionary.values())

def is_dict_valid_for_sum_keys(dictionary):
    """
    Проверяет, что все ключи в словаре являются числами.
    param dictionary Входной словарь.
    return True, если все ключи — числа, иначе False.
    """
    if not isinstance(dictionary, dict):
        return False
    return all(isinstance(key, (int, float)) for key in dictionary.keys())

def print_sum_results(dictionary, result, operation="сумма значений по ключам"):
    """
    Красиво выводит результат суммирования.
    param dictionary Исходный словарь.
    param result Результат суммирования.
    param operation Описание операции (по умолчанию "сумма значений по ключам").
    """
    print(f"Исходный словарь: {dictionary}")
    print(f"Результат ({operation}): {result}")


    # Проверка на корректность данных
    if is_dict_valid_for_sum_values(data):
        result = sum_values_by_key(data)
        print_sum_results(data, result, "сумма значений по ключам")
    else:
        print("Ошибка: не все значения в словаре являются числами.")

    if is_dict_valid_for_sum_keys(data):
        result = sum_keys_by_value(data)
        print_sum_results(data, result, "сумма ключей по значениям")
    else:
        print("Ошибка: не все ключи в словаре являются числами.")