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
    #is_voted = False
    choice = request.POST.get('recipe')
    Vote.objects.create(recipe=detail, user=request.user, rating=choice)
    '''if detail.votes.filter(pk=request.user.id).exists():
        is_voted = True
    if is_voted == True:
        print("You chosed", choice )'''
    return redirect('detail', pk=pk)

def like_recipe(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    is_liked = False
    if detail.likes.filter(pk=request.user.id).exists():
        is_liked = True
    if is_liked == False:
        detail.likes.add(request.user)
        detail.save()
    else:
        detail.likes.remove(request.user)
        detail.save()
    return redirect('detail', pk=pk)

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-creation_time')
    paginator = Paginator(recipes, 2)  # 2 posts in each page
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'recipe/recipe_list.html', {'recipes':recipes,'list': list})


def detail(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    ingredient_list = Ingredient.objects.filter(recipe__id=pk)
    is_voted = False
    chosen = 0
    if detail.votes.filter(user__pk=request.user.id).exists():
        is_voted = True
        ch = detail.votes.filter(user__pk=request.user.id)
        chosen= ch[0].rating
    context = {
        'detail': detail,
        'ingredient_list': ingredient_list,
        'is_voted': is_voted,
        'chosen':chosen,
    }
    print(detail.author)
    print(detail.difficulty)
    print(detail.ingredients)
    print(ingredient_list)
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
