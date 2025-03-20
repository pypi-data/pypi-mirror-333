import sqlite3 as sq3
import os

class SQLite:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    def Connect(self, database, **kwargs):
        result, msg, conn = False, None, None
        try:
            if os.path.isfile(database):
                if "check_same_thread" in kwargs.keys():
                    __check_same_thread = kwargs.get("check_same_thread")
                else:
                    __check_same_thread = True
                result = sq3.connect(database, check_same_thread=__check_same_thread)
                self._connection_is_valid = True
                self._cnn = result
                self.__database_error = f"""SQLITE database: {database}\nConexao bem sucedida!"""
            else:
                raise Exception("File NOT FOUND!")
            self._nome_database = 'SQLITE'
        except Exception as error:
            msg = f"""SQLITE database: {database}\nFalha ao tentar se conectar com o banco de dados SQLITE\nException Error: {error} """
            result = msg
            self._connection_is_valid = False
            self.__database_error = msg + "\n" + error
        finally:
            return result

    @property
    def CONNECTION(self):
        return self._cnn

    @property
    def CONNECTION_VALID(self):
        return self._connection_is_valid

    @property
    def NOME_DATABASE(self):
        return self._nome_database.upper()

    @property
    def DATABASE_ERROR(self):
        return self.__database_error