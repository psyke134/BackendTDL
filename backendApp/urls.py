from django.urls import path

from . import controllers

urlpatterns = [
        path("task/", controllers.TaskAPI.tasksOf, name="TasksOf"),
        path("task/addNew/", controllers.TaskAPI.addNew, name="AddTask"),
        path("task/delete/", controllers.TaskAPI.delete, name="DeleteTask"),
        path("account/register/", controllers.AccountAPI.register, name="Register"),
        path("account/login/", controllers.AccountAPI.login, name="Login"),
        path("amf/healthCheck/", controllers.AmfAPI.healthCheck, name="HealthCheck"),
        path("amf/becomeActive/", controllers.AmfAPI.becomeActive, name="BecomeActive"),
]
