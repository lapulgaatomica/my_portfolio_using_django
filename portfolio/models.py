from django.db import models
from django.urls import reverse

class About(models.Model):
    paragraph = models.TextField(max_length=400)

    def __str__(self):
        return self.paragraph[:30]

    def get_absolute_url(self):
        return reverse('home')

class Competency(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

    def get_absolute_url(self):
        return reverse('home')
