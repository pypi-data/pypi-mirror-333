import redshift_connector as DB


class Azure:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    def AZURE(self, string_connect: dict):
        conn = None
        try:
            from azure.storage.filedatalake import DataLakeServiceClient as az

            conn = az.connect(host=string_connect["host"],
                              database=string_connect["instance"],
                              user=string_connect["username"],
                              password=string_connect["password"]
                              )
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
        except Exception as error:
            self._connection_is_valid = False
            self.__database_error = conn.DatabaseError
            conn = error
        finally:
            return conn

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