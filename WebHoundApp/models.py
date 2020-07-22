from django.db import models


class Trace(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    was_traced = models.BooleanField(default=False)
    is_task_active = models.BooleanField(default=False)
    task_active_ts = models.DateTimeField(null=True)
    name = models.CharField(max_length=200, primary_key=True)
    data = models.TextField(default={})

    def __str__(self):
        return f"{self.date} | {self.was_traced} | {self.name} | {len(self.data)}"
