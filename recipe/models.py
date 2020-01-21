from django.conf import settings
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

class desert(models.Model):
    recipe_name = models.CharField(max_length=400)
    image = models.ImageField()
    description = models.TextField()
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'More Effort'),
        ('Hard', 'A challenge'),
    ]
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
    )
    INGREDIENT_CHOICES = [
        ('Coffee Granules', 'Coffee Granules'),
        ('Vanilla', 'Vanilla'),
        ('Mascarpone', 'Mascarpone'),
        ('Milk', 'Milk'),
        ('Sponge fingers', 'Sponge fingers'),
        ('Mascarpone', 'Mascarpone'),
        ('Coffee Liqueur', 'Coffee Liqueur'),
        ('Sugar', 'Sugar'),
        ('Egg', 'Egg'),
        ('Orange', 'Orange'),
        ('Cream', 'Cream'),
        ('Raspberrries', 'Raspberries'),
        ('Egg Whites', 'Egg Whites'),
        ('Pistachio', 'Pistachio'),
    ]
    ingredients = MultiSelectField(
        max_choices=10,
        choices=INGREDIENT_CHOICES,
    )

    def __str__(self):
        return self.recipe_name
