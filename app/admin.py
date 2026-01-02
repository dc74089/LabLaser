from django.contrib import admin

from app.models import TemplateFile, CustomizedFile

# Register your models here.
admin.site.register(TemplateFile)
admin.site.register(CustomizedFile)