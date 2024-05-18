from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="data-files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file} uploaded at {self.uploaded_at}"
    

class CleanedData(models.Model):
    data = models.JSONField()
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)