from django import forms

from .models import Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('recipe_name', 'image','description', 'difficulty', 'ingredients')
