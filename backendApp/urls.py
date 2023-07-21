from django.urls import path

from . import controllers

urlpatterns = [
        path("Task/", controllers.TaskAPI.tasksOf, name="TasksOf"),
        path("Task/AddNew/", controllers.TaskAPI.addTask, name="AddTask"),
        path("Task/Delete/", controllers.TaskAPI.deleteTask, name="DeleteTask"),
        path("AMF/HealthCheck/", controllers.AmfAPI.healthCheck, name="HealthCheck"),
]
