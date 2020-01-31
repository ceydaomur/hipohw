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
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, ListView
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
    print(frequent_list)
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
    paginator = Paginator(recipe_list, 2)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    context = {
        'recipe_list': recipe_list,
        'ingredient': ingredient,
        'list':list,
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

class SearchResultsView(ListView):
    model = Recipe
    #paginate_by = 2
    template_name = 'recipe/search_results.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        #check = "," in query

        query_list = query.split(",")
        q_object = Q(recipe_name__icontains=query_list[0]) | Q(description__icontains=query_list[0])| Q(ingredients__name__icontains=query_list[0])
        for item in query_list:
            q_object.add( (Q(recipe_name__icontains=item) | Q(description__icontains=item)| Q(ingredients__name__icontains=item)), q_object.connector)
        first_list = Recipe.objects.filter(q_object)
        #else:
            #first_list = Recipe.objects.filter(Q(recipe_name__icontains=query) | Q(description__icontains=query) | Q(ingredients__name__icontains=query))
        #first_list = Recipe.objects.filter((recipe_name__in=query_list)| (description__in= query_set)|(ingredients__name__in= query_set))
        count = first_list.count()
        object_list = first_list.annotate(num = Count('recipe_name')).order_by('-num')[:count]
        return object_list
