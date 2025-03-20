

class Informix:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    # ----------------------------------------------------------------
    # Falta tudo (Instalar driver ODBC) Maquina local não permite
    def Connect(self, string_connect: dict):
        try:
            pass
            self._connection_is_valid = True
            self._cnn = None
        except Exception as error:
            self._connection_is_valid = False
            self._DATABASE_ERROR = True
        finally:
            pass

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