from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(user_data)
admin.site.register(task)
admin.site.register(task_user)
admin.site.register(machine)
admin.site.register(maintenance)
