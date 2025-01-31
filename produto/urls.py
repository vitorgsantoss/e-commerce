from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), 
        name='adicionaraocarrinho'),
    path('removerprodutodocarrinho/', views.RemoverProdutoDoCarrinho.as_view(),
        name='removerprodutodocarrinho'),
    path('removervariacaocarrinho/', views.RemoverVariacaoDoCarrinho.as_view(),
        name='removervariacaocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
    path('<slug>/', views.DetalheProduto.as_view(), name='detalhe'),
]
