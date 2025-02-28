from django.db import models
from django.contrib.auth.models import User
from perfil.models import Endereco

# Create your models here.

class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A','Aprovado'),
            ('C','Criado'),
            ('R','Reprovado'),
            ('P','Pendente'),
            ('E','Enviado'),
            ('F','Finalizado'),
        )
    )
    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.CASCADE,
        null= True, 
        blank=True,
    )

    def __str__(self):
        return f'Pedido {self.pk}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto =  models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=255)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item do pedido {self.pedido.pk}'
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    