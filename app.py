# app.py
from flask import Flask, render_template

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
        "vk": "https://vk.com/slyjewbro1337"
    }
}

# Маршрут для главной страницы
@app.route("/")
def index():
    return render_template("index.html", data=my_data)

# Запускаем сервер
if __name__ == "__main__":
    app.run(debug=True)