from django.db import models

class Taboo(models.Model):
    word = models.CharField(max_length = 100)