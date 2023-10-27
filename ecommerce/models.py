from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    nome = models.CharField(max_length=255, blank=False, null=True)
    cpf = models.CharField(max_length=11, blank=False, null=True)
    adm = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Produto(models.Model):
    nome_produto = models.CharField(max_length=255)
    descricao_produto = models.TextField()
    valor_produto = models.DecimalField(max_digits=6, decimal_places=2)
    img_url = models.URLField()
    tamanho_p = models.IntegerField(blank=False, null=True)
    tamanho_m = models.IntegerField(blank=False, null=True)
    tamanho_g = models.IntegerField(blank=False, null=True)
    tamanho_gg = models.IntegerField(blank=False, null=True)

    def __str__(self):
        return self.nome_produto


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usuario_pedido")
    data_pedido = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return f"ID: {self.pk} | Cliente: {self.usuario}"
    
    
class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="produto_item", blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True, related_name="pedido_pertencente")
    quantidade = models.PositiveIntegerField(null=True, blank=True)
    data_adicionada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido: {self.produto}"
    
class Endereco(models.Model):
    numero = models.IntegerField()
    cep = models.CharField(max_length=8)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    complemento = models.CharField(max_length=255, blank=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.bairro}, {self.numero}"