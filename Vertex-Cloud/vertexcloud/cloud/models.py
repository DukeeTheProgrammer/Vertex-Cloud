from django.db import models
from datetime import datetime
from django.conf import settings


class File(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="static/files")
    type = models.CharField(max_length=50)
    size = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=datetime.utcnow)

