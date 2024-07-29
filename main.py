"""
Позволяет запускать игры с помощью этого файла
"""
import importlib.util
import os

directory_with_games = 'games'


class CliApp:
    """Класс отвечает за взаимодействие с управлением приложением"""

    def __init__(self):
        self.games_manager = GamesManager()

    def start(self, parameter=None):
        """
        Метод позволяет выбирать настройки самого приложения:
        Настройки представлены: dict с методами вызова настроек
        """
        parameters_dict = [
            {"index": 1, "name": "Выбрать игру", "method": self.games_manager}
        ]

        if parameter is None:
            os.system('cls||clear')
            print("\n\nДобро пожаловать в меню программы, "
                  "\nчем желаете заняться?")

            print()
            for parameter in parameters_dict:
                print(f"{parameter["index"]}: {parameter["name"]}")

            def parameter_get():
                print()
                parameter = int(input(f"Введите номер параметра (от {1} до {len(parameters_dict)}): "))
                if parameter in range(1, len(parameters_dict) + 1):
                    return parameter
                else:
                    print("Было введено неверное значение!")
                    parameter_get()

            parameter = parameter_get()
            self.start(parameter=parameter)

        else:
            method = [parameter_in_dict["method"]
                      for parameter_in_dict in parameters_dict
                      if parameter_in_dict["index"] == parameter][0]
            start = getattr(method, "start")
            start()


class GamesManager:
    def __init__(self):

        self.games_list = self.get_games_dict()

    @staticmethod
    def get_games_dict() -> dict:
        games_list = list()
        for filename in os.listdir(directory_with_games):
            filepath = os.path.join(directory_with_games, filename)
            if os.path.isfile(filepath):
                games_list.append({
                    "index": len(games_list) + 1,
                    "file_name": filename,
                    "file_path": filepath,
                })

        return games_list

    def start(self):
        os.system('cls||clear')
        print("\n\nВы перешли в меню выбора игры!\n")

        for game in self.games_list:
            print(f"{game["index"]}: {game["file_name"][:-3]}")

        def game_index_get():
            print()
            game_number = int(input(f"Введите номер игры, которую желаете запустить"
                                    f"\n(от {1} до {len(self.games_list)}): "))
            if game_number in range(1, len(self.games_list) + 1):
                return game_number
            else:
                print("Было введено неверное значение!")
                game_index_get()

        game_index = game_index_get()
        self.start_game(game_index)

    def start_game(self, game_index):

        game_file_path = [parameter_in_dict["file_path"]
                          for parameter_in_dict in self.games_list
                          if parameter_in_dict["index"] == game_index][0]
        game_name = [parameter_in_dict["file_name"]
                     for parameter_in_dict in self.games_list
                     if parameter_in_dict["index"] == game_index][0][:-3]

        def import_module_from_path(path):
            spec = importlib.util.spec_from_file_location("my_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        os.system('cls||clear')
        print(f"\n\nЗапуск игры: {game_name}")
        start = getattr(import_module_from_path(game_file_path), "start")
        start()


if __name__ == "__main__":
    client = CliApp()
    client.start()
