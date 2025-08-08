from django.db import models

#classe para o autor do livro
class Autor(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True)
    bio = models.TextField()