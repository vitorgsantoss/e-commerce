from django.db import models
from django.contrib.auth.models import User
from util.valida_cpf import validate
from django.forms import ValidationError
import re
    

class Perfil(models.Model):
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=14)

    def clean(self):
        error_messages = {}

        if not validate(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido'

        if error_messages:
            raise ValidationError(error_messages)
        
        
    
    def __str__(self):
        return self.usuario.username


class Endereco(models.Model):
    usuario = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    rua = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        default= 'SP',
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )
    def clean(self):
        error_messages = {}

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'Informe um CEP válido'
        
        if error_messages:
            raise ValidationError(error_messages)

    def __str__(self):
        return f'Endereço {self.usuario.pk}'
    
    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


