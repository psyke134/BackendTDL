from .models import Account, Task
import datetime

class TaskDAO:
    @staticmethod
    def getTasksOf(username):
        acc = AccountDAO.getAccount(username)
        if not acc:
            return None
        rs = Task.objects.filter(owner=acc)
        return rs
    
    @staticmethod
    def addNewTask(username, taskText):
        acc = AccountDAO.getAccount(username)
        if not acc:
            return False
        newTask = Task(owner=acc, text=taskText)
        newTask.save()
        return True

    @staticmethod
    def deleteTask(username, taskText):
        acc = AccountDAO.getAccount(username)
        if not acc:
            return False

        task = TaskDAO.getTask(acc, taskText)
        if not task:
            return False

        task.delete()
        return True

    @staticmethod
    def getTask(account, taskText):
        try:
            task = Task.objects.filter(text=taskText).filter(owner=account).first()
        except Task.DoesNotExist:
            return None
        return task

class AccountDAO:
    @staticmethod
    def createAccount(name, username, password):
        existed = AccountDAO.getAccount(username)
        if existed:
            return False

        now = datetime.datetime.now()
        newAccount = Account(name=name, username=username, password=password, reg_date=now)
        newAccount.save()
        return True

    @staticmethod
    def getAccount(username):
        try:
            acc = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return None
        return acc
