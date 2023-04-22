from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class MajorItem(models.Model):
    item = models.CharField(max_length=8,blank=False)

    def __str__(self):
        return self.item


class DetailItem(models.Model):
    major = models.ForeignKey(MajorItem, on_delete=models.CASCADE, related_name='item_id')
    items = models.CharField(max_length=20)
    detail = models.CharField(max_length=30,  blank=True)

    def __str__(self):
        return self.items


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_id')
    items = models.ForeignKey(DetailItem, on_delete=models.CASCADE,related_name='detail_item')
    content = models.CharField(max_length=20,blank=False)
    start_time = models.DateTimeField(auto_created=True)
    end_time = models.DateTimeField(auto_created=False, blank=True)
    spend_time = models.FloatField(default=0)

    def __str__(self):
        return self.content



