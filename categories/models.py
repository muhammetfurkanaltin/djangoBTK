from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null = True) 

    def __str__(self):
        return self.name