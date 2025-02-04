from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido

class FecharPedido(View):
    def get(self,*args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request, 
                'Efetue login para ter acesso a está página.'
            )
            return redirect('perfil:criar')
        
        carrinho = self.request.session.get('carrinho')
        
        if not carrinho:
            messages.error(
                self.request, 
                'Adicione produtos ao carrinho.'
            )
            return redirect('produto:lista')
        
        carrinho_variacoes = [ v for v in carrinho]

        bd_variacao = list(Variacao.objects.select_related('produto').filter(
            id__in=carrinho_variacoes))
        
        for variacao in bd_variacao:
            vid=str(variacao.pk)
            if variacao.estoque < carrinho[vid]['quantidade']:

                carrinho[vid]['quantidade'] = variacao.estoque
                carrinho[vid]['preco_quantitativo'] = variacao.estoque\
                *carrinho[vid]['preco_unitario']
                carrinho[vid]['preco_quantitativo_promocional'] = \
                    variacao.estoque*carrinho[vid]['preco_unitario_promocional']

                if carrinho[vid]['quantidade'] == 0:
                    del carrinho[vid]

                self.request.session['carrinho']= carrinho
                self.request.session.save()

                messages.error(
                    self.request,
                    f'Quantidade insuficiente para {variacao.produto.nome}, \
                        adicionado ao carrinho {variacao.estoque}x'
                )
                return redirect('produto:finalizar')
            
            cart_total = carrinho[vid]['preco_quantitativo_promocional'] or \
                carrinho[vid]['preco_quantitativo']

            variacao.estoque -= carrinho[str(variacao.pk)]['quantidade']
            variacao.save()
        messages.success(
            self.request,
            'UHUL! Compra efetuada com sucesso!'
        )

        pedido = Pedido(
            user= self.request.user,
            total = cart_total,
            status = 'C'
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido= pedido,
                    produto = v['produto_nome'],
                    produto_id = v['produto_id'],
                    variacao = v['variacao_nome'],
                    variacao_id = v['variacao_id'],
                    preco = v['preco_unitario'],
                    preco_promocional = v['preco_unitario_promocional'],
                    quantidade = v['quantidade'],
                    imagem = v['imagem'],
                    ) for v in carrinho.values()
            ]
        )

        del self.request.session['carrinho']

        return redirect('produto:lista')


class Pagar(View):
    template_name = 'pedido/pagar.html'
    def get(self,*args, **kwargs):
        return render(self.request, self.template_name)

class Detalhe(View):
    ...
