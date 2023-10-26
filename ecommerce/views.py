from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import User, Pedido, Produto, ItemPedido, Endereco

# Create your views here.

def index(request):
    produtos = Produto.objects.all()
    return render(request, "ecommerce/index.html", context={
        "produtos": produtos[:5]
    })

def produtos(request):
    produtos = Produto.objects.all()
    return render(request, "ecommerce/produtos.html", context={
        "produtos": produtos
    })

@login_required
def add_produto(request):
    if request.user.is_superuser or request.user.adm:
        if request.method == "POST":
            nome = request.POST["nome_produto"]
            quantidade = request.POST["quantidade_produto"]
            tamanho = request.POST["tamanho_produto"]
            descricao = request.POST["descricao_produto"]
            valor = request.POST["valor_produto"]
            url = request.POST["url_produto"]

            produto = Produto.objects.create(
                nome_produto=nome,
                quantidade_produto=quantidade,
                tamanho_produto=tamanho.upper(),
                descricao_produto=descricao,
                valor_produto=valor,
                img_url=url,
            )
            produto.save()
            print("PRODUTO SALVO")

            return HttpResponseRedirect(reverse("index"))

        return render(request, "ecommerce/add_produto.html")
    else:
        return HttpResponseRedirect(reverse("index"))

def produto_page(request, produto_pk):
    produto = Produto.objects.get(pk=produto_pk)
    return render(request, "ecommerce/produto.html", context={
        "produto": produto
    })

@login_required
def commands(request):
    if request.user.is_superuser or request.user.adm:
        return render(request, "ecommerce/commands.html")
    else:
        return HttpResponseRedirect(reverse("index"))



# USER AUTHENTICATION !

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ecommerce/login.html", context={
                "message": "E-mail ou senha incorretos."
            })


    return render(request, "ecommerce/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "ecommerce/register.html", context={
                "message", "Passwords must match."
            })
        
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ecommerce/register.html", context={
                "message": "Esse endereço de email já está em uso."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ecommerce/register.html")

        