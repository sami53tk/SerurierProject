from django.db import models
from django.contrib.auth.models import User

# Create your models here.
RATING_CHOICES = [(i, i) for i in range(1, 5)]
class Avis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentaire = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f'Avis de {self.user}'
    


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.full_name}"
