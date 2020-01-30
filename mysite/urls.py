
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf.urls import *
from django.conf import settings
from recipe.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipe.urls')),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup_view, name="signup")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
