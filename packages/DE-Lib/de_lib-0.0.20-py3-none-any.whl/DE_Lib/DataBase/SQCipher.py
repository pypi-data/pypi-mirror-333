

class SQCipher:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    def Connect(self, database, password):
        DATABASE_NAME, result, msg, conn = None, False, None, None
        try:
            if os.path.isfile(database):
                #conn = sqch.connect(database, password=password)
                self._connection_is_valid = True
                self._nome_database = 'SQLCIPHER'
                self._cnn = conn
            else:
                msg = f"""SQLITE [{database}]- Não existe no local informado!"""
                raise Exception(msg)
        except Exception as error:
            conn = error
            self._connection_is_valid = False
            self._DATABASE_ERROR = True
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