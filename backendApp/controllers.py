from django.http import JsonResponse
from django.db import connection
import json

from .DAO import TaskDAO, AccountDAO    #data access objects

class TaskAPI:
    @classmethod
    def tasksOf(self, request):
        if request.method != "GET":
            error = {"error": "Method not allowed"}
            return JsonResponse(error, status=405)

        data = json.loads(request.body)
            
        try:
            accName = data["accountName"]
        except KeyError as e:
            return JsonResponse({"error": "Account name is missing"}, status=404)

        tasks = TaskDAO.getTasksOf(accName)

        if len(tasks) != 0:
            taskDict = {"name": accName, "task": [task.text for task in tasks]}
            return JsonResponse(taskDict, status=200)

        return JsonResponse({"error": "Account name not found"}, status=404)

    @classmethod
    def addTask(self, request):
        if request.method != "POST":
            error = {"error": "Method not allowed"}
            return JsonResponse(error, status=405)

        data = json.loads(request.body)

        try:
            accName = data["accountName"]
            newTaskText = data["taskText"]
        except KeyError as e:
            return JsonResponse({"error": "Account name or task text is missing"}, status=404)

        status = TaskDAO.addNewTask(accName, newTaskText)
        if status == True:
            return JsonResponse({"Message": "Scuessfully added task"}, status=201)

        return JsonResponse({"error": "Account name not found"}, status=404)

    @classmethod
    def deleteTask(self, request):
        if request.method != "DELETE":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        data = json.loads(request.body)

        try:
            accName = data["accountName"]
            taskText = data["taskText"]
        except KeyError as e:
            return JsonResponse({"error": "Account name or task text is missing"}, status=404)

        status = TaskDAO.deleteTask(accName, taskText)
        if status == True:
            return JsonResponse({"Message": "Scuessfully deleted task"}, status=200)

        return JsonResponse({"error": "Account name or task not found"}, status=404)

class AmfAPI:
    @classmethod
    def healthCheck(self, request): #this API will be pinged by SAFplus middleware's proxy component to do health check
        if request.method != "GET":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                row = cursor.fetchone()
                if row[0] == 1:
                    return JsonResponse({"ClRcT": "0x0"}, status=200)    #CL_OK
                else:
                    return JsonResponse({"ClRcT": "0x04"}, status=500)   #CL_ERR_NOT_EXIST indicating database if not available right now

        except Exception as e:
            return JsonResponse({"ClRcT": "0x04"}, status=500)

