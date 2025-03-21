# Task_3_Collection_Framework_Task_4_CLI

---

# Завдання (Task_3_Collection_Framework):

Написати програму, яка приймає рядок і повертає кількість символів в рядку, які 
трапляються лише раз. Очікується, що рядок з однією такою ж послідовністю символів 
може бути переданий методу декілька раз. Оскільки операція підрахунку може зайняти
багато часу, метод повинен кешувати результати, так що, коли методу буде наданий 
рядок, який трапився раніше, він просто витягне збережений результат.

Вимоги:

 - використання модуля collections для підрахунку символів
 - використання методу для кешування результатів
 - використання map() для підрахунку унікальних символів
 - тестування через pytest
 - використaти для покриття коду пакет coverage 5.1

# Завдання (Task_4_CLI):

 - додати інтерфейс командного рядка до Task_3_Collection_Framework, використовуючи стандартний бібліотечний модуль
 - додати функціонал для обробки текстового файлу. Програма повинна мати два параметри --string або --file.
Наприклад:
python collect_framework.py --string “your string”
python collect_framework.py --file path_to_text_file
якщо передано два параметри, параметр '--file' повинен мати вищий пріоритет - значить рядок слід ігнорувати
python collect_framework.py --string “your string” --file path_to_text_file

Тести повинні мати моки для читання файлу та роботи з переданими параметрами.

# Завдання (Task_5_Packaging):

Конвертувати попередній проект із task 3-4 в пакет python. Додати README.md та описати як використовувати цей пакет.
Для корректного встановлення додати відсутнє зіставлення шляху до файлу pyproject.toml   


# MY_COLLECTION

# Опис
Python-пакет для обробки тексту, включаючи підрахунок унікальних символів, 
підтримує обробку даних черех командний рядок

# Встановлення
встанови пакет за допомогою pip з PyPi(https://pypi.org):

"bash" - pip install my-collection

# Використання
1 - після встановлення пакету можна використовувати його як CLI-інструмент
- для обробки текстового рядка:
"bash" - my-collection --string "This is a test"
- для обробки текстового файлу:
"bash" - my-collection --file path/text.txt
- 
Аргумент --file має вищий пріоритет над --string, якщо передані обидва.
Якщо не передати жодного аргументу, програма завершиться з помилкою.

2 - використання у Python-коді

from my_collection import unique_char_count

text = "example text"

result = unique_char_count(text)

print(f"Unique character count: {result")

# Документація
для перегляду вбудованої документації:

1 - відкрий Python-інтерпретатор:
"bash" - python

2 - імпортуй функцію та використовуй help():

from my_collection import unique_char_count

help(unique_char_count)

# Приклади
1 - підрахунок унікальних символів у рядку

from my_collection import unique_char_count

print(unique_char_count("abbbccdf")) # виведе 3

2 - використання CLI
"bash" - my-collection --string "abbbccdf" # виведе Unique character count: 3

# Оновлення пакету
Для оновлення пакету до останньої версії

"bash" - pip install --upgrade my-collection

# Тестування
Використовується Pytest для запуску тестів. Для виконання:

1 - клонувати репозиторій
"bash" - cd task-5-packaging

         git clone https://git.foxminded.ua/liliia-shpytsia-mentoring/task-5-packaging.git 

2 - встановити залежності для розробки:
"bash" - pip install -r requirements.txt

3 - запустити тести:
"bash" - pytest

# Структура проекту

![Опис зображення](images/screenshot.png)

# Ліцензія
Цей проєкт ліцензовано за умовами [MIT License] 
(https://git.foxminded.ua/liliia-shpytsia-mentoring/task-5-packaging/-/blob/dev/LICENSE)

# Пошук проблем
Якщо виникли проблеми, створи Issue на Gitlab
[Створити Issue] (https://git.foxminded.ua/liliia-shpytsia-mentoring/task-5-packaging/-/issues) 
або напиши коментар
