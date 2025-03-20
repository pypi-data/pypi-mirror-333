import os
import cx_Oracle as ora
import sqlalchemy as sqa
import json

class Oracle:
    def __init__(self):
        self._connection_is_valid = None
        self._nome_database = None
        self._cnn = None
        self.__database_error = None

    def Connect_ORA(self, string_connect: dict):
        pathlib, msg, result = None, None, None
        try:
            # Definindo a Library ORACLE
            if "library" in string_connect.keys():
                if string_connect["library"] is None:
                    pathlib = os.getenv("ORACLE_LIB")
                else:
                    pathlib = string_connect["library"]
            else:
                pathlib = os.getenv("ORACLE_LIB")

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)

            # Definindo o tipo de instancia SID/SERVICE_NAME
            if string_connect["type_conection"].upper() == "SID":
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], sid=string_connect["instance"])
            else:
                dnsName = ora.makedsn(host=string_connect["host"], port=string_connect["port"], service_name=string_connect["instance"])

            # Efetuando a conexao com a instancia do BANCO
            result = ora.connect(string_connect["username"], string_connect["password"], dnsName, threaded=True)
            self._connection_is_valid = True
            self._nome_database = string_connect["database"]
            self._cnn = result
            self.__database_error = f"""{json.dumps(string_connect, indent=4).replace(string_connect["password"], "******")}\nConexao bem sucedida!"""
        except Exception as error:
            msg = f"""{json.dumps(string_connect, indent=4).replace(string_connect["password"], "******")}\nFalha ao tentar se conectar com o banco de dados ORACLE\nException Error: {error} """
            result = msg
            self._connection_is_valid = False
            self.__database_error = msg

        finally:
            return result

    def Connect_SQLA(self, string_connect: dict):
        conn = None
        try:
            # Definindo a Library ORACLE
            if string_connect["path_library"] is None:
                pathlib = os.getenv("ORACLE_LIB")
            else:
                pathlib = string_connect["path_library"]

            # Consistindo se a biblioteca do oracle ja esta iniciada
            try:
                ora.init_oracle_client(lib_dir=pathlib)
            except:
                pass
                # não faz nada (e para deixar assim se nao da erro)
            # Validando se foi passado um driver para conexao
            if string_connect["driver_conexao"] is None:
                string_connect["driver_conexao"] = "cx_oracle"
            database = string_connect["database"]
            driver = string_connect["driver_conexao"]
            user = string_connect["username"]
            pwd = string_connect["password"]
            host = string_connect["host"]
            port = string_connect["port"]
            string_connect["instance"] = ora.makedsn(host, port, string_connect["instance"])
            # Validando o tipo de conexao (SID ou SERVICE_NAME) apenas oracle
            if string_connect["type_conection"].upper() == "SERVICE_NAME":
                string_connect["instance"] = string_connect["instance"].replace("SID", "SERVICE_NAME")
            dnsName = string_connect["instance"]
            str_cnn = f"""{database.lower()}{driver}://{user}:{pwd}@{dnsName}"""
            engine = sqa.create_engine(str_cnn)
            result = engine.connect()
            self._connection_is_valid = True
            self._cnn = result
            self.__database_error = f"""{json.dumps(string_connect, indent=4).replace(string_connect["password"], "******")}\nConexao bem sucedida!"""
            self._nome_database = string_connect["database"]
        except Exception as error:
            msg = f"""{json.dumps(string_connect, indent=4).replace(string_connect["password"], "******")}\nFalha ao tentar se conectar com o banco de dados ORACLE (SqlAlchemy)\nException Error: {error} """
            result = msg
            self._connection_is_valid = False
            self.__database_error = msg
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