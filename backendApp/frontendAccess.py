import requests, json

class FrontendAccess:
    invalidIP = "255.255.255.255"
    frontendServerIP = invalidIP
    myIP = invalidIP
    protocol = "http"
    port = "8000"
    headers = {'Content-Type': 'application/json'}
    timeout = 2
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
    def updateInfo(frontendServerIP, port, protocol, myIP):
        FrontendAccess.frontendServerIP = frontendServerIP
        FrontendAccess.port = port
        FrontendAccess.protocol = protocol
        FrontendAccess.myIP = myIP

    @staticmethod
    def getServerAddress():
        return "{0}://{1}:{2}/".format(FrontendAccess.protocol, FrontendAccess.backendServerIP, FrontendAccess.port)

    @staticmethod
    def request(url, method, data, headers, timeout):
        if FrontendAccess.frontendServerIP == FrontendAccess.invalidIP:
            return (404, BackendAccess.wellKnownStatus[404], {"Error": "No frontend server set"})

        try:
            sendMethod = FrontendAccess.wellKnowMethod[method]
            response = sendMethod(url, data=data, headers=headers, timeout=timeout)
        except requests.exceptions.Timeout:
            return (400, BackendAccess.wellKnownStatus[400], {"Error": "frontend server took too long make response"})
        except requests.exceptions.ConnectionError:
            return (500, BackendAccess.wellKnownStatus[500], {"Error": "Frontend server is not available right now"})

        data = response.json()
        status = response.status_code
        return (status, FrontendAccess.wellKnownStatus.get(status, ""), data)

    @staticmethod
    def updateBackendServer():
        if FrontendAccess.myIP == FrontendAccess.invalidIP:
            return (404, "Not found", {"Error": "Settings not found"})

        addr = FrontendAccess.getServerAddress()
        url = addr + "frontend/backendServerUpdate/"
        data = {"backendServerIP": FrontendAccess.myIP, "protocol": FrontendAccess.protocol, "port": FrontendAccess.port}

        return BackendAccess.request(url, "post", json.dumps(data), BackendAccess.headers, BackendAccess.timeout)
