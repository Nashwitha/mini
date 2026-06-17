from django.db import models
from django.contrib.auth.models import User
import os

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_hash = models.CharField(max_length=256)
    blockchain_tx = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    @property
    def extension(self):
        name, extension = os.path.splitext(self.file_name)
        return extension.lower()