

class SQL:
    def __init__(self):
        ...

    @staticmethod
    def colunas_cursor(cursor) -> list:
        header = [head[0] for head in cursor.description]
        return header

    @staticmethod
    def Crud(sql: str = None, values: dict = None, conexao=None, commit: bool = True):
        msg, result, linhas_afetadas = None, [], 0
        try:
            if not isinstance(sql, str) or sql is None:
                raise Exception(f"""Comando sql não foi definido {sql}""")
            if conexao is None:
                raise Exception(f"""Conexão não foi informada {conexao}""")
            if not isinstance(values, dict):
                raise Exception(f"""Lista de valores não foi informada {values}""")
            cursor = conexao.cursor()
            cursor.execute(sql, values)
            linhas_afetadas = cursor.rowcount
            cursor.close()
            if commit:
                conexao.commit()
            msg = f"""Comando SQL executado com sucesso!"""
        except Exception as error:
            msg = f"""Falha ao tentar executar o comando SQL! Erro: {error}"""
            result = msg
        finally:
            result = {"linhas_afetadas": linhas_afetadas, "mensagem": msg, "sql": sql}
            return result