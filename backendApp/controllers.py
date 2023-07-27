from django.http import JsonResponse
from django.db import connection
import json
import requests
import threading
from .frontendAccess import FrontendAccess

from .DAO import TaskDAO, AccountDAO    #data access objects

class TaskAPI:
    @classmethod
    def tasksOf(self, request):
        if request.method != "GET":
            error = {"Error": "Only GET is allowed"}
            return JsonResponse(error, status=405)

        data = json.loads(request.body)
            
        try:
            username = data["username"]
        except KeyError as e:
            return JsonResponse({"Error": "Account name is missing"}, status=404)

        tasks = TaskDAO.getTasksOf(username)
        account = AccountDAO.getAccount(username)

        if len(tasks) != None:
            taskDict = {"name": account.name, "task": [task.text for task in tasks]}
            return JsonResponse(taskDict, status=200)

        return JsonResponse({"Error": "Account name not found"}, status=404)

    @classmethod
    def addNew(self, request):
        if request.method != "POST":
            error = {"Error": "Only POST is allowed"}
            return JsonResponse(error, status=405)

        data = json.loads(request.body)

        try:
            username = data["username"]
            newTaskText = data["taskText"]
        except KeyError as e:
            return JsonResponse({"Error": "Account name or task text is missing"}, status=404)

        status = TaskDAO.addNewTask(username, newTaskText)
        if status == True:
            return JsonResponse({"Message": "Successfully added task"}, status=201)

        return JsonResponse({"Error": "Account name not found"}, status=404)

    @classmethod
    def delete(self, request):
        if request.method != "DELETE":
            return JsonResponse({"Error": "Only DELETE is allowed"}, status=405)

        data = json.loads(request.body)

        try:
            username = data["username"]
            taskText = data["taskText"]
        except KeyError as e:
            return JsonResponse({"Error": "Account name or task text is missing"}, status=404)

        status = TaskDAO.deleteTask(username, taskText)
        if status == True:
            return JsonResponse({"Message": "Successfully deleted task"}, status=200)

        return JsonResponse({"Error": "Account name or task not found"}, status=404)

class AccountAPI:
    @classmethod
    def authenticate(self, request):
        if request.method != "POST":
            return JsonResponse({"Error": "Only POST is allowed"}, status=405)

        data = json.loads(request.body)

        try:
            accUser = data["username"]
            accPasswd = data["password"]
        except KeyError as e:
            return JsonResponse({"Error": "Missing account infos"}, status=404)

        acc = AccountDAO.getAccount(accUser)
        if acc:
            if acc.password == accPasswd:
                return JsonResponse({"Message": "Successfully loged in"}, status=200)
        return JsonResponse({"Error": "Wrong username or password"}, status=401)

    @classmethod
    def register(self, request):
        if request.method != "POST":
            return JsonResponse({"Error": "Only POST is allowed"}, status=405)

        data = json.loads(request.body)

        try:
            accName = data["accountName"]
            accUser = data["username"]
            accPasswd = data["password"]
        except KeyError as e:
            return JsonResponse({"Error": "Missing account infos"}, status=404)

        status = AccountDAO.createAccount(accName, accUser, accPasswd)
        if status == True:
            return JsonResponse({"Message": "Successfully created account"}, status=200)

        return JsonResponse({"Error": "Account with the username already existed"}, status=409)

class AmfAPI:
    """
    For the sake of high availability management,
    the server exposes API called by SAFplus middleware's proxy component
    """
    @classmethod
    def healthCheck(self, request):
        """
        Call this API to do health check and will return SAFplus error code
        """
        if request.method != "GET":
            return JsonResponse({"Error": "Only GET is allowed"}, status=405)

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                row = cursor.fetchone()
                if row[0] == 1:
                    return JsonResponse({"ClRcT": "0x0"}, status=200)    #CL_OK
                else:
                    return JsonResponse({"ClRcT": "0x04"}, status=500)   #CL_ERR_NOT_EXIST indicating database is not available right now

        except Exception as e:
            return JsonResponse({"ClRcT": "0x04"}, status=500)

    @classmethod
    def becomeActive(self, request):
        """
        Call this API to tell the frontend server to use this active backend server
        """
        if request.method != "POST":
            return JsonResponse({"Error": "Only POST is allowed"}, status=405)

        (status, desc, msg) = FrontendAccess.updateBackendServer()
        if status == 400 or status == 500:
            return JsonResponse({"ClRcT": "0x04"}, status=400)  #frontend server is not available
        elif status == 404:
            return JsonResponse({"ClRcT": "0x0e"}, status=404)  #no settings

        return JsonResponse({"ClRcT": "0x0"}, status=200)

class Utils:
    @staticmethod
    def forwardApiRequest(url, dataDict, method):
        methodLut = {"GET": requests.get,
                     "POST": requests.post,
                     "DELETE": requests.delete}

        sendFunc = methodLut.get(method, None)
        if sendFunc:
            headers = {'Content-Type': 'application/json'}
            sendThrd = threading.Thread(target=_sendCallback, args=(sendFunc, url, dataDict, headers, 2))
            sendThrd.start()
    
    def _sendCallback(sendFunc, url, dataDict, headers, timeout):
        try:
            sendFunc(url, data=json.dumps(dataDict), headers=headers, timeout=2)
        except requests.exceptions.Timeout:
            pass
