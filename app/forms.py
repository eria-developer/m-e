from django.forms import ModelForm
from . import models

class UploadFileForm(ModelForm):
    class Meta:
        model = models.UploadedFile
        fields = ["file"]