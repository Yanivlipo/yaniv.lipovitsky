import copy

import mysql.connector
from excercise10 import settings


class DBManager:
    __connection = None
    __cursor = None

    _CREATE_DB_SQL = """CREATE DATABASE if not exists %s """

    def __init__(self):
        self._create_database()

    def _create_database(self):
        db_config = copy.copy(settings.DB)
        db_name = db_config.pop('database')
        self.__connect(db_config)
        sql = self._CREATE_DB_SQL % db_name
        result = self.__execute(sql, db_name)
        self.__close_connection()
        return result

    def commit(self, query, args=()):
        # Use for INSERT UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        self.__connect()
        self.__execute(query, args)
        self.__connection.commit()
        affected_rows = self.__cursor.rowcount
        self.__close_connection()
        return affected_rows

    def fetch(self, query, args=()):
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = False
        self.__connect()
        if self.__execute(query, args):
            query_result = self.__cursor.fetchall()
        self.__close_connection()
        return query_result

    def execute(self, query, args=()):
        # Use for CREATE, DROP AND ALTER statements.
        self.__connect()
        query_result = self.__execute(query, args)
        self.__close_connection()
        return query_result

    def __connect(self, db_config = None):
        # Opens a connection to the database.
        try:
            db_config = db_config or settings.DB
            if not self.__connection or not self.__connection.is_connected():
                self.__connection = mysql.connector.connect(**db_config)
                self.__cursor = self.__connection.cursor(named_tuple=True)
        except mysql.connector.Error as error:
            print("Connection failed with error {}".format(error))

    def __execute(self, query, args=()):
        # Executes a given query with given args, if provided.
        if query:
            try:
                self.__cursor.execute(query, args)
                return True
            except mysql.connector.Error as error:
                print("Query failed with error {}".format(error))
        return False

    def __close_connection(self):
        # Closes an open database connection.
        try:
            if self.__connection.is_connected():
                self.__connection.close()
                self.__cursor.close()
        except mysql.connector.Error as error:
            print("Failed to close connection with error {}".format(error))


# Creates an instance for the DBManager class for export.
dbManager = DBManager()
