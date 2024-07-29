import random
from app.functions import y_or_n_get
from app.decorators import cls_clear


class Board:
    def __init__(self):
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

    def check_win(self):
        """
        !!! Доступен лишь один победитель !!!
        Если кто-то победил: возвращает значение победителя.
        Если победителей нет: ничего не возвращает!
        """
        board = self.board
        # Проверка горизонталей и вертикалей
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i]
        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        # Игра продолжается
        return None

    def show(self):
        """
        Если есть победитель: выводит победителя
        Если нет победителя: выводит текущее поле
        """
        # Получение результата проверки
        win_result = self.check_win()
        # Если нет победителя
        if not win_result:
            # Формируется и выводиться поле, а так же ничего не возвращается
            print("\nТекущее поле:")
            for row_index, row in enumerate(self.board):
                s = ""
                for column_index, column in enumerate(row):
                    s += f"[{self.board[row_index][column_index]}]"
                print(s)
            return None
        # Если есть победитель он возвращается
        else:
            return win_result

    def add(self, value, x_or_o) -> bool:
        """
        Проверяет доступность ячейки:
        1. Если есть возможность изменить поля: изменяет
        2. Если нет возможности изменить поле: не изменяет
        """
        if self.board[value // 3][value % 3] == " ":
            self.board[value // 3][value % 3] = x_or_o.upper()
            return True
        else:
            return False


class TicTacToe:
    def __init__(self):
        self.x_or_o = None
        self.board = Board()

    @cls_clear(time_to_sleep=1)
    def x_or_y_get(self):
        """
        Получает значение, которым собирается играть пользователь.
        Если введённое значение не является правильным: выводит ошибку и перезапускает механизм.
        """
        # Получение значения
        x_or_o = input("\nКем вы хотите играть? (X/O)\n").lower()
        # Если значение не равно O или X
        if x_or_o not in ["o", "x"]:
            # Выводит ошибку
            print("Вы ввели не допустимое значение!")
            # Перезапускает механизм
            self.x_or_y_get()
        # Если значение не равно O или X
        else:
            # Присваивает классу значение
            self.x_or_o = x_or_o
            # Запускает первый шаг
            self.step()

    @cls_clear(time_to_sleep=1)
    def step(self):
        """
        Создаёт новый ход:
        Если есть победитель: выводит его
        Если нет победителя выводит поле
        """
        # Попытка получить значение победителя
        winner_value = self.board.show()
        # Если победителя нет
        if not winner_value:
            # Получается значение ячейки в которую собирается добавиться знак
            value = int(input("\nВведите поле куда хотите поставить знак (от 1 до 9): "))
            # Если значения поля в допустимом радиусе
            if value in range(1, 10):
                # Перевожу в index-значение
                status_user_board_add = self.board.add(value - 1, self.x_or_o)
                # Если добавить получилось
                if status_user_board_add:
                    # Устанавливается
                    status_program_board_add = False
                    bot_value = 0
                    while not status_program_board_add:
                        x_or_o = "x" if self.x_or_o == "o" else "o"
                        bot_value = random.randint(1, 9) - 1
                        status_program_board_add = self.board.add(value=bot_value, x_or_o=x_or_o)
                    print(f"Программы выбрала ячейку {bot_value}")
                    # Начинает новый шаг
                    self.step()
                # Если добавить не получилось
                else:
                    # Выводит ошибку
                    print("Данная ячейка уже занята")
                    # Начинает шаг заново
                    self.step()

            # Если значение не допустимо
            else:
                print("Вы ввели не допустимое значение!")
        else:
            print("\n", winner_value, "выигрывает")

            answer = y_or_n_get(question="\nХотите сыграть ещё? (Y/N)\n")
            if answer == "y":
                self.board.board = [
                    [" ", " ", " "],
                    [" ", " ", " "],
                    [" ", " ", " "]
                ]
                self.x_or_y_get()
            elif answer == "n":
                answer = y_or_n_get(question="\nЖелаете выбрать другую игру? (Y/N)\n")
                if answer == "y":
                    from main import GamesManager
                    games = GamesManager()
                    games.start()
                elif answer == "n":
                    @cls_clear(time_to_sleep=1)
                    def print_exit():
                        print(f"\nСпасибо что был со мной!")

                    print_exit()


def start():
    game = TicTacToe()
    game.x_or_y_get()


if __name__ == "__main__":
    start()
