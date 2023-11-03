from .models import User, Pedido, Produto, ItemPedido, Endereco
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(request):
    produtos = Produto.objects.all().order_by("?")
    return render(request, "ecommerce/index.html", context={"produtos": produtos[:5]})


def search_bar(request):
    if request.method == "GET":
        produtos = Produto.objects.all()
        user_input = request.GET.get("search", "").lower().strip()
        search_products = []
        for produto in produtos:
            formatted_input = f"{produto.nome_produto.title()}{produto.nome_produto.upper()}{produto.nome_produto.lower()}{produto.nome_produto.swapcase()}"
            if user_input in formatted_input:
                search_products.append(produto)

        return render(request, "ecommerce/search_bar.html", context={
            "produtos": search_products,
            "user_input": user_input,
        })
    
    return HttpResponseRedirect(reverse("index"))


def produtos(request):
    produtos = Produto.objects.all()
    return render(request, "ecommerce/produtos.html", context={
        "produtos": produtos}
    )


@login_required
def add_produto(request):
    if request.user.is_superuser or request.user.adm:
        if request.method == "POST":
            nome = request.POST.get("nome_produto")
            p = request.POST.get("tamanho_p")
            m = request.POST.get("tamanho_m")
            g = request.POST.get("tamanho_g")
            gg = request.POST.get("tamanho_gg")
            descricao = request.POST.get("descricao_produto")
            valor = request.POST.get("valor_produto")
            url = request.POST.get("url_produto")

            Produto.objects.create(
                nome_produto=nome,
                tamanho_p=p,
                tamanho_m=m,
                tamanho_g=g,
                tamanho_gg=gg,
                descricao_produto=descricao,
                valor_produto=valor,
                img_url=url,
            )
            print("PRODUTO SALVO")

            return HttpResponseRedirect(reverse("index"))

        return render(request, "ecommerce/add_produto.html")
    else:
        return HttpResponseRedirect(reverse("index"))


def produto_page(request, produto_pk):
    produto = Produto.objects.get(pk=produto_pk)
    return render(request,"ecommerce/produto.html",context={
        "produto": produto,},
    )


@login_required
def commands(request):
    if request.user.is_superuser or request.user.adm:
        return render(request, "ecommerce/commands.html")

    else:
        return HttpResponseRedirect(reverse("index"))


# USER AUTHENTICATION !

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        request_username = User.objects.get(email=email).username
        user = authenticate(request, username=request_username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "ecommerce/login.html",
                context={"message": "E-mail ou senha incorretos."},
            )

    return render(request, "ecommerce/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(
                request,
                "ecommerce/register.html",
                context={"message", "Passwords must match."},
            )
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "ecommerce/register.html",
                context={"message": "Esse endereço de email já está em uso."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ecommerce/register.html")
