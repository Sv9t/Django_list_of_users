from django.contrib import admin
from .models import TableUsers, TableStat, UsersShtat
# Register your models here.

admin.site.register(TableUsers)
admin.site.register(TableStat)
admin.site.register(UsersShtat)