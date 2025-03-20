from cryptography.fernet import Fernet
import os
import json

class FERNET:
    def __init__(self):
        self.__token = None
        self.__cipher = None

    # -----------------------------------
    def encrypt(self, word:str, token: str):
        msg, result = None, None
        try:
            #x = Fernet(key)
            result = self.CIPHER.encrypt(word.encode())
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result

    # ----------------------------------
    def decrypt(self, word):
        msg, result = None, True
        try:
            result = self.CIPHER.decrypt(word).decode()
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result


    # ----------------------------------
    def setBuildToken(self):
        # normalmente sera gerado apenas uma unica vez
        # armazenar a chave. Caso seja gerado uma outra
        # todas as criptografias geraradas anteriormente
        # serao perdidas.
        msg, result = None, True
        try:
            self.__token = Fernet.generate_key()
            result = self.TOKEN
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result

    # ----------------------------------
    def setToken(self, token):
        msg, result = None, True
        try:
            self.__token = token
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result


    # ----------------------------------
    def __setCipher(self, key):
        msg, result = None, True
        try:
            self.__cipher = Fernet(key)
        except Exception as error:
            msg = error
            result = msg
        finally:
            return result


    @property
    def TOKEN(self) -> str:
        return self.__token

    @property
    def CIPHER(self):
        return Fernet(self.TOKEN)

