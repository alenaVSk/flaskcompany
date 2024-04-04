import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash, abort
from FDataBase import FDataBase

# конфигурация
DATABASE = '/tmp/fcompany.db'  # путь к БД
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'


app = Flask(__name__)
app.config.from_object(__name__)  # загружаем конфигурацию из приложения (__name__ ссылается на этот текущий модуль)

app.config.update(dict(DATABASE=os.path.join(app.root_path,'fcompany.db'))) # переопределим путь к БД(ссылка на тек каталог


def connect_db():  # общая функция для установления соединения с БД
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row  # записи будут представлены не в виде кортежей, а в виде словаря (для исп в шаблонах)
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД (без запуска вебсервера)"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:  # откр файл для чтения
        db.cursor().executescript(f.read())      # выполняем скрипт кот находится в файле
    db.commit()             # применить изменения к текущей БД
    db.close()             # закрыть установленное соединение


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    return render_template("index.html")


@app.route("/zhurnal")
def showZhurnal():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("zhurnal.html", title="журнал", log=dbase.getLog())


@app.route("/aaa")
def aaa():
    db = get_db()
    return render_template("aaa.html", title='aaa')


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
