from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload-data/", views.upload_data, name="upload_data"),
    path("profile/", views.profile, name="profile"),
    path("logout", views.signout, name="logout"),
]
