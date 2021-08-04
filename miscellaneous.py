import random
from datetime import datetime


def get_password(password_length=6, by_chance=None) -> str:
    """
    Сгенерировать пароль пользователя по умолчанию.
    Если by_chance=True, то пароль - набор случайных символов, длинной password_length.
    Если by_chance=None, то пароль - текщий месяц, плюс год со строчной буквы, например, май2021.
    :return: Пароль пользователя
    """
    if by_chance:
        numbers = "1234567890"
        letters_lower = "abcdefghijklmnopqrstuvwxyz"
        letters_upper = letters_lower.upper()
        sequence = list(numbers + letters_lower + letters_upper)
        # Перемешать список
        random.shuffle(sequence)
        return "".join([random.choice(sequence) for _ in range(password_length)])
    else:
        list_of_months = ["январь", "февраль", "март", "апрель", "май", "июнь",
                          "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]
        date = datetime.now()
        month = date.month
        year = date.year
        return list_of_months[month - 1] + str(year)


def requisites_to_data(fio: str) -> tuple:
    """
    Преобразовать фамилию, имя и отчество в данные.
    Данные - фамилия, имя, отчество и имя директории упакованны в кортеж.
    Имя директории в формате Фамилия_ИО.
    :param fio: Фамилия, имя и отчество
    :return: Имя директории
    """
    surname, name, middle_name = [element.strip().capitalize() for element in fio.split()]
    return surname, name, middle_name, surname + "_" + name[0] + middle_name[0]
