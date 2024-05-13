# функция которая извлекает данные о материалах и работах из каждой строки формы и возвращает их в виде словаря.
def process_row_data(row):
    materials = row.getlist('materials[]')
    price_materials = row.getlist('price_materials[]')
    quantity = row.getlist('quantity[]')
    work_completed = row.getlist('work_completed[]')
    name_work = row.getlist('name_work[]')
    price_work = row.getlist('price_work[]')
    print("process_row_data(row)")
    row_data = {
        'materials': materials,
        'price_materials': price_materials,
        'quantity': quantity,
        'work_completed': work_completed,
        'name_work': name_work,
        'price_work': price_work
    }

    print(f"Row data: {row_data}")  # строка для печати данных

    return row_data
