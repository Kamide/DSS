from django.db import models


# taboo table - essentially 1D list stored in database
class Taboo(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word