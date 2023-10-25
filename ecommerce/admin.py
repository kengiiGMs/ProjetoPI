from django.contrib import admin
from .models import User, Produto, ItemPedido, Pedido, Endereco

# Register your models here.

admin.site.register(User)
admin.site.register(Pedido)
admin.site.register(Produto)
admin.site.register(Endereco)
admin.site.register(ItemPedido)