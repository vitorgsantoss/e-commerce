# Generated by Django 5.1.5 on 2025-01-21 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itempedido',
            options={'verbose_name': 'Item do Pedido', 'verbose_name_plural': 'Itens do Pedido'},
        ),
    ]
