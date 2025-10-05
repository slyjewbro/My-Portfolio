# app.py
from flask import Flask, render_template, flash, request ,redirect

# Создаем объект приложения
app = Flask(__name__)

# Данные для сайта
my_data = {
    "name": "Владимир Болотов",
    "about_me": "Привет! Я начинающий программист, увлекаюсь IT.",
    "skills": ["Python", "HTML", "CSS", "Flask"],
    "contacts": {
        "email": "login47rus@gmail.com",
        "github": "https://github.com/slyjewbro",
        "telegram": "https://t.me/slyjewbro",
        "vk": "https://vk.com/slyjewbro1337"},
    "projects": {
        "name": "Мой сайт-визитка",
        "description": "Персональный сайт на Flask с адаптивным дизайном",
        "technologies": ["Python", "Flask", "HTML", "CSS"],
        "github_url": "https://github.com/slyjewbro/my-portfolio",
        "live_url": "https://slyjewbro.pythonanywhere.com"
    }
}

# Маршрут для главной страницы
@app.route("/")
def index():
    return render_template("index.html", data=my_data)
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Здесь можно добавить отправку на email
    flash('Сообщение отправлено!', 'success')
    return redirect('/')

# Запускаем сервер
if __name__ == "__main__":
    app.run(debug=True)