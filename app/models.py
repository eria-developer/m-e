from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    fullname  = models.CharField(max_length=64)


class UploadedFile(models.Model):
    file = models.FileField(upload_to="data-files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file} uploaded at {self.uploaded_at}"                                                
    

class CleanedData(models.Model):
    data = models.JSONField()
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DataOne(models.Model):
    baseline_ID = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    training_received = models.CharField(max_length=64, null=True, blank=True)
    form_of_land_access = models.CharField(max_length=64, null=True, blank=True)
    source_of_seed = models.CharField(max_length=64, null=True, blank=True)
    main_channel_of_selling = models.CharField(max_length=64, null=True, blank=True)
    major_transition_method = models.CharField(max_length=64, null=True, blank=True)
    main_outlet = models.CharField(max_length=64, null=True, blank=True)
    distance_to_market_km = models.DecimalField(decimal_places=2, max_digits=8, null=True, blank=True)
    major_transport_means = models.CharField(max_length=64, null=True, blank=True)
    transport_cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.baseline_ID}"