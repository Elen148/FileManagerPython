import os
import json
import sys
import xml.etree.ElementTree as ET
import zipfile
import psutil

invalid_chars = ['"', "<", ">", "|", "/", "\\", "?", "*", ":", ","]
file_name = ""
path = ""
dir_path = r"D:\WorkWithFiles" #директория, в которую будут сохраняться созданные файлы

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
    print(f"Директория '{dir_path}' создана")
zip_path = ""


def main():
    menu()


def check_file_name(extension=""):
    global file_name, path
    if extension:
        print(f"Введите имя файла с расширением '{extension}'")
    else:
        print("Введите имя файла с расширением")

    file_name = input()
    path = os.path.join(dir_path, file_name)

    # Проверка на недопустимые символы
    while any(char in file_name for char in invalid_chars):
        print("Ошибка! В названии файла недопустимые символы")
        file_name = input()
        path = os.path.join(dir_path, file_name)

    # Проверка на существование файла
    while os.path.exists(path):
        print("Файл с таким именем уже существует, введите другое имя файла")
        file_name = input()
        path = os.path.join(dir_path, file_name)


def check_file_exists(extension=""):
    global file_name, path
    if extension:
        print(f"Введите имя файла с расширением '{extension}'")
    else:
        print("Введите имя файла с расширением")

    file_name = input()
    path = os.path.join(dir_path, file_name)

    return os.path.exists(path)


items = [1, 2, 3, 4, 5, 6]


def menu(task=0):
    if task == 0:
        print("Выберите действие из приведенного списка:")
        print("1 - Посмотреть информацию о дисках")
        print("2 - Работа с файлами")
        print("3 - Работа с форматом JSON")
        print("4 - Работа с форматом XML")
        print("5 - Работа с архивами")
        print("6 - Выход")

        try:
            task = int(input("Введите номер действия: "))
        except ValueError:
            print("Ошибка! Некорректный ввод")
            menu()
            return

        if task not in items:
            print("Введённый номер действия не существует, выберите действие повторно")
            menu()
        else:
            print()
            menu(task)

    elif task == 1:
        print("Информация о дисках:")

        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"Название: {partition.device}")
            print(f"Метка: {partition.mountpoint}")
            print(f"Тип файловой системы: {partition.fstype}")


            try:
                usage = psutil.disk_usage(partition.mountpoint)
                print(f"Объем диска: {usage.total / (1024 ** 3):.2f} ГБ")
                print(f"Свободное пространство: {usage.free / (1024 ** 3):.2f} ГБ")
            except PermissionError:
                print("Нет доступа к информации о диске")
            print()

        menu()

    elif task == 2:
        print("Выберите действие из приведенного списка:")
        print("1 - Создать файл")
        print("2 - Записать в файл строку")
        print("3 - Прочитать файл в консоль")
        print("4 - Удалить файл")
        print("5 - Главное меню")

        try:
            file_task = int(input("Введите номер действия: "))
        except ValueError:
            print("Ошибка! Некорректный ввод")
            menu(2)
            return

        print()

        if file_task in items:
            if file_task == 5:
                menu()
            else:
                work_with_files(file_task)

        else:
            print("Введённый номер действия не существует, выберите действие повторно")
            menu(2)

    elif task == 3:
        print("Выберите действие из приведенного списка:")
        print("1 - Создать файл в формате JSON")
        print("2 - Создать новый объект. Его сериализация в JSON и запись в файл")
        print("3 - Прочитать файл в консоль")
        print("4 - Удалить файл")
        print("5 - Главное меню")

        try:
            json_task = int(input("Введите номер действия: "))
        except ValueError:
            print("Ошибка! Некорректный ввод")
            menu(3)
            return

        print()

        if json_task in items:
            if json_task == 5:
                menu()
            else:
                work_with_json(json_task)
        else:
            print("Введённый номер действия не существует, выберите действие повторно")
            menu(3)

    elif task == 4:
        print("Выберите действие из приведенного списка:")
        print("1 - Создать файл в формате XML")
        print("2 - Записать в файл новые данные")
        print("3 - Прочитать файл в консоль")
        print("4 - Удалить файл")
        print("5 - Главное меню")

        try:
            xml_task = int(input("Введите номер действия: "))
        except ValueError:
            print("Ошибка! Некорректный ввод")
            menu(4)
            return

        print()

        if xml_task in items:
            if xml_task == 5:
                menu()
            else:
                work_with_xml(xml_task)
        else:
            print("Введённый номер действия не существует, выберите действие повторно.")
            menu(4)

    elif task == 5:
        print("Выберите действие из приведенного списка:")
        print("1 - Создать архив в формате zip")
        print("2 - Добавить файл в архив")
        print("3 - Разархивировать файл и вывести данные о нём")
        print("4 - Удалить файл и архив")
        print("5 - Главное меню")

        try:
            archive_task = int(input("Введите номер действия: "))
        except ValueError:
            print("Ошибка! Некорректный ввод")
            menu(5)
            return

        print()

        if archive_task in items:
            if archive_task == 5:
                menu()
            else:
                work_with_archives(archive_task)
        else:
            print("Введённый номер действия не существует, выберите действие повторно")
            menu(5)

    elif task == 6:
        sys.exit()

    else:
        print("Неверный код задания")
        print()
        menu()


def work_with_files(file_task):
    global path, file_name

    if file_task == 1:  # Создаем новый файл
        check_file_name()
        with open(path, 'x') as f:
            pass
        print(f"Файл '{file_name}' создан по следующему пути: {path}")
        print()
        menu(2)

    elif file_task == 2:  # Записываем что-то в файл
        while not check_file_exists():
            print("Файла с таким именем не существует")

        print("Введите строку для записи в файл:")
        text = input()
        try:
            with open(path, 'a') as f:  # 'a' открывает файл для добавления
                f.write(text + '\n')
            print(f"Текст записан в файл '{file_name}'")
        except Exception as e:
            print(e)

        print()
        menu(2)

    elif file_task == 3:  # Вывод информации из файла
        while not check_file_exists():
            print("Файла с таким именем не существует")

        try:
            with open(path, 'r') as f:  # 'r' открывает файл для чтения
                print(f"Текст из файла '{file_name}': ")
                for line in f:
                    print(line.strip())
        except Exception as e:
            print(e)

        print()
        menu(2)

    elif file_task == 4:  # Удаление файла
        while not check_file_exists():
            print("Файла с таким именем не существует")

        try:
            os.remove(path)
            print(f"Файл '{file_name}' был удалён по следующему пути: {path}")
        except Exception as e:
            print(e)

        print()
        menu(2)


def work_with_json(file_task):
    global path, file_name

    if file_task == 1:  # Создаем JSON-файл
        while True:
            check_file_name("json")
            if not file_name.endswith('.json'):
                print("Файл имеет отличное расширение от JSON")
            else:
                break

        with open(path, 'w') as f:
            json.dump({}, f)
        print(f"Пустой JSON-файл '{file_name}' успешно создан")
        print()
        menu(3)

    elif file_task == 2:  # Создание и запись объекта в JSON
        while not check_file_exists("json"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.json'):
                print("Файл имеет отличное расширение от JSON")
                while not check_file_exists("json"):
                    print("Файла с таким именем не существует")
            else:
                break

        objects_list = []

        while True:
            obj = {}
            print("Создаём новый объект")
            while True:
                key = input("Введите ключ: ")
                value = input("Введите значение: ")
                obj[key] = value
                add_more = input("Добавить ещё ключ-значение в этот объект? (да/нет): ").lower()
                if add_more != 'да':
                    break

            objects_list.append(obj)

            create_another = input("Создать новый объект? (да/нет): ").lower()
            if create_another != 'да':
                break

        with open(path, 'w') as f:
            json.dump(objects_list, f, indent=4)

        print(f"Данные записаны в файл: {file_name}")
        print()
        menu(3)

    elif file_task == 3:  # Чтение JSON
        while not check_file_exists("json"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.json'):
                print("Файл имеет отличное расширение от JSON")
                while not check_file_exists("json"):
                    print("Файла с таким именем не существует")
            else:
                break

        with open(path, 'r') as f:
            deserialized_objects = json.load(f)
            for obj in deserialized_objects:
                print("\nОбъект:")
                for key, value in obj.items():
                    print(f"{key}: {value}")

        print()
        menu(3)

    elif file_task == 4:  # Удаление JSON-файла
        while not check_file_exists("json"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.json'):
                print("Файл имеет отличное расширение от JSON")
                while not check_file_exists("json"):
                    print("Файла с таким именем не существует")
            else:
                break

        try:
            os.remove(path)
            print(f"Файл '{file_name}' удалён")
        except Exception as e:
            print(e)

        print()
        menu(3)


def work_with_xml(file_task):
    global path, file_name

    if file_task == 1:  # Создаем XML файл
        while True:
            check_file_name("xml")
            if not file_name.endswith('.xml'):
                print("Файл имеет отличное расширение от XML")
            else:
                break

        root = ET.Element("Items")
        tree = ET.ElementTree(root)
        tree.write(path)

        print(f"Файл {file_name} создан")
        print()
        menu(4)

    elif file_task == 2:  # Добавление объектов в XML
        while not check_file_exists("xml"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.xml'):
                print("Файл имеет отличное расширение от XML")
                while not check_file_exists("xml"):
                    print("Файла с таким именем не существует")
            else:
                break


        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            print(f"Файл '{file_name}' не найден")
            return
        except ET.ParseError:
            print("Ошибка при разборе XML")
            return

        root = tree.getroot()
        add_objects_to_xml(root)
        tree.write(path)
        print(f"Данные успешно записаны в файл '{file_name}'")
        print()
        menu(4)

    elif file_task == 3:  # Чтение XML
        while not check_file_exists("xml"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.xml'):
                print("Файл имеет отличное расширение от XML")
                while not check_file_exists("xml"):
                    print("Файла с таким именем не существует")
            else:
                break

        try:
            tree = ET.parse(path)
        except FileNotFoundError:
            print(f"Файл '{file_name}' не найден")
            return
        except ET.ParseError:
            print("Ошибка при разборе XML")
            return

        root = tree.getroot()

        if len(root) == 0:
            print("Файл пуст")
        else:
            for item in root:
                print(f"Объект: {item.tag}")
                for field in item:
                    print(f"{field.tag}: {field.text}")
                print()
        print()
        menu(4)

    elif file_task == 4:  # Удаление XML файла
        while not check_file_exists("xml"):
            print("Файла с таким именем не существует")

        while True:
            if not file_name.endswith('.xml'):
                print("Файл имеет отличное расширение от XML")
                while not check_file_exists("xml"):
                    print("Файла с таким именем не существует")
            else:
                break

        try:
            os.remove(path)
            print(f"Файл '{file_name}' удалён")
        except Exception as e:
            print(e)

        print()
        menu(4)

def add_objects_to_xml(root):
    while True:
        object_name = input("Введите название объекта: ")
        item = ET.SubElement(root, object_name)

        while True:
            field_name = input("Введите название поля: ")
            field_value = input("Введите значение поля: ")
            field_element = ET.SubElement(item, field_name)
            field_element.text = field_value

            add_more_fields = input("Добавить еще одно поле в этот объект? (да/нет): ").lower()
            if add_more_fields != 'да':
                break

        add_more_objects = input("Добавить еще один объект? (да/нет): ").lower()
        if add_more_objects != 'да':
            break


def work_with_archives(file_task):
    global path, file_name, zip_path

    if file_task == 1:  # Создание архива
        while True:
            check_file_name("zip")
            if not file_name.endswith('.zip'):
                print("Файл имеет отличное расширение от zip")
            else:
                break

        with zipfile.ZipFile(path, 'w') as zip_file:
            pass

        print(f"Архив с именем '{file_name}' успешно создан")
        print()
        menu(5)

    elif file_task == 2:  # Добавление файла в архив
        while not check_file_exists("zip"):
            print("Архива с таким именем не существует")

        while True:
            if not file_name.endswith('.zip'):
                print("Файл имеет отличное расширение от zip")
                while not check_file_exists("zip"):
                    print("Архива с таким именем не существует")
            else:
                break

        zip_path = path

        print("Введите имя файла, который нужно добавить в архив:")
        while not check_file_exists():
            print("Файла с таким именем не существует")


        with zipfile.ZipFile(zip_path, 'a') as zip_file:  # 'a' открывает архив для добавления
            zip_file.write(path, os.path.basename(path))
            print(f"Файл {path} добавлен в архив {zip_path}")

        print()
        menu(5)

    elif file_task == 3:  # Разархивирование архива
        while not check_file_exists("zip"):
            print("Архива с таким именем не существует")

        while True:
            if not file_name.endswith('.zip'):
                print("Файл имеет отличное расширение от zip")
                while not check_file_exists("zip"):
                    print("Архива с таким именем не существует")
            else:
                break

        zip_path = path

        extract_path = os.path.join(dir_path, os.path.splitext(zip_path)[0])


        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(extract_path)
            print(f"Архив {zip_path} извлечён в папку по следующему пути: {extract_path}.")


            for file_info in zip_file.infolist():
                print(f"Файл: {file_info.filename}, Размер: {file_info.file_size} байт, Создан: {file_info.date_time}")

        print()
        menu(5)

    elif file_task == 4:  # Удаление архива
        while not check_file_exists("zip"):
            print("Архива с таким именем не существует")

        while True:
            if not file_name.endswith('.zip'):
                print("Файл имеет отличное расширение от zip")
                while not check_file_exists("zip"):
                    print("Архива с таким именем не существует")
            else:
                break

        try:
            os.remove(path)
            print(f"Архив {file_name} удалён")
        except Exception as e:
            print(e)

        print()
        menu(5)



if __name__ == "__main__":
    main()