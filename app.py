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
@app.route("/")
def index():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    log_visit(user_ip, user_agent)
    
    visit_count = get_visit_count()
    
    # Обновляем данные для шаблона
    my_data["visit_count"] = visit_count
    
    return render_template('index.html', data=my_data)
# Запускаем сервер
if __name__ == "__main__":
    app.run(debug=True)