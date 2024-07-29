"""
Позволяет запускать игры с помощью этого файла
"""
import importlib.util
import os

from app.decorators import cls_clear
from app.functions import show_get_menu

directory_with_games = 'games'


class CliApp:
    """Класс отвечает за взаимодействие с управлением приложением"""

    def __init__(self):
        self.games_manager = GamesManager()

    @cls_clear(time_to_sleep=1)
    def start(self, parameter=None):
        """
        Метод позволяет выбирать настройки самого приложения:
        Настройки представлены: dict с методами вызова настроек
        """
        parameters_list = [
            {"index": 1, "name": "Выбрать игру", "method": self.games_manager}
        ]

        if parameter is None:

            parameter = show_get_menu(len_parameters=len(parameters_list),
                                      list_to_show=parameters_list,
                                      menu_bio="\n\n\033[5;1mДобро пожаловать в меню программы, "
                                               "\nчем желаете заняться?\033[0m\n")
            self.start(parameter=parameter)

        else:
            method = [parameter_in_dict["method"]
                      for parameter_in_dict in parameters_list
                      if parameter_in_dict["index"] == parameter][0]
            getattr(method, "start")()


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
                    "name": filename[:-3],
                    "path": filepath,
                })

        return games_list

    @cls_clear(time_to_sleep=1)
    def start(self):

        game_index = show_get_menu(len_parameters=len(self.games_list),
                                   list_to_show=self.games_list,
                                   menu_bio="\n\n\033[5;1mВы перешли в меню выбора игры!\n\033[0m")
        self.start_game(game_index)

    @cls_clear(time_to_sleep=1)
    def start_game(self, game_index):

        game_file_path = [parameter_in_dict["path"]
                          for parameter_in_dict in self.games_list
                          if parameter_in_dict["index"] == game_index][0]
        game_name = [parameter_in_dict["name"]
                     for parameter_in_dict in self.games_list
                     if parameter_in_dict["index"] == game_index][0]

        def import_module_from_path(path):
            spec = importlib.util.spec_from_file_location("my_module", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module

        print(f"\033[5;1m\n\nЗапуск игры: {game_name}\033[0m")
        start = getattr(import_module_from_path(game_file_path), "start")
        start()


if __name__ == "__main__":
    client = CliApp()
    client.start()
