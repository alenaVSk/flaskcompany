import sqlite3
from row_data import process_row_data


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getLog(self):
        sql = '''SELECT * FROM log'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            log_list = [dict(row) for row in res]
            if log_list: return log_list
        except:
            print("Ошибка чтения из БД")
        return []

    def addCustomer(self, data_order, name_customer, brand_car, number_car, text_order):
        try:
            self.__cur.execute("INSERT INTO log VALUES(NULL, ?, ?, ?, ?, ?)", (data_order, name_customer, brand_car, number_car, text_order))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True


    def delete_entry(self, entry_id):
        sql = '''DELETE FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except Exception as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()


    def get_entry(self, entry_id):
        sql = '''SELECT * FROM log WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except Exception as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None


    # Метод для обновления данных в Журнале
    def update_entry(self, entry_id, data_order, name_customer, brand_car, number_car, text_order):
        try:
            sql = '''UPDATE log 
                     SET data_order = ?, name_customer = ?, brand_car = ?, number_car = ?, text_order = ? 
                     WHERE id = ?'''
            self.__cur.execute(sql, (data_order, name_customer, brand_car, number_car, text_order, entry_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в БД:", str(e))
            self.__db.rollback()

    # Отображение Склада (stock_plus - stock_minus), 71 строка: SUM(sp.quantity) - COALESCE(SUM(sm.quantity), 0) AS quantity_total,
    def getStock(self):
        print('getStock quantity, quantity_totalFFF', self)
        sql = '''SELECT 
                    sp.name AS name_total,
                    SUM(sp.quantity) - COALESCE(SUM(sm.quantity), 0) AS quantity_total,
	                sp.price_unit AS price_unit_total
                 FROM 
                    stock_plus sp
                    LEFT JOIN 
                    stock_minus sm ON sp.name = sm.name AND sp.price_unit = sm.price_unit
                 GROUP BY 
                    sp.name, sp.price_unit;'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            stock_list = [dict(row) for row in res]
            print('stock_listFFF', stock_list)
            if stock_list:
                return stock_list
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
        return []

    def addStock(self, name, quantity, price_unit):
        try:
            self.__cur.execute("""
                INSERT INTO stock_plus (name, quantity, price_unit) 
                VALUES (?, ?, ?)
                ON CONFLICT(name, price_unit) DO UPDATE 
                SET quantity = quantity + EXCLUDED.quantity;
                """, (name, quantity, price_unit))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Список сотрудников
    def getEmployees(self):
        sql = '''SELECT * FROM employees'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            # Преобразование каждой строки в список значений
            employees_list = [dict(row) for row in res]
            if employees_list: return employees_list
        except:
            print("Ошибка чтения из БД")
        return []

    # Добавление сотрудника
    def addEmployees(self, name, profession):
        try:
            self.__cur.execute("INSERT INTO employees VALUES(NULL, ?, ?)", (name, profession))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    # Удаление из списка сотрудников
    def delete_entry_employees(self, entry_id):
        sql = '''DELETE FROM employees WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            self.__db.commit()
        except Exception as e:
            print("Ошибка удаления из БД:", str(e))
            self.__db.rollback()

   # Редактирование списка сотрудников
    def get_entry_employees(self, entry_id):
        sql = '''SELECT * FROM employees WHERE id = ?'''
        try:
            self.__cur.execute(sql, (entry_id,))
            res = self.__cur.fetchone()
            if res:
                return dict(res)
        except Exception as e:
            print("Ошибка при получении записи из БД:", str(e))
        return None


    # Метод для обновления данных о сотрудниках
    def update_entry_employees(self, entry_id, name, profession):
        try:
            sql = '''UPDATE employees
                     SET name = ?, profession = ? 
                     WHERE id = ?'''
            self.__cur.execute(sql, (name, profession, entry_id))
            self.__db.commit()
        except Exception as e:
            print("Ошибка при обновлении записи в БД:", str(e))
            self.__db.rollback()



# Добавление данных в акт вып работ

    def addAct_foreign_key_db(self, data_order, data_act, number_car, form):
        #print(f"data_order: {data_order}, data_act: {data_act}, number_car: {number_car}, form: {form}")
        try:
            # Добавление данных в таблицу act_foreign_key
            self.__cur.execute("INSERT INTO act_foreign_key (data_order, data_act, number_car) VALUES (?, ?, ?)",
                               (data_order, data_act, number_car))

            # Получение автоматически сгенерированного act_id
            act_id = self.__cur.lastrowid

            for row_data in form:
                materials = row_data['materials'][0]
                price_materials = row_data['price_materials'][0]
                quantity = row_data['quantity'][0]
                work_completed = row_data['work_completed'][0]
                name_work = row_data['name_work'][0]
                price_work = row_data['price_work'][0]

                sql_act_materials = "INSERT INTO act_materials (act_id, materials, price_materials, quantity) VALUES (?, ?, ?, ?)"
                self.__cur.execute(sql_act_materials, (act_id, materials, price_materials, quantity))

                sql_stock_minus = "INSERT INTO stock_minus (name, price_unit, quantity) VALUES (?, ?, ?)"
                #print('ACT sql_stock_minus, (materials, price_materials, quantity)', materials, price_materials, quantity)
                #print('STOCK stock_minus (name, price_unit, quantity)', materials, price_materials, quantity)
                self.__cur.execute(sql_stock_minus, (materials, price_materials, quantity))

                sql_act_work = "INSERT INTO act_work (act_id, work_completed, name_work, price_work) VALUES (?, ?, ?, ?)"
                self.__cur.execute(sql_act_work, (act_id, work_completed, name_work, price_work))

            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления данных в БД: {str(e)}")
            self.__db.rollback()
            raise Exception(f"Ошибка добавления данных в БД: {str(e)}")

"""
    def addAct_foreign_key_db(self, data_order, data_act, number_car, form):
        print(f"data_order: {data_order}, data_act: {data_act}, number_car: {number_car}")
        try:
            # Добавление данных в таблицу act_foreign_key
            self.__cur.execute("INSERT INTO act_foreign_key (data_order, data_act, number_car) VALUES (?, ?, ?)",
                               (data_order, data_act, number_car))

            # Получение автоматически сгенерированного act_id
            act_id = self.__cur.lastrowid

            for key in form:
                if key.startswith("materials"):
                    print("Processing materials row")
                    row_data = process_row_data(form)
                    print(f"Row data: {row_data}")
                    for materials, price_materials, quantity, work_completed, name_work, price_work in zip(
                            row_data['materials'], row_data['price_materials'],
                            row_data['quantity'], row_data['work_completed'],
                            row_data['name_work'], row_data['price_work']):
                        sql_act_materials = "INSERT INTO act_materials (act_id, materials, price_materials, quantity) VALUES (?, ?, ?, ?)"
                        self.__cur.execute(sql_act_materials, (act_id, materials, price_materials, quantity))

                        sql_stock_minus = "INSERT INTO stock_minus (name, price_unit, quantity) VALUES (?, ?, ?)"
                        self.__cur.execute(sql_stock_minus, (materials, price_materials, quantity))

                        sql_act_work = "INSERT INTO act_work (act_id, work_completed, name_work, price_work) VALUES (?, ?, ?, ?)"
                        self.__cur.execute(sql_act_work, (act_id, work_completed, name_work, price_work))

            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Ошибка добавления данных в БД: {str(e)}")
            self.__db.rollback()
            raise Exception(f"Ошибка добавления данных в БД: {str(e)}")


        # Добавление данных в акт вып работ

    def addAct_foreign_key(self, data_order, data_act, number_car, materials, price_materials, quantity, work_completed,
                           name_work, price_work):
        try:
            # Добавление данных в таблицу act_foreign_key
            self.__cur.execute("INSERT INTO act_foreign_key (data_order, data_act, number_car) VALUES (?, ?, ?)",
                               (data_order, data_act, number_car))

            # Получение автоматически сгенерированного act_id
            act_id = self.__cur.lastrowid

            # Добавление данных в таблицу act_materials и stock_minus
            for i in range(len(materials)):
                # Добавление данных в таблицу act_materials
                self.__cur.execute("INSERT INTO act_materials (act_id, materials, price_materials, quantity) VALUES (?, ?, ?, ?)",
                                   (act_id, materials[i], price_materials[i], quantity[i]))

                # Добавление данных в таблицу stock_minus
                self.__cur.execute("INSERT INTO stock_minus (name, price_unit, quantity) VALUES (?, ?, ?)",
                                   (materials[i], price_materials[i], quantity[i]))

            # Добавление данных в таблицу act_work
            for i in range(len(work_completed)):
                self.__cur.execute(
                    "INSERT INTO act_work (act_id, work_completed, name_work, price_work) VALUES (?, ?, ?, ?)",
                    (act_id, work_completed[i], name_work[i], price_work[i]))

            # Применение изменений к базе данных
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления данных в БД: " + str(e))
            self.__db.rollback()
            return False

        return True
        
"""
