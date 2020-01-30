from django.shortcuts import render, redirect
from .models import Recipe, Ingredient, Vote
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from .forms import RecipeForm
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Recipe
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.views.generic.edit import DeleteView
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
    frequent_list = Ingredient.objects.all().annotate(num = Count('recipes')).order_by('-num')[:5]
    username = None
    if request.user.is_authenticated:
       username = request.user.username
    paginator = Paginator(recipes, 2)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return render(request, 'recipe/recipe_list.html', {'recipes':recipes,'list': list, 'username':username, 'frequent_list': frequent_list})

def ingredient_detail(request,pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    recipe_list = ingredient.recipes.all()
    context = {
        'recipe_list': recipe_list,
        'ingredient': ingredient,
    }
    return render(request, 'recipe/ingredient_detail.html', context)

def detail(request, pk):
    detail = get_object_or_404(Recipe, pk=pk)
    ingredient_list = Ingredient.objects.filter(recipes__id=pk)
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
    return render(request, 'recipe/detail.html', context)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

class CreateRecipeView(LoginRequiredMixin,CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_edit.html'

    def form_valid(self, form):
        author = self.request.user
        form.instance.author = author
        return super(CreateRecipeView, self).form_valid(form)

class EditRecipeView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/recipe_edit.html'

    def form_valid(self, form):
        return super(EditRecipeView, self).form_valid(form)

class DeleteRecipeView(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe_list')
