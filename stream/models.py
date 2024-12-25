import uuid
from django.db import models

class Stream(models.Model):
    title = models.CharField(max_length=250)
    unique_key = models.CharField(max_length=36, unique=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.title
