from django.urls import path
from . import views
from .views import CustomTokenObtainView


urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("token/", CustomTokenObtainView.as_view(), name="token_obtain_pair"),
]
