from django.db import models
from util.image import resize_image
from util.rands import slugfy_new

# Create your models here.
class Produto(models.Model):
    nome = models.CharField( max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
        )
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to=f'produto_imagens/',
        blank=True,
        null=True,
        )
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V','Variável'),
            ('S', 'Simples'),
        )
    )
    
    
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugfy_new(self.nome, len = 8)
        
        current_imagem_name = str(self.imagem.name)
        super_save = super().save(*args, **kwargs)
        imagem_changed = False

        if self.imagem:
            imagem_changed = current_imagem_name != self.imagem.name
        
        if imagem_changed:
            resize_image(self.imagem, 800)

        return super_save
    

class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome
