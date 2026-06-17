from django.urls import path
from Admins.views import *

urlpatterns = [
    path('adminhome/', adminhome, name='adminhome'),
    path('admin_update_userstatus/<int:user_id>/', admin_update_userstatus, name='admin_update_userstatus'),
    path('deduplicated_files/', deduplicated_files, name="deduplicated_files"),
    path('audit/<int:file_id>/', audit_file, name="audit_file"),

]