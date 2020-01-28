from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('recipes/new/', views.recipe_new, name='recipe_new'),
    path('<int:pk>/like/',views.like_recipe,name='like_recipe'),
    path('<int:pk>/vote/',views.vote_recipe,name='vote_recipe'),
]
