from django.db import models


class Trace(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    data = models.TextField()
