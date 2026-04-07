import json
import csv

CONFIG_FILE = "config.json"

#нач параметры
DEFAULT_CONFIG = {
    "database": "mydb",
    "host": "localhost",
    "port": 5432,
    "use_ssl": False
}

config = {}


try:
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
        print("Файл загружен успешно.")

except FileNotFoundError:
    print(f"Файла '{CONFIG_FILE}' нету. Автоматически создам файл")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
    config = DEFAULT_CONFIG.copy()

except json.JSONDecodeError:
    print(f"Повреждённый JSON в файле. Автоматическим создам файл")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
    config = DEFAULT_CONFIG.copy()

except PermissionError:
    print("Нет прав на чтение файла")
    exit()

except Exception as e:
    print(f"Ошибка при чтении: {e}")
    exit()

while True:
    print("\nТекущие параметры")
    for k, v in config.items():
        print(f"{k}: {v}")
        
    print("\nДоступные ключи: database, host, port, use_ssl")
    print("Для выхода введите 'exit'")
    
    key = input("\nКакой параметр изменить? ").strip().lower()
    
    if key == "exit":
        print("Программа завершена.")
        break
        
    if key not in config:
        print("Такого параметра нет в конфигурации!")
        continue
        
    new_value = input(f"Введите новое значение для '{key}': ").strip()

    if key == "port":
        try:
            port_num = int(new_value)
            if 1 <= port_num <= 65535:
                config[key] = port_num
            else:
                print("Порт должен быть числом от 1 до 65535!")
                continue
        except ValueError:
            print("Порт должен быть целым числом!")
            continue
            
    elif key == "use_ssl":
        val_low = new_value.lower()
        if val_low in ("true", "1", "yes", "да"):
            config[key] = True
        elif val_low in ("false", "0", "no", "нет"):
            config[key] = False
        else:
            print("use_ssl должно быть true/false (или 1/0)!")
            continue
    else:
        if new_value == "":
            print("Строковое значение не может быть пустым!")
            continue
        config[key] = new_value
        

    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("Изменения успешно сохранены в файл. ->")
    except PermissionError:
        print("Нет прав на запись файла!")
    except Exception as e:
        print(f"Ошибка сохранения: {e}")