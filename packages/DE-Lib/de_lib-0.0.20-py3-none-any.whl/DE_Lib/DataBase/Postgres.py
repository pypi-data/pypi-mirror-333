import psycopg2 as ps2

class Postgres:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    def Connect(self, string_connect: dict):
        msg, conn = None, None
        try:
            # Efetuando a conexao com a instancia do BANCO
            conn = ps2.connect(user=string_connect["username"], password=string_connect["password"], database=string_connect["instance"], host=string_connect["host"])
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
            self._cnn = conn
        except Exception as error:
            conn = f"""Falha ao tentar se conectar com o banco de dados POSTGRES.\n """
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
        return self.__database_error