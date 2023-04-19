from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, verbose_name='Завдання')
    description = models.TextField(null=True, blank=True, verbose_name='Опис')
    complete = models.BooleanField(default=False, verbose_name='Виконано')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete', '-updated']
