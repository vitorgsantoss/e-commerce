from django.urls import path
from . import views


app_name = 'pedido'


urlpatterns = [
    path('fecharpedido/', views.FecharPedido.as_view() ,name='fecharpedido'),
    path('listapedidos/', views.ListaPedidos.as_view() ,name='listapedidos'),
    path('detalhe/<pk>/', views.Detalhe.as_view() ,name='detalhe'),
    path('<pk>/', views.Pagar.as_view() ,name='pagar'),
]
