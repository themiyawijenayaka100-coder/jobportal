from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    company = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def employer(self):
        return self.created_by

    def __str__(self):
        return self.title


class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title