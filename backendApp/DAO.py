from .models import Account, Task

class TaskDAO:
    @staticmethod
    def getTasksOf(accountName):
        acc = AccountDAO.getAccount(accountName)
        if not acc:
            return []
        rs = Task.objects.filter(owner=acc)
        return rs;
    
    @staticmethod
    def addNewTask(accountName, taskText):
        acc = AccountDAO.getAccount(accountName)
        if not acc:
            return False
        newTask = Task(owner=acc, text=taskText)
        newTask.save()
        return True

    @staticmethod
    def deleteTask(accountName, taskText):
        acc = AccountDAO.getAccount(accountName)
        if not acc:
            return False

        task = TaskDAO.getTask(taskText)
        if not task:
            return False

        task.delete()
        return True

    @staticmethod
    def getTask(taskText):
        try:
            task = Task.objects.get(text=taskText)
        except Task.DoesNotExist:
            return None
        return task

class AccountDAO:
    @staticmethod
    def getAccount(accountName):
        try:
            acc = Account.objects.get(name=accountName)
        except Account.DoesNotExist:
            return None
        return acc
