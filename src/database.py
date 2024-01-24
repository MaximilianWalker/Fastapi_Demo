import mysql.connector
from fastapi import Depends
from settings import settings

class Result:
    def __init__(self, result, arguments):
        self.result = result
        self.arguments = arguments

class Database:

    def __init__(self):
        self.host = settings.db_host
        self.port = settings.db_port
        self.schema = settings.db_schema
        self.user = settings.db_user
        self.password = settings.db_password

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                port = self.port,
                database = self.schema,
                user = self.user,
                password = self.password
            )
        except Exception as e:
            raise "Failed connection to the database!"

    def execute_procedure(self, procedure, *arguments, hasResult=False):
        cursor = self.connection.cursor(buffered=True, dictionary=True)
        result_query, result_arguments = None, None
        try:
            result_arguments = cursor.callproc(procedure, arguments)
            self.connection.commit()
            if hasResult:
                result_query = list(cursor.stored_results())[0].fetchall()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            raise e
        finally:
            cursor.close()
        return Result(result_query, result_arguments)

    def close(self):
        self.connection.close()
