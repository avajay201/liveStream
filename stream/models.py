import uuid
from django.db import models
from django.contrib.auth.models import User

class Stream(models.Model):
    title = models.CharField(max_length=250)
    unique_key = models.CharField(max_length=36, unique=True, editable=False, default=uuid.uuid4)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chat(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
