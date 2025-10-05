# app.py
import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, flash, request ,redirect

# Создаем объект приложения
app = Flask(__name__)

# Функции БД
def init_db():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            user_agent TEXT,
            visit_date TEXT,
            page_url TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS visit_counter (
            id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')
    c.execute('INSERT OR IGNORE INTO visit_counter (id, count) VALUES (1, 0)')
    conn.commit()
    conn.close()

def log_visit(ip, user_agent, page_url='/'):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO visits (ip_address, user_agent, visit_date, page_url)
        VALUES (?, ?, ?, ?)
    ''', (ip, user_agent, datetime.now().isoformat(), page_url))
    c.execute('UPDATE visit_counter SET count = count + 1 WHERE id = 1')
    conn.commit()
    conn.close()

def get_visit_count():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('SELECT count FROM visit_counter WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

# Инициализация БД
init_db()

# Данные для сайта
my_data = {
    "name": "Владимир Болотов",
    "about_me": "Привет! Я начинающий программист, увлекаюсь IT.",
    "skills": ["Python", "HTML", "CSS", "Flask"],
    "visit_count": 0,
    "contacts": {
        "email": "login47rus@gmail.com",
        "github": "https://github.com/slyjewbro",
        "telegram": "https://t.me/slyjewbro",
        "vk": "https://vk.com/slyjewbro1337"},
    "projects": [
        {"name": "Мой сайт-визитка",
        "description": "Персональный сайт на Flask с адаптивным дизайном",
        "technologies": ["Python", "Flask", "HTML", "CSS"],
        "github_url": "https://github.com/slyjewbro/my-portfolio",
        "live_url": "https://slyjewbro.pythonanywhere.com"
        },
        {
        "name": "To-Do List", 
        "description": "Приложение для управления задачами",
        "technologies": ["Python", "Flask", "SQLite"],
        "github_url": "https://github.com/username/todo-app",
        "live_url": "https://username.pythonanywhere.com/todo"
        }     
]
         
    }

# Маршрут для главной страницы
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Здесь можно добавить отправку на email
    flash('Сообщение отправлено!', 'success')
    return redirect('/')
def log_ip_to_file(ip_address, user_agent=""):
    """Записывает IP-адрес в текстовый файл"""
    try:
        # Создаем папку logs если ее нет
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Создаем имя файла с текущей датой
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"logs/visitors_{today}.txt"
        
        # Формируем запись
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - IP: {ip_address} - User Agent: {user_agent}\n"
        
        # Записываем в файл
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"Записан IP: {ip_address} в файл {filename}")
        
    except Exception as e:
        print(f"Ошибка записи в файл: {e}")
@app.route("/")
def index():
    # Получаем информацию о посетителе
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Логируем в базу данных (если есть)
    try:
        log_visit(user_ip, user_agent)
    except:
        pass  # Игнорируем ошибки БД если ее нет
    
    # Логируем в текстовый файл
    log_ip_to_file(user_ip, request.headers.get('User-Agent','Unknown'))
    
    # Обновляем счетчик если есть БД
    try:
        my_data["visit_count"] = get_visit_count()
    except:
        my_data["visit_count"] = "N/A"
    
    return render_template('index.html', data=my_data)
@app.route("/logs")
def view_logs():
    """Показывает содержимое лог-файлов"""
    try:
        logs_content = []
        
        # Проверяем есть ли папка logs
        if os.path.exists('logs'):
            # Получаем все файлы логов
            log_files = [f for f in os.listdir('logs') if f.startswith('visitors_') and f.endswith('.txt')]
            log_files.sort(reverse=True)  # Сортируем по дате (новые сначала)
            
            # Читаем последние 3 файла
            for log_file in log_files[:3]:
                file_path = os.path.join('logs', log_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    logs_content.append(f"=== {log_file} ===\n{content}")
        
        return "<pre>" + "\n\n".join(logs_content) + "</pre>"
    
    except Exception as e:
        return f"Ошибка чтения логов: {e}" 
def log_detailed_visit(ip_address, request_info):
    """Детальное логирование посещения"""
    try:
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"logs/visitors_{today}.txt"
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Собираем детальную информацию
        log_entry = f"""
=== НОВОЕ ПОСЕЩЕНИЕ ===
Время: {timestamp}
IP-адрес: {ip_address}
Браузер: {request_info.headers.get('User-Agent', 'Unknown')}
URL: {request_info.url}
Метод: {request_info.method}
Язык: {request_info.headers.get('Accept-Language', 'Unknown')}
Реферер: {request_info.headers.get('Referer', 'No referer')}
------------------------
"""
        
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"Детально записан IP: {ip_address}")
        
    except Exception as e:
        print(f"Ошибка детальной записи: {e}")           
# Запускаем сервер
if __name__ == "__main__":
    app.run(debug=True)