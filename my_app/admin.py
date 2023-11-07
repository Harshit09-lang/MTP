from django.contrib import admin
from .models import MLmodel,Data
# Register your models here.

@admin.register(MLmodel)
class MLfileAdmin(admin.ModelAdmin):
    list_display = ['id','ml_file']

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ['id','data']