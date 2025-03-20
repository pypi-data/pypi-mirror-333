import fbd

class Firebird:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    # ----------------------------------------------------------------
    # Falta driver - maquina local não permite
    def Connect(self, string_connect: dict):
        msg, conn = None, None
        try:
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            instance = string_connect["instance"]
            conn = fbd.connect(host=host, database=instance, user=user, password=pwd, port=port)
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
            self._cnn = conn
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = conn.DatabaseError
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
        return self._DATABASE_ERROR