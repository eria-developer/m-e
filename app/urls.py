from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from . import report_pdf

# urlpatterns = [
#     path("", views.home, name="home"),
#     path("upload-data/", views.upload_data, name="upload_data"),
#     path('process_data/<int:pk>/', views.process_data, name='process_data'),
#     path('visualize_data/<int:pk>/', views.visualize_data, name='visualize_data'),
#     path("profile/", views.profile, name="profile"),
#     path("logout", views.signout, name="logout"),


#     path("upload_file/", views.upload_file, name="upload_file"),
# ]


urlpatterns = [
    path("", views.home, name="home"),
    path("upload-data/", views.upload_file, name="upload_data"),
    path('process_data/', views.process_data, name='process_data'),
    path('visualize_data/<int:pk>/', views.visualize_data, name='visualize_data'),
    path("profile/", views.profile, name="profile"),
    path("logout", views.signout, name="logout"),

    path("user_signup/", views.user_signup, name="user_signup"),
    path("user_login/", views.user_login, name="user_login"),
    path("generate_report", report_pdf.generate_report, name="generate_report"),


    path("upload_file/", views.upload_file, name="upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)