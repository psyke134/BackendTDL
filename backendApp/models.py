from django.db import models

# Create your models here.

class Account(models.Model):
    name = models.CharField(max_length = 30)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    reg_date = models.DateTimeField()

    def __str__(self):
        return self.name

class Task(models.Model):
    owner = models.ForeignKey(Account, on_delete = models.CASCADE)
    text = models.CharField(max_length = 300)

    def __str__(self):
        return self.text

