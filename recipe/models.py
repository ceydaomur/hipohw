from django.conf import settings
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from django.db.models import Avg

class Ingredient(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Recipe(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=400)
    image = models.ImageField(upload_to='static/img/', blank=True,null=True)
    description = models.TextField()
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def total_likes(self):
        return self.likes.count()

    def total_votes(self):
        return self.votes.count()

    def average(self):
        return self.votes.all().aggregate(Avg('rating'))['rating__avg']

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium','More Effort'),
        ('Hard', 'A challenge'),
    ]
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
    )
    ingredients = models.ManyToManyField('Ingredient')
    creation_time= models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.recipe_name

    class Meta:
        ordering = ['creation_time']

class Vote(models.Model):
    VOTE_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'))
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name = 'votes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name = 'votes')
    rating = models.CharField(
        max_length=5,
        choices=VOTE_CHOICES,
        default = 3,
    )
