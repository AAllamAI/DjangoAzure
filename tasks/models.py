from django.db import models


class Task(models.Model):
    title = models.CharField("العنوان", max_length=200)
    description = models.TextField("الوصف", blank=True)
    is_completed = models.BooleanField("مكتملة", default=False)
    created_at = models.DateTimeField("تاريخ الإنشاء", auto_now_add=True)
    updated_at = models.DateTimeField("آخر تحديث", auto_now=True)

    class Meta:
        ordering = ["is_completed", "-created_at"]

    def __str__(self):
        return self.title
