from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

def database_connector():
    try:
        print(os.getenv("MYSQL_PASSWORD"))
        connection = pymysql.connect(
            host="localhost",
            user="root",
            password=f"{os.getenv('MYSQL_PASSWORD')}",
            database="analyzer"
        )

        return connection

    except pymysql.MySQLError as e:
        print(e)
        return None


def check_if_table_exist(table_name: str):
    query = f"""
        SELECT 1
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_name = %s
        LIMIT 1
     """

    connection = database_connector()

    if connection is None:
        print("Connection Failed")
        return


    with connection.cursor() as cursor:
        cursor.execute(query, ("analyzer", table_name))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:
            print("table exist")
            return True

        else:
            print("table not exist")
            return False



def insert_data_into_database(data: str, file_id: int):
    connection = database_connector()
    table_name = os.getenv("MYSQL_DATA_TABLE_NAME")

    if not check_if_table_exist(table_name):
        print("table isn't exist")

        with connection.cursor() as cursor:
            query = f""" CREATE TABLE {table_name} (
                          file_id INT NOT NULL,
                          content TEXT NOT NULL
                  ) """
            cursor.execute(query)
        print("Table created successfully")


    with connection.cursor() as cursor:
        insert_data_query = f"""
                    INSERT INTO {table_name} (file_id, content)
                    VALUES (%s , %s) 
            """
        cursor.execute(insert_data_query, (file_id, data ))

    connection.commit()
    connection.close()

    return True
