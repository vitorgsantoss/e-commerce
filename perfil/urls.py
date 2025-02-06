from django.urls import path
from . import views


app_name = 'perfil'


urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('enderecos/', views.ListaEnderecos.as_view(), name='listar_enderecos'),
    path('modificar_endereco/<pk>', views.ModificarEndereco.as_view(), name='modificar_endereco'),
    path('criar_endereco/', views.CriarEndereco.as_view(), name='criar_endereco'),
]
