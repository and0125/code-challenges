from django.db import models

# Create your models here.


class Widget(models.Model):
    name = models.CharField(max_length=64)
    number_of_parts = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
