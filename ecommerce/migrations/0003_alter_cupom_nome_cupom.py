# Generated by Django 4.2.6 on 2023-11-06 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_cupom_pedido_cupom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupom',
            name='nome_cupom',
            field=models.CharField(max_length=24, null=True),
        ),
    ]