from app.decorators import cls_clear


@cls_clear(time_to_sleep=1)
def y_or_n_get(question) -> str:
    """
    Используется для получения ответа
    """

    def print_not_correct_value(answer=None):
        if answer:
            print(answer)
        else:
            print("Вы ввели неверное значение!")

    parameter_index: str = input(question).lower()
    if parameter_index in ["y", "n"]:
        return parameter_index
    else:
        print_not_correct_value(answer=f"\nОтвет может быть только X или Y")


def get_parameter_index(len_parameters: int):
    """
    Используется получения числа из возможного списка.
    """

    def print_not_correct_value(text=None):
        if text:
            print(text)
        else:
            print("Вы ввели неверное значение!")

    parameter_index: str = input(f"\nВведите номер параметра от {1} до {len_parameters}: ")
    try:
        parameter_index: int = int(parameter_index)
        if parameter_index in range(1, len_parameters + 1):
            return parameter_index
        else:
            print_not_correct_value(text=f"\nНомер параметра  может быть только от {1} до {len_parameters}")
            get_parameter_index(len_parameters=len_parameters)

    except:
        print_not_correct_value()
        get_parameter_index(len_parameters=len_parameters)


def show_parameters(list_to_show: list, menu_bio: str = None):
    """
    Использует для вывода заголовка меню и списка его параметров
    """
    try:
        dict_to_show = {parameter_dict["index"]: parameter_dict["name"] for parameter_dict in list_to_show}
        print(menu_bio)
        for index, name in dict_to_show.items():
            print(f"{index}: {name}")

    except:
        print("В параметрах нет index или name")


@cls_clear(time_to_sleep=1)
def show_get_menu(len_parameters: int, list_to_show: list, menu_bio: str) -> int:
    show_parameters(list_to_show=list_to_show, menu_bio=menu_bio)
    return get_parameter_index(len_parameters=len_parameters)
