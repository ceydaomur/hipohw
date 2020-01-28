from django.shortcuts import render, redirect
from .models import Recipe, Ingredient, Vote
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('recipe_list')
    return render(request, 'registration/signup.html', {'form': form})

def vote_recipe(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    choice = request.POST.get('recipe')
    ch = Vote.objects.create(recipe=detail, user=request.user, rating=choice)
    ingredient_list = Ingredient.objects.filter(recipe__id=pk)
    return render(request, 'recipe/detail.html', {'detail':detail,  'ingredient_list': ingredient_list, 'choice':choice} )


def like_recipe(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    detail.likes.add(request.user)
    detail.save()
    is_voted=False
    ingredient_list = Ingredient.objects.filter(recipe__id=pk)
    if detail.votes.filter(pk=request.user.id).exists():
        is_voted = True
    #return redirect('detail', pk=request.pk)
    return render(request, 'recipe/detail.html', {'detail':detail, 'ingredient_list': ingredient_list, 'is_voted': is_voted,} )


def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-creation_time')
    #object_list = Recipe.objects.all()
    paginator = Paginator(recipes, 2)  # 2 posts in each page
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        list = paginator.page(paginator.num_pages)
    return render(request, 'recipe/recipe_list.html', {'recipes':recipes,'list': list})


def detail(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    ingredient_list = Ingredient.objects.filter(recipe__id=pk)
    is_liked = False
    is_voted = False
    if detail.likes.filter(pk=request.user.id).exists():
        is_liked = True
    if detail.votes.filter(pk=request.user.id).exists():
        is_voted = True
    context = {
        'detail': detail,
        'ingredient_list': ingredient_list,
        'is_liked': is_liked,
        'is_voted': is_voted,
    }
    return render(request, 'recipe/detail.html', context)

@login_required
def recipe_new(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.creation_time = timezone.now()
            recipe.save()
            return redirect('detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    return render(request, 'recipe/recipe_edit.html', {'form': form})
