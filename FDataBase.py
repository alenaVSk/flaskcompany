import sqlite3


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


    # Метод для обновления данных записи
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

    def getStock(self):
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
