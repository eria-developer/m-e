from django.contrib import admin
from . import models

admin.site.register(models.UploadedFile)
admin.site.register(models.CleanedData)
admin.site.register(models.DataOne)