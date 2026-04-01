import csv 
import json
from datetime import *

source = input("Введите путь к исходному файлу: ")
folder = input("Введите путь к папке назначения: ")
if not folder:
    folder= "."
try:
    with open(source, "r", encoding="utf-8") as test:
        pass 
    print("файл найден")
except FileNotFoundError:
    print(f"Ошибка: Файл '{source}' не найден.")
    exit()
except PermissionError:
    print(f"Нет доступа к файлу '{source}.")
    exit()
except UnicodeDecodeError:
    print(f"Ошибка: Неверная кодировка файла '{filename}'.")
    exit()
except Exception as e:
    print(f"Неизвестная ошибка при работе с файлом: {e}")
    exit()

try:
    if "\\" in source:
        newfile = source.split("\\")[-1]
    elif "/" in source:
        newfile = source.split("/")[-1]
    else:
        newfile = source
    
    if "." in newfile:
        name_parts = newfile.rsplit(".", 1)
        name_without_ext = name_parts[0]
        ext = "." + name_parts[1]
        file_name = newfile
    else:
        file_name = newfile
    
 
    now = datetime.now()
    date_str = f"{now.year}-{now.month:02d}-{now.day:02d}"
    time_str = f"{now.hour:02d}-{now.minute:02d}-{now.second:02d}"
    
    backup_name = f"{file_name}_{date_str}_{time_str}_backup{ext}"
    if "\\" in folder:
        backup_path = folder + "\\" + backup_name
    else:
        backup_path = folder + "/" + backup_name
    print("Резервная копия файла была создана")

except Exception as e:
    print(f"Ошибка при формировании резервного файла: {e}")
    exit()

try:
    source_file=open(source, "rb")
    backup_file=open(backup_path, "wb")
    while True:
        data=source_file.read()
        if not data:
            break
        backup_file.write(data)
    source_file.close()
    backup_file.close()
    print(f"Файл скопирован - Исходный файл: {source}")
    print(f"Файл копии: {backup_path}")
except FileNotFoundError:
    print("Ошибка: Файл не найден при копировании!")
    exit()
except PermissionError:
    print("Ошибка: Нет прав доступа к файлу!")
    exit()
except Exception as e:
    print(f"Ошибка при копировании: {e}")
    exit()