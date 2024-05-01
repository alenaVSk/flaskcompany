import sqlite3
import os
from flask import Flask, render_template, url_for, request, g, flash, abort, redirect
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


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/zhurnal")
def showZhurnal():
    return render_template("zhurnal.html", title="Журнал", log=dbase.getLog())


@app.route("/add_customer", methods=["POST", "GET"])
def addCustomer():
    if request.method == "POST":

        res = dbase.addCustomer(request.form['data_order'], request.form['name_customer'], request.form['brand_car'],
                                request.form['number_car'], request.form['text_order'],)
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_customer.html', title="Добавление записи в журнал")


# Маршрут для удаления записи в "Журнал"
@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    try:
        dbase.delete_entry(entry_id)
        flash('Запись успешно удалена', 'success')
    except:
        flash('Ошибка удаления записи', 'danger')
    return redirect(url_for('showZhurnal'))


# Маршрут для страницы редактирования записи записи в "Журнал"
@app.route('/edit_entry/<int:entry_id>', methods=['GET'])
def edit_entry(entry_id):
    entry_data = dbase.get_entry(entry_id)
    # print(entry_data)  # Проверка, получены ли данные
    return render_template('edit_entry.html', title="Редактировать", entry_data=entry_data)


# Маршрут для сохранения изменений
@app.route('/save_entry/<int:entry_id>', methods=['POST'])
def save_entry(entry_id):
    data_order = request.form['data_order']
    name_customer = request.form['name_customer']
    brand_car = request.form['brand_car']
    number_car = request.form['number_car']
    text_order = request.form['text_order']
    dbase.update_entry(entry_id, data_order, name_customer, brand_car, number_car, text_order)
    return redirect(url_for('showZhurnal'))


@app.route("/stock")
def showStock():
    return render_template("stock.html", title="Склад материалов", stock=dbase.getStock())


@app.route("/add_stock", methods=["POST", "GET"])
def addStock():
    if request.method == "POST":

        res = dbase.addStock(request.form['name'], request.form['quantity'], request.form['price_unit'])
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_stock.html', title="Добавление материалов на склад")


@app.route("/employees")
def showEmployees():
    return render_template("employees.html", title="Сотрудники", employees=dbase.getEmployees())


@app.route("/add_employees", methods=["POST", "GET"])
def addEmployees():
    if request.method == "POST":

        res = dbase.addEmployees(request.form['name'], request.form['profession'])
        if not res:
            flash('Ошибка добавления', category='error')
        else:
            flash('Запись добавлена успешно', category='success')

    return render_template('add_employees.html', title="Добавление сотрудника")


# Маршрут для удаления записи в "Сотрудники"
@app.route('/delete_entry_employees/<int:entry_id>', methods=['POST'])
def delete_entry_employees(entry_id):
    try:
        dbase.delete_entry_employees(entry_id)
        flash('Запись успешно удалена', 'success')
    except:
        flash('Ошибка удаления записи', 'danger')
    return redirect(url_for('showEmployees'))


# Маршрут для страницы редактирования записи записи в "Сотрудники"
@app.route('/edit_entry_employees/<int:entry_id>', methods=['GET'])
def edit_entry_employees(entry_id):
    entry_data = dbase.get_entry_employees(entry_id)
    # print(entry_data)  # Проверка, получены ли данные
    return render_template('edit_entry_employees.html', title="Редактировать", entry_data=entry_data)


# Маршрут для сохранения изменений  в "Сотрудники"
@app.route('/save_entry_employees/<int:entry_id>', methods=['POST'])
def save_entry_employees(entry_id):
    name = request.form['name']
    profession = request.form['profession']
    dbase.update_entry_employees(entry_id, name, profession)
    return redirect(url_for('showEmployees'))


# Акт выполненных работ/ форма для составления
@app.route("/act_form", methods=["GET", "POST"])
def addAct_foreign_key():
    if request.method == "GET":
        # Логика для отображения формы
        return render_template('act.html', title="Составление акта")
    elif request.method == "POST":
        data_order = request.form.get('data_order')
        data_act = request.form.get('data_act')
        number_car = request.form.get('number_car')

        materials = request.form.getlist('materials[]')
        price_materials = request.form.getlist('price_materials[]')
        quantity = request.form.getlist('quantity[]')
        work_completed = request.form.getlist('work_completed[]')
        name_work = request.form.getlist('name_work[]')
        price_work = request.form.getlist('price_work[]')

        print("Содержимое request.form:", request.form)
        print("Содержимое data_order:", data_order)
        print("Содержимое data_act:", data_act)
        print("Содержимое number_car:", number_car)
        print("Содержимое materials:", materials)
        print("Содержимое price_materials:", price_materials)
        print("Содержимое quantity:", quantity)
        print("Содержимое work_completed:", work_completed)
        print("Содержимое name_work:", name_work)
        print("Содержимое price_work:", price_work)

        try:
            dbase.addAct_foreign_key(data_order, data_act, number_car, materials, price_materials, quantity, work_completed, name_work, price_work)
            flash('Запись успешно удалена', 'success')
        except:
            flash('Ошибка удаления записи', 'danger')

        #return render_template('act.html', title="Составление акта")
        return redirect(url_for('addAct_foreign_key'))

""""
# Акт выполненных работ / форма для составления
@app.route("/act_form", methods=["POST"])
def addAct_foreign_key():
    data = request.form.getlist('data[]')

    print("Содержимое request.form:", request.form)
    print("Содержимое data:", data)

    data_order = data[0]
    data_act = data[1]
    number_car = data[2]
    materials = data[3::9]
    price_materials = data[4::9]
    quantity = data[5::9]
    work_completed = data[6::9]
    name_work = data[7::9]
    price_work = data[8::9]

    try:
        dbase.addAct_foreign_key(data_order, data_act, number_car, materials, price_materials, quantity, work_completed, name_work, price_work)
        flash('Запись успешно удалена', 'success')
    except:
        flash('Ошибка удаления записи', 'danger')

    return render_template('act.html', title="Составление акта")
"""

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


if __name__ == "__main__":
    app.run(debug=True)
