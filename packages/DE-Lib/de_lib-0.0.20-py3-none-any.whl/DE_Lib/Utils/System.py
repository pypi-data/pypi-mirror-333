import os
import signal
import socket as skt
import platform as so

class SO:
    def __init__(self):
        self.__msg = {} # mensagems para funcionalidades


    def ping(self, hostname) -> bool:
        msg, result = None, False
        # hostname = "google.com"  # example
        response = os.system("ping -n 1 " + hostname + " >> trash_ping.log")
        # and then check the response...
        if response == 0:
            self.__msg["ping"] = f"""{hostname} Sucesso!"""
            result = True
        else:
            self.__msg["ping"] = f"""{hostname} Não encontrado!"""
        return result

    def killPID(self, pid):
        msg, result = None, True
        try:
            os.kill(pid, signal.SIGKILL)
            self.__msg["pid"] = "PID eliminado!"
        except Exception as error:
            self.__msg["pid"] = f"""Erro ao tentar eliminar o PID!\n{error}"""
            result = False
        finally:
            return result

    @property
    def PID(self):
        return os.getpid()

    @property
    def OSINFO(self):
        result = {"user_db": None,
                  "local_ip": skt.gethostbyname(skt.gethostname()),
                  "local_name": skt.gethostname(),
                  "processor": so.machine(),
                  "os_user": os.getlogin(),
                  "so_platform": so.platform(),
                  "so_system": so.system(),
                  "so_version": so.version()
                  }
        return result

