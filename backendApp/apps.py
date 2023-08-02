from django.apps import AppConfig
from .serverAccess import FrontendAccess, StandbyAccess
import json


class BackendappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendApp'
    def ready(self):
        # load the IP configuations for this backend server
        f = open("backendApp/serverSetting.json", "r")
        content = f.read()
        settingDict = json.loads(content)
        try:
            myIP = settingDict["myIP"]

            frontendDict = settingDict["frontend"]
            frontendIP, frontendPort, frontendProtocol = frontendDict["frontendServerIP"], frontendDict["port"], frontendDict["protocol"]

            standbyDict = settingDict["standby"]
            standByBackendIP, standByBackendPort, standByBackendProtocol = standbyDict["standByBackendServerIP"], standbyDict["port"], standbyDict["protocol"]
        except KeyError as e:
            raise Exception("Missing servers setting info [{0}]".format(str(e)))
        FrontendAccess.updateInfo(frontendIP, frontendPort, frontendProtocol, myIP)
        StandbyAccess.updateInfo(standByBackendIP, standByBackendPort, standByBackendProtocol)
