import requests, json
import threading

class RequestUtils:
    invalidIP = "255.255.255.255"
    wellKnownStatus = {
        200: "OK",
        201: "Created",
        400: "Request timed out",
        401: "Unauthorized",
        404: "Not found",
        405: "Method not allowed",
        409: "Conflict",
        500: "Internal server error"
    }
    wellKnowMethod = {
        "get": requests.get,
        "post": requests.post,
        "delete": requests.delete
    }

    @staticmethod
    def getServerAddress(serverIP, port, protocol):
        return "{0}://{1}:{2}/".format(protocol, serverIP, port)

    @staticmethod
    def request(url, method, data, headers, timeout):
        if RequestUtils.invalidIP in url:
            return (404, RequestUtils.wellKnownStatus[404], {"Error": "No frontend server set"})

        try:
            sendMethod = RequestUtils.wellKnowMethod[method]
            print(url)
            response = sendMethod(url, data=data, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            return (400, RequestUtils.wellKnownStatus[400], {"Error": "frontend server took too long make response"})
        except requests.exceptions.ConnectionError:
            return (500, RequestUtils.wellKnownStatus[500], {"Error": "Frontend server is not available right now"})

        data = response.json()
        status = response.status_code
        return (status, RequestUtils.wellKnownStatus.get(status, ""), data)

class BaseAccess:
    remoteIP = RequestUtils.invalidIP
    protocol = "http"
    port = "8000"
    headers = {'Content-Type': 'application/json'}
    timeout = 2

class FrontendAccess(BaseAccess):
    myIP = RequestUtils.invalidIP

    @staticmethod
    def updateInfo(remoteIP, port, protocol, myIP):
        FrontendAccess.myIP = myIP
        FrontendAccess.remoteIP = remoteIP
        FrontendAccess.port = port
        FrontendAccess.protocol = protocol

    @staticmethod
    def updateBackendServer():
        if FrontendAccess.myIP == RequestUtils.invalidIP:
            return (404, "Not found", {"Error": "Settings not found"})

        print("remote ip" + FrontendAccess.remoteIP)
        print("my ip" + FrontendAccess.myIP)
        addr = RequestUtils.getServerAddress(FrontendAccess.remoteIP, FrontendAccess.port, FrontendAccess.protocol)
        url = addr + "todo-list/controller/backendServerUpdate/"
        data = {"backendServerIP": FrontendAccess.myIP, "protocol": FrontendAccess.protocol, "port": FrontendAccess.port}

        return RequestUtils.request(url, "post", json.dumps(data), FrontendAccess.headers, FrontendAccess.timeout)

class StandbyAccess(BaseAccess):
    @staticmethod
    def updateInfo(remoteIP, port, protocol):
        StandbyAccess.remoteIP = remoteIP
        StandbyAccess.port = port
        StandbyAccess.protocol = protocol

    @staticmethod
    def forwardApiRequest(apiPath, dataDict, method):
        url = RequestUtils.getServerAddress(StandbyAccess.remoteIP, StandbyAccess.port, StandbyAccess.protocol)
        url += apiPath

        sendThrd = threading.Thread(target=StandbyAccess._sendCallback, args=(url, method, dataDict))
        sendThrd.start()

    @staticmethod
    def _sendCallback(url, method, dataDict):
        #TODO: if no standby, just drop the request?
        RequestUtils.request(url, method, json.dumps(dataDict), StandbyAccess.headers, StandbyAccess.timeout)
