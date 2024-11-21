import os
import json
from zipfile import ZipFile
from window_mode import Window
import posixpath
import io


class MyTerminal:
    def __init__(self, file_system: ZipFile, log_path):
        self.fs = file_system
        self.cur_d = ''
        self.polling = False
        self.window = None
        self.log_path = log_path
        self.log_actions = []

    def attach(self, window: Window):
        self.window = window
        self.window.write(f'user:~{self.cur_d}$ ')

    def output(self, message, end='\n'):
        if self.window is None:
            print(message, end=end)
        else:
            self.window.write(message + end)

    def start_polling(self):
        self.polling = True
        try:
            while self.polling:
                message = f'user:~{self.cur_d}$ '
                enter = input(message).strip()
                if len(enter) > 0:
                    self.command_dispatcher(enter)
        finally:
            self.write_log()
            self.output('stop polling...')

    def stop_polling(self):
        self.polling = False
        self.write_log()
        self.output('stop polling...')

    def write_log(self):
        with open(self.log_path, 'w', encoding='utf-8') as log_file:
            json.dump(self.log_actions, log_file, ensure_ascii=False, indent=4)

    def run_startup_script(self, startup_script_path):
        if os.path.exists(startup_script_path):
            with open(startup_script_path, 'r', encoding='utf-8') as script_file:
                commands = script_file.readlines()
            for cmd in commands:
                cmd = cmd.strip()
                if cmd:
                    self.command_dispatcher(cmd)
        else:
            self.output('Стартовый скрипт не найден')

    def command_dispatcher(self, command):
        if self.window is not None:
            self.output(command)

        self.log_actions.append({'command': command})

        params = command.split()
        if len(params) == 0:
            return

        if params[0] == 'exit':
            if self.window is None:
                self.polling = False
            else:
                self.window.stop_polling()
                return
        elif params[0] == 'cd':
            temp_dir = self.cd(params[1:])
            if temp_dir is not None:
                self.cur_d = temp_dir
        elif params[0] == 'ls':
            self.output(self.ls(params[1:]))
        elif params[0] == 'mv':
            result = self.mv(params[1:])
            if result:
                self.output(result)
        elif params[0] == 'tail':
            self.output(self.tail(params[1:]))
        elif params[0] == 'du':
            self.output(self.du(params[1:]))
        else:
            self.output("Команда не найдена")

        if self.window is not None:
            self.output(f'user:~{self.cur_d}$ ', end='')

    def cd(self, params):
        if len(params) == 0:
            return ''
        directory = params[-1]

        if directory.startswith('/'):
            new_path = posixpath.normpath(directory)
        else:
            new_path = posixpath.normpath(posixpath.join(self.cur_d, directory))

        if new_path in ('.', '/'):
            new_path = ''
        elif new_path != '':
            new_path += '/'

        for file in self.fs.namelist():
            if file.startswith(new_path):
                return new_path
        self.output('Директория с таким названием отсутствует')

    def ls(self, params):
        work_directory = self.cur_d
        if len(params) > 0:
            temp_dir = self.cd((params[-1],))
            if temp_dir is not None:
                work_directory = temp_dir
            else:
                return ''

        files = set()
        for file in self.fs.namelist():
            if file.startswith(work_directory):
                ls_name = file[len(work_directory):]
                if '/' in ls_name:
                    ls_name = ls_name[:ls_name.index('/')]
                files.add(ls_name)
        return '\n'.join(sorted(filter(lambda x: len(x) > 0, files)))

    def mv(self, params):
        if len(params) != 2:
            return 'Usage: mv source destination'

        source = posixpath.join(self.cur_d, params[0])
        destination = posixpath.join(self.cur_d, params[1])

        source = posixpath.normpath(source)
        destination = posixpath.normpath(destination)

        if source not in self.fs.namelist():
            return 'Source file not found'

        if any(file == destination + '/' for file in self.fs.namelist()):
            dest_filename = destination + '/' + posixpath.basename(source)
        else:
            dest_filename = destination

        self.rename_in_zip(source, dest_filename)
        return ''

    def rename_in_zip(self, source_filename, dest_filename):
        with ZipFile(self.fs.filename, 'r') as zip_read:
            zip_buffer = io.BytesIO()
            with ZipFile(zip_buffer, 'w') as zip_write:
                for item in zip_read.infolist():
                    data = zip_read.read(item.filename)
                    if item.filename == source_filename:
                        item.filename = dest_filename
                    zip_write.writestr(item, data)
            with open(self.fs.filename, 'wb') as f:
                f.write(zip_buffer.getvalue())
        self.fs = ZipFile(self.fs.filename, 'a')

    def tail(self, params):
        if len(params) == 0:
            return 'Usage: tail [-n] filename'

        n = 10
        file = params[-1]

        if len(params) > 1 and params[0].startswith('-'):
            try:
                n = int(params[0][1:])
            except:
                return 'Invalid flag, defaulting to last 10 lines'

        filename = posixpath.normpath(posixpath.join(self.cur_d, file))

        try:
            with self.fs.open(filename, 'r') as read_file:
                data = read_file.read().decode('UTF-8').split('\n')
                return '\n'.join(data[-n:])
        except:
            return 'Invalid file name'

    def du(self, params):
        path = self.cur_d
        if len(params) > 0:
            path_candidate = self.cd((params[-1],))
            if path_candidate is not None:
                path = path_candidate
            else:
                return 'Invalid directory'

        total_size = 0
        for file in self.fs.namelist():
            if file.startswith(path):
                info = self.fs.getinfo(file)
                total_size += info.file_size
        return f'Total size: {total_size} bytes'
