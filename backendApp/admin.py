from django.contrib import admin

# Register your models here.

from .models import Account, Task

admin.site.register(Account)
admin.site.register(Task)
