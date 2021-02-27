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


class Reason(models.Model):
    purpose = models.CharField(max_length=25)

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse('reasons')


class Message(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'message from {self.email}'

    def get_absolute_url(self):
        return reverse('home')
