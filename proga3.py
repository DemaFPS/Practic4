import re # взял с гпт

LOG_FILE = "access.log"
REPORT_FILE = "log_analysis_report.txt"

#статистика
ip_counts = {}    
status_counts = {}  
total_bytes = 0     
unique_urls = set() 

# Регулярное выражение для разбора строки Apache Common Log Format - с гпт
LOG_PATTERN = re.compile(
    r'(\d+\.\d+\.\d+\.\d+)\s+'   # IP адрес
    r'\S+\s+'                     # ident
    r'\S+\s+'                     # authuser
    r'\[([^\]]+)\]\s+'            # Дата
    r'"(\w+)\s+'                  # Метод
    r'(\S+)\s+'                   # URL
    r'\S+"\s+'                    # Протокол
    r'(\d{3})\s+'                 # Код статуса
    r'(\d+|-)'                    # Размер ответа
)

print("<<< Анализатор логов веб-сервера >>>")
lines = []

try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"Файл '{LOG_FILE}' загружен.")
except FileNotFoundError:
    print(f"Файл не найден. Создам тестовый access.log")
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write('127.0.0.1 - - [10/Oct/2023:13:55:36 +0000] "GET /index.html HTTP/1.1" 200 2326\n')
        f.write('192.168.1.5 - - [10/Oct/2023:13:56:00 +0000] "POST /api/login HTTP/1.1" 401 512\n')
        f.write('127.0.0.1 - - [10/Oct/2023:13:57:12 +0000] "GET /style.css HTTP/1.1" 200 1024\n')
        f.write('10.0.0.1 - - [10/Oct/2023:13:58:05 +0000] "GET /about.html HTTP/1.1" 404 230\n')
        f.write('10.0.0.1 - - [10/Oct/2023:13:58:05 +0000] "GET /about.html HTTP/1.1" 404 230\n')
        f.write('Это некорректная строка лога\n')
        f.write('10.0.0.1 - - [10/Oct/2023:13:58:05 +0000] "GET /about.html HTTP/1.1" 404 230\n')
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print("Тестовый файл создан и загружен.")
except PermissionError:
    print("Нет прав на чтение файла!")
    exit()
except Exception as e:
    print(f"Ошибка при чтении: {e}")
    exit()

#обработка строк
for line in lines:
    line = line.strip()
    if not line:
        continue
        
    match = LOG_PATTERN.match(line)
    if match:
        ip = match.group(1)
        url = match.group(4)
        status = match.group(5)
        size_str = match.group(6)
        
        size = 0 if size_str == '-' else int(size_str) if size_str.isdigit() else 0

        ip_counts[ip] = ip_counts.get(ip, 0) + 1
        
        status_counts[status] = status_counts.get(status, 0) + 1
        
        total_bytes += size

        unique_urls.add(url)
    else:
        pass


report = []

report.append("       ОТЧЁТ АНАЛИЗА ЛОГОВ СЕРВЕРА")


report.append("\nКоличество запросов по IP-адресам:")
report.append(f"{'IP-адрес':<20} | {'Запросов'}")
report.append("-" * 35)
for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
    report.append(f"{ip:<20} | {count}")

report.append("\nКоличество запросов по коду ответа:")
report.append(f"{'Код':<10} | {'Запросов'}")
report.append("-" * 25)
for status, count in sorted(status_counts.items()):
    report.append(f"{status:<10} | {count}")

report.append("\nОбщий объём переданных данных:")
report.append(f"Всего: {total_bytes} байт")

report.append("\nКоличество уникальных URL:")
report.append(f"Всего: {len(unique_urls)}")

report.append("\n ============================")
report_text = "\n".join(report)


print(report_text)

try:
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\nОтчёт сохранён в {REPORT_FILE}")
except Exception as e:
    print(f"Не удалось сохранить отчёт: {e}")