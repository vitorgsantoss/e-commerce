from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto
from django.http import HttpResponse


class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6


class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, request, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
            )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto não existe!')

            return redirect(http_referer)
        
        if not self.request.session['carrinho']:
            self.request.session['carrinho']= {}

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            pass

        else: 
            pass


        return HttpResponse('Adicionar ao carrinho')

class RemoverDoCarrinho(View):
    ... 


class Carrinho(View):
    ...


class Finalizar(View):
    ...