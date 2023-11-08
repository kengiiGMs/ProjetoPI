# Generated by Django 4.2.6 on 2023-11-07 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_endereco_rua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='bairro',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='cep',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='cidade',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='complemento',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='estado',
            field=models.CharField(max_length=2, null=True),
        ),
    ]
