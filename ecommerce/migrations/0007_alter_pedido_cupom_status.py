# Generated by Django 4.2.6 on 2023-11-06 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_pedido_cupom_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='cupom_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
