# Generated by Django 4.2.6 on 2023-11-06 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0007_alter_produto_img_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='cupom',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
