# Эмулятор языка оболочки ОС  

Задание выполнено студенткой группы **ИКБО-61-23 Колосовой Светланой** в рамках курса **Конфигурационное управление**.

---

### Описание проекта  
Проект представляет собой эмулятор языка оболочки для UNIX-подобных систем. Эмулятор запускается из реальной командной строки, поддерживает работу с виртуальной файловой системой в формате zip и предоставляет графический интерфейс пользователя (GUI).  

### Функциональность  
1. **Команды оболочки**:  
   - `ls` — вывод содержимого текущей директории.  
   - `cd` — переход между директориями.  
   - `exit` — завершение сеанса работы.  
   - `mv` — перемещение или переименование файлов и директорий.  
   - `tail` — вывод последних строк файла.  
   - `du` — отображение размера файлов и директорий.  

2. **Конфигурационный файл**:  
   - Задает параметры запуска эмулятора.  

3. **Логирование**:  
   - Вся активность записывается в лог-файл в формате JSON.  

4. **Стартовый скрипт**:  
   - Автоматическое выполнение заданного списка команд при запуске.  

5. **Обработка ошибок**:  
   - Вывод сообщений об отсутствии обязательных аргументов или неправильной работе команд.  

6. **Тестирование**:  
   - Все функции покрыты тестами. Для каждой команды реализовано минимум три теста.  

---

### Установка и запуск  

#### Установка зависимостей  
Убедитесь, что у вас установлен Python версии 3.8+ и выполните:  
```bash
pip install -r requirements.txt
```

#### Запуск программы  
Для запуска эмулятора выполните следующую команду:  
```bash
python main.py <путь_к_конфигурационному_файлу>
```

Пример:  
```bash
python main.py ./config.json
```

Если конфигурационный файл не указан, программа выведет сообщение:  
```plaintext
Отсутствует необходимый аргумент: путь к конфигурационному файлу
```

---

### Форматы данных  

#### Конфигурационный файл  
Формат конфигурационного файла `JSON`. Пример:  
```json
{
    "fs_path": "my_zip_tes.zip",
    "log_path": "session_log.json",
    "startup_script_path": "startup_script.txt"
}
```
- `fs_path` — путь к zip-архиву с виртуальной файловой системой.  
- `log_path` — путь к файлу логов.  
- `startup_script_path` — путь к файлу стартового скрипта.  

#### Лог-файл  
Лог-файл записывает все команды, выполняемые в ходе сеанса работы. Пример содержимого:  
```json
[
    {"command": "cd user"},
    {"command": "ls"},
    {"command": "mv my.txt documents/"},
    {"command": "tail -5 log.txt"},
    {"command": "du ."},
    {"command": "cd /"},
    {"command": "ls"},
    {"command": "exit"}
]
```

#### Стартовый скрипт  
Стартовый скрипт содержит список команд, которые выполняются автоматически при запуске программы. Пример:  
```plaintext
cd user
ls
tail -5 secrets.txt
du .
cd /
ls
exit
```

---

### Зависимости  
Для работы эмулятора требуются следующие зависимости:  
```plaintext
colorama==0.4.6
coverage==7.6.1
iniconfig==2.0.0
packaging==24.1
pluggy==1.5.0
pytest==8.3.3
```

---

### Тестирование  
Для запуска тестов выполните:  
```bash
pytest
```
