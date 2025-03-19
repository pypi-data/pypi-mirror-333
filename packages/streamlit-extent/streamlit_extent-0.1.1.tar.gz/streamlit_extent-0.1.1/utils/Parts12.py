import pyodbc
import json

def connect_db(query,result=True,return_json=True):
    str_conn=pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};server=tcp:84.54.228.191,49172;database=Pushkarcki;UID=Pushkarcki;PWD=3kVJPI3h")

    try:
        # Подключение к базе данных
        
        cursor = str_conn.cursor()

        # Выполнение SQL-запроса
        cursor.execute(query)

        # Если запрос требует возврата данных (например, SELECT)
        if result:
            data = cursor.fetchall()

            # Если нужно вернуть данные в JSON формате
            if return_json:
                # Получаем имена колонок
                columns = [column[0] for column in cursor.description]
                # Преобразуем данные в список словарей
                result = [dict(zip(columns, row)) for row in data]
                # Преобразуем список словарей в JSON
                return json.dumps(result, ensure_ascii=False, indent=4)
            else:
                return data

        # Если запрос не требует возврата данных (например, INSERT, UPDATE, DELETE)
        str_conn.commit()  # Подтвердить изменения
        return None
    except pyodbc.Error as e:
        print(f"Ошибка выполнения запроса: {e}")
        return None
    finally:
        # Закрытие ресурсов
        try:
            if cursor:
                cursor.close()
            if str_conn:
                str_conn.close()
        except Exception as close_error:
            print(f"Ошибка при закрытии ресурсов: {close_error}")