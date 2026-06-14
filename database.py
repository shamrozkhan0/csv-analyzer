from dotenv import load_dotenv
import logging as log
import pymysql
import json
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


    def insert_analytics_into_database(self, data: str, file_id: int):
        try:
            connection = self._database_connector()
            if not self._check_if_table_exist():
                log.info("table isn't exist.")
                with connection.cursor() as cursor:
                    query = f""" CREATE TABLE {self.table_name} (
                              file_id INT NOT NULL,
                              content TEXT NOT NULL,
                              conversation JSON,
                              PRIMARY KEY (file_id)
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
        except pymysql.Error as e:
            log.error(f"Error inserting data into database: {e}")


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


    def update_conversation_into_database(self, conversation: str, file_id:int):
        previous_conversation_query = f"""
                SELECT conversation from {self.table_name} WHERE file_id = %s
                """

        query = f"""
                UPDATE {self.table_name} SET conversation = %s WHERE file_id = %s
                """
        try:
            connection = self._database_connector()
            with connection.cursor() as cursor:
                cursor.execute(previous_conversation_query, (file_id,))
                result = cursor.fetchone()
                if result and result[0]:
                    prev_conversation = json.loads(result[0])
                else:
                    prev_conversation = {"messages": []}
                current_message = conversation
                prev_conversation["messages"].append(current_message)
                final_conversation_json = json.dumps(prev_conversation)
                cursor.execute(query, (final_conversation_json, file_id))
                log.info("Success: 'Conversation = (prompt, response)' have been inserted into database ")
            connection.commit()
            connection.close()
        except pymysql.Error as e:
            log.error(f"Error: inserting 'conversation = (prompt, response)' inserting into database  {e}")


    def get_conversation_by_id(self, id: int):
        connection = self._database_connector()
        query = f""" SELECT conversation FROM {self.table_name} WHERE file_id = %s"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                connection.commit()
                return cursor.fetchall()
        except pymysql.Error as e:
            log.error(e)


c = Database()
c.get_conversation_by_id(7937341)