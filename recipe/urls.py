from django.urls import path
from . import views
#from recipe.views import CreateRecipeview

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.detail, name='detail'),
    path('recipes/new/', views.CreateRecipeView.as_view(), name='recipe_new'),
    path('<int:pk>/like/',views.like_recipe,name='like_recipe'),
    path('<int:pk>/vote/',views.vote_recipe,name='vote_recipe'),
    path('recipes/<int:pk>/edit/', views.EditRecipeView.as_view(), name='recipe_edit'),
    path('recipes/<int:pk>/delete/', views.DeleteRecipeView.as_view(), name='recipe_delete'),
    path('<int:pk>/top_used/', views.ingredient_detail, name='ingredient_detail'),
]
