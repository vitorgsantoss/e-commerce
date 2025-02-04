from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404, get_list_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from .models import Produto, Variacao
from perfil.models import Perfil, Endereco



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
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
            )
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(
                self.request, 
                'Produto não existe!'
            )
            return redirect(http_referer)
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        variacao_id = variacao_id
        preco_unitario  = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        slug  = produto.slug
        imagem  = produto.imagem.name or ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque Insuficiente'
            )
            return redirect(http_referer)
        
       
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if quantidade_carrinho > variacao.estoque:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente, {produto_nome} adicionado ao '
                    f'carrinho {carrinho[variacao_id]["quantidade"]}x'
                )
                return redirect('produto:lista')
            
            carrinho[variacao_id]['quantidade']=quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = quantidade_carrinho*\
            carrinho[variacao_id]['preco_unitario']
            carrinho[variacao_id]['preco_quantitativo_promocional'] = quantidade_carrinho*\
            carrinho[variacao_id]['preco_unitario_promocional']
            

        else: 
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id' : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo' : preco_unitario,
                'preco_quantitativo_promocional' : preco_unitario_promocional,
                'quantidade' : 1,
                'slug' : slug,
                'imagem' : imagem,
            }
        self.request.session.save()

        return redirect(
            'produto:carrinho',            
        )
            
            
            
class RemoverVariacaoDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:carrinho')
            )
        
        variacao_id = self.request.GET.get('vid')
       
        carrinho = self.request.session.get('carrinho')

        if not carrinho:
            return redirect(http_referer)
        
        if not variacao_id:
            return redirect(http_referer)
        
        if not variacao_id in carrinho:
            return redirect(http_referer)
       
        
        messages.success(
            self.request,
            'Produto removido com sucesso!'
            )
        
        
        self.request.session['carrinho'][variacao_id]['quantidade'] -= 1

        if carrinho[variacao_id]['quantidade'] == 0:
            del self.request.session['carrinho'][variacao_id]

        self.request.session.save()

        return redirect(
            'produto:carrinho'
        )
    

class RemoverProdutoDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
            )
        
        variacao_id = self.request.GET.get('vid')
       
        carrinho = self.request.session.get('carrinho')

        if not carrinho:
            return redirect(http_referer)
        
        if not variacao_id:
            return redirect(http_referer)
        
        if not variacao_id in carrinho:
            return redirect(http_referer)
        
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()

        messages.success(
            self.request,
            'Produto removido com sucesso!'
            )

        return redirect(
            'produto:carrinho'
        )
        

class Carrinho(View):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho')
        return render(
            self.request,
            'produto/carrinho.html',
            {
                'carrinho': carrinho,
            }

        )


class Finalizar(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, 
                'Usuário não logado!'
            )
            return redirect('perfil:criar')

        usuario = Perfil.objects.select_related('usuario').get(usuario=self.request.user)

        if not usuario:
            messages.error(
                self.request,
                'Perfil não encontrado!'
            )
            return redirect('perfil:criar')

        enderecos = Endereco.objects.filter(usuario=usuario)

        contexto = {
            'carrinho': self.request.session.get('carrinho', None),
            'perfil': usuario,
            'enderecos': enderecos,
        }
        
        return render(
            self.request, 
            'produto/resumo_da_compra.html',
            contexto
        )