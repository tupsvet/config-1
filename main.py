import json
from zipfile import ZipFile
from sys import argv
from os.path import exists
from window_mode import Window
from terminal import MyTerminal


def main():
    if len(argv) > 1:
        config_file = argv[1]
    else:
        print("Отсутствует необходимый аргумент: путь к конфигурационному файлу")
        return

    if exists(config_file):
        with open(config_file) as config_file_obj:
            config = json.load(config_file_obj)
            fs_path = config['fs_path']
            log_path = config['log_path']
            startup_script_path = config['startup_script_path']
    else:
        print("Конфигурационный файл с таким названием отсутствует")
        return

    if exists(fs_path):
        with ZipFile(fs_path, 'a') as file_system:
            terminal = MyTerminal(file_system, log_path)
            terminal.run_startup_script(startup_script_path)
            if len(argv) > 2 and argv[2] == '-cli':
                terminal.start_polling()
            else:
                window = Window(terminal)
                window.start_polling()
    else:
        print("Модель файловой системы с таким названием отсутствует")
        return


if __name__ == '__main__':
    main()
