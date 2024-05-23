# from django.forms import ModelForm
# from . import models


# class UploadFileForm(ModelForm):
#     class Meta:
#         model = models.UploadedFile
#         fields = ["file"]


from django import forms 
from django.contrib.auth.forms import UserCreationForm
from . import models

class UploadFileForm(forms.Form):
    file = forms.FileField()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.CustomUser
        fields = ["username"]