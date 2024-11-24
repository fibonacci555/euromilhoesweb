from django.db import models

# Create your models here.

class EuromilhoesPredict(models.Model):
    region = models.CharField(max_length=100)
    number = models.IntegerField()
    lucky_stars = models.IntegerField()
