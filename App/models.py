from django.db import models
from django.contrib.auth.models import User

class Transcript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    transcript = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


