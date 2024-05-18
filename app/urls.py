from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload-data/", views.upload_data, name="upload_data"),
    path('process_data/<int:pk>/', views.process_data, name='process_data'),
    path('visualize_data/<int:pk>/', views.visualize_data, name='visualize_data'),
    path("profile/", views.profile, name="profile"),
    path("logout", views.signout, name="logout"),
]
