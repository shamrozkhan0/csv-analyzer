from dotenv import load_dotenv
import logging as log
import pymysql
import os


load_dotenv()
log.basicConfig(level=log.INFO, format="%(asctime)s %(levelname)s | %(message)s")


class Database:


    def __init__(self):
        self.table_name = os.getenv("MYSQL_DATA_TABLE_NAME")


    def _database_connector(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password=f"{os.getenv('MYSQL_PASSWORD')}",
                database="analyzer"
            )

            log.info("Connection successfully created with database. ")

            return connection

        except pymysql.Error as e:
            log.error(f"Error connection to Database: {e}")
            return False


    def _check_if_table_exist(self):
        query = f"""
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
            AND table_name = %s
            LIMIT 1
        """
        try:
           connection = self._database_connector()

           with connection.cursor() as cursor:
               cursor.execute(query, ("analyzer", self.table_name))
               result = cursor.fetchone()

               cursor.close()
               connection.close()

               if result:
                   return True

               else:
                   return False

        except pymysql.Error as e:
           log.error(f"Error searching for table: {e}")



    def insert_data_into_database(self, data: str, file_id: int):

        try:
            connection = self._database_connector()

            if not self._check_if_table_exist():
                log.info("table isn't exist.")

                with connection.cursor() as cursor:
                    query = f""" CREATE TABLE {self.table_name} (
                              file_id INT NOT NULL,
                              content TEXT NOT NULL
                    ) """
                    cursor.execute(query)
                    log.info("Table created successfully.")


            with connection.cursor() as cursor:
                insert_data_query = f"""
                        INSERT INTO {self.table_name} (file_id, content)
                        VALUES (%s , %s) 
                """
                cursor.execute(insert_data_query, (file_id, data ))
                log.info("Data inserted successfully.")

            connection.commit()
            connection.close()

            return True

        except pymysql.Error as e:
            log.error(f"Error inserting data into database: {e}")
            return False



    def get_content_by_id(self, id: int):
        query = f"""SELECT content FROM {self.table_name} WHERE file_id = %s"""

        try:
            connection = self._database_connector()

            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                result = cursor.fetchall()
                log.info("Successfully fetch content from database.")
                return result

        except pymysql.Error as e:
            log.error(f"Error fetching content from database {e}")
            return None



c = Database()
c.get_content_by_id(2580163)