from django.urls import path
from Users.views import *

urlpatterns = [
    path('userhome/', userhome, name='userhome'),
    path('upload_file/', upload_file, name="upload_file"),
    path('view_files/', view_files, name="view_files"),
]