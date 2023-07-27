from django.apps import AppConfig
from .frontendAccess import FrontendAccess
import json


class BackendappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendApp'
    def ready(self):
        f = open("backendApp/frontendSetting.json", "r")
        content = f.read()
        settingDict = json.loads(content)
        try:
            frontendServerIP, myIP, port, protocol = settingDict["frontendServerIP"], settingDict["myIP"], settingDict["port"], settingDict["protocol"]
        except KeyError as e:
            raise Exception("Missing frontend setting info [{0}]".format(str(e)))
        FrontendAccess.updateInfo(frontendServerIP, port, protocol, myIP)
