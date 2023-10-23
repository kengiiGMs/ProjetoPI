from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class User(AbstractUser):
    nome = models.CharField(max_length=255)
    rg = models.CharField(max_length=9)
    cpf = models.CharField(max_length=11)

class Funcionario(User):
    cargo_funcionario = models.CharField(max_length=32)
    administrador = models.BooleanField(default=False)

class Produto(models.Model):
    TAMANHO_CHOICES = [
        ("P", "Pequeno"),
        ("M", "Médio"),
        ("G", "Grande"),
        ("GG", "Extra Grande"),
    ]
    nome_produto = models.CharField(max_length=255)
    quantidade_produto = models.IntegerField()
    tamanho_produto = models.CharField(max_length=2, choices=TAMANHO_CHOICES)
    descricao_produto = models.TextField()
    valor_produto = models.DecimalField(max_digits=6, decimal_places=2)

class Endereco(models.Model):
    numero = models.IntegerField()
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=255, blank=True)

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_pedido")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="produto_pedido")
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.CASCADE, related_name="endereco_pedido")
    quantidade = models.PositiveIntegerField()
    data_pedido = models.DateTimeField(auto_now_add=True)
