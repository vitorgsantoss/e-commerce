from django.urls import path
from . import views


app_name = 'perfil'


urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('atualizar/', views.Criar.as_view(), name='atualizar'),
    path('login/', views.Criar.as_view(), name='login'),
    path('logout/', views.Criar.as_view(), name='logout'),
]
