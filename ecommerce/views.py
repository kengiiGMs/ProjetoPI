from .models import User, Pedido, Produto, ItemPedido, Categoria, Cupom, Endereco, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse

def set_shipping(post, pedido, user):
    rua = post.get("rua")
    numero = post.get("numero")
    bairro = post.get("bairro")
    complemento = post.get("complemento", "")
    cidade = post.get("cidade")
    cep = post.get("cep")
    estado = post.get("estado")

    e = Endereco.objects.create(
        rua=rua,
        numero=numero, 
        cep=cep, 
        bairro=bairro, 
        cidade=cidade, 
        estado=estado, 
        complemento=complemento, 
        pedido=pedido
    )

    if bool(post.get("lembrar_endereco")):
        e.usuario = user
    
    e.save()

# Create your views here.

def index(request):
    produtos = Produto.objects.all().order_by("?")
    return render(request, "ecommerce/index.html", context={
        "produtos": produtos[:5],
    })


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


def produtos(request, category_name):
    if category_name == "all":
        produtos = Produto.objects.all()
    else:
        categoria = Categoria.objects.filter(nome_categoria=category_name).first()

        if not categoria:
            produtos = Produto.objects.all()
        else:
            produtos = Produto.objects.filter(categorias=categoria)

    return render(request, "ecommerce/produtos.html", context={
        "produtos": produtos,
        "categorias": Categoria.objects.all(),
    })


@login_required
def add_produto(request):
    if request.user.is_superuser or request.user.adm:
        if request.method == "POST":
            categoria = request.POST.get("categoria")
            nova_categoria = request.POST.get("nova_categoria")
            
            # Só cria uma nova categoria caso nova_categoria tenha um valor e categoria == Nenhuma.
            if nova_categoria and categoria == "Nenhuma":
                categoria = Categoria.objects.create(nome_categoria=nova_categoria)
                categoria.save()
                categoria = categoria.pk
                print(f"Condicional: {categoria}")

            nome = request.POST.get("nome_produto")
            p = request.POST.get("tamanho_p")
            m = request.POST.get("tamanho_m")
            g = request.POST.get("tamanho_g")
            gg = request.POST.get("tamanho_gg")
            descricao = request.POST.get("descricao_produto")
            valor = request.POST.get("valor_produto")
            url = request.POST.get("url_produto", "")
            image = request.FILES.get("image")

            produto = Produto.objects.create(
                nome_produto=nome,
                tamanho_p=p,
                tamanho_m=m,
                tamanho_g=g,
                tamanho_gg=gg,
                descricao_produto=descricao,
                valor_produto=valor,
                img_url=url,
                image=image
            )
            produto.save()
            print("PRODUTO SALVO")

            if categoria != "False":
                cat = Categoria.objects.get(pk=categoria)
                cat.produto.add(produto)

            return HttpResponseRedirect(reverse("index"))

        return render(request, "ecommerce/add_produto.html", context={
            "categorias": Categoria.objects.all()
        })
    else:
        return HttpResponseRedirect(reverse("index"))


def produto_page(request, produto_pk):
    if request.method == "POST":
        if request.user.is_authenticated:
            produto = Produto.objects.get(pk=produto_pk)
            pedido, create = Pedido.objects.get_or_create(usuario=request.user, complete=False)
            quantidade = request.POST.get("quantidade")
            tamanho = request.POST.get("tamanho")
            
            # Filtra todos os produtos iguais de mesmo tamanho e pega o primeiro 
            item_pedido = pedido.items.filter(produto=produto).filter(tamanho=tamanho).first()

            # Se existir o item filtrado, então apenas adiciona a quantidade desejada ao carrinho
            if item_pedido:
                item_pedido = ItemPedido.objects.get(pk=item_pedido.pk)
                item_pedido.quantidade += int(quantidade)
                item_pedido.save()
            
            # Caso não exista, cria um ItemPedido novo
            else:
                ItemPedido.objects.create(produto=produto, pedido=pedido, quantidade=quantidade, tamanho=tamanho)

            if request.POST.get("carrinho"):
                return HttpResponseRedirect(reverse("produto_page", args=(produto_pk, )))
            
            elif request.POST.get("finalizar"):
                return HttpResponseRedirect(reverse("carrinho"))
        else:
            return HttpResponseRedirect(reverse("login"))

    produto = Produto.objects.get(pk=produto_pk)
    compradores = produto.compradores.all()
    commentarios = produto.comentarios.all()
    estrelas = range(1,6)
    return render(request,"ecommerce/produto.html",context={
        "produto": produto,
        "compradores": compradores,
        "comments": commentarios,
        "estrelas": estrelas,
    })

@login_required(login_url="/login")
def editar_produto(request, produto_pk, status):
    user = request.user
    if user.is_superuser or user.adm:
        if request.method == "POST":
            produto = Produto.objects.get(pk=produto_pk)
            if status == "deletar":
                produto.delete()
            elif status == "editar":
                novo_nome = request.POST.get("novo_nome")
                novo_valor = request.POST.get("novo_valor")

                produto.nome_produto = novo_nome
                produto.valor_produto = novo_valor

                produto.save()

                return HttpResponseRedirect(reverse("produto_page", args=(produto_pk, )))

    return HttpResponseRedirect(reverse("index"))


def carrinho(request):
    if request.user.is_authenticated:
        cliente = request.user
        pedido, created = Pedido.objects.get_or_create(usuario=cliente, complete=False)
        carrinho = pedido.items.all()
        for item in carrinho:
            pi = ItemPedido.objects.get(pk=item.pk)
            if (item.tamanho == "P") and (item.quantidade > item.produto.tamanho_p):
                pi.quantidade = pi.produto.tamanho_p
            elif (item.tamanho == "M") and (item.quantidade > item.produto.tamanho_m):
                pi.quantidade = pi.produto.tamanho_m
            elif (item.tamanho == "G") and (item.quantidade > item.produto.tamanho_g):
                pi.quantidade = pi.produto.tamanho_g
            elif (item.tamanho == "GG") and (item.quantidade > item.produto.tamanho_gg):
                pi.quantidade = pi.produto.tamanho_gg
            pi.save()
            
    else:
        carrinho = []
        pedido = {"get_total_carrinho": 0, "get_total_items": 0}

    return render(request, "ecommerce/carrinho.html", context={
        "carrinho": carrinho,
        "pedido": pedido,
    })


def carrinho_action(request, item_pk, action):
    if request.method == "POST":
        item = ItemPedido.objects.get(pk=item_pk)
        if action == "adicionar":
            item.quantidade += 1
        elif action == "remover":
            item.quantidade -= 1
        item.save()
        
        if item.quantidade <= 0:
            item.delete()

        return HttpResponseRedirect(reverse("carrinho"))
    else:
        return HttpResponseRedirect(reverse("index"))
    
def cupom(request, pedido_pk):
    if request.method == "POST":
        user_input = request.POST.get("cupom").lower()
        pedido = Pedido.objects.get(pk=pedido_pk)
        cupom = Cupom.objects.filter(nome_cupom=user_input).first()
        
        if cupom:
            pedido.cupom_status = True
            pedido.cupom = cupom
            pedido.save()
            message = "Cupom adicionado com sucesso!"
        else:
            message = "Cupom inválido!"

        carrinho = pedido.items.all()
        
        return render(request, "ecommerce/carrinho.html", context={
            "carrinho": carrinho,
            "pedido": pedido,
            "message": message,
        })
    
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url="/login")
def comments(request, produto_pk):
    if request.method == "POST":
        produto = Produto.objects.get(pk=produto_pk)
        titulo = request.POST.get("titulo")
        texto = request.POST.get("texto")
        estrelas = request.POST.get("starValue")
        usuario = request.user
        5
        Comment.objects.create(
            usuario=usuario,
            produto=produto,
            titulo=titulo,
            texto=texto,
            estrelas=int(estrelas)
        )

        return HttpResponseRedirect(reverse("produto_page", args=(produto_pk, )))
    
    return HttpResponseRedirect(reverse("index"))

@login_required(login_url="/login")
def checkout(request):
    if request.method == "POST":
        pedido = Pedido.objects.get(usuario=request.user, complete=False)
        pedido.complete = True
        for item in pedido.items.all():
            produto = item.produto

            # Código de merda, eu sei...
            if item.tamanho == "P":
                produto.tamanho_p -= item.quantidade
            elif item.tamanho == "M":
                produto.tamanho_m -= item.quantidade
            elif item.tamanho == "G":
                produto.tamanho_g -= item.quantidade
            elif item.tamanho == "GG":
                produto.tamanho_gg -= item.quantidade
            
            produto.compradores.add(request.user)
            produto.save()
            
        set_shipping(request.POST, pedido, request.user)
        pedido.save()
        return HttpResponseRedirect(reverse("checkout"))

    if request.user.is_authenticated:
        cliente = request.user
        pedido, created = Pedido.objects.get_or_create(usuario=cliente, complete=False)
        carrinho = pedido.items.all()
    else:
        carrinho = []
        pedido = {"get_total_carrinho": 0, "get_total_items": 0}

    if not carrinho:
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "ecommerce/checkout.html", context={
        "carrinho": carrinho,
        "pedido": pedido,
    })


@login_required
def user_page(request):
    pedidos_finalizados = Pedido.objects.filter(usuario=request.user, complete=True).order_by("-data_pedido")
    return render(request, "ecommerce/user_page.html", context={
        "pedidos_finalizados": pedidos_finalizados,
    })


# USER AUTHENTICATION !

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

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
        first_name = request.POST.get("first_name").title()
        last_name = request.POST.get("last_name").title()
        username = request.POST.get("email").lower()
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        if password != confirmation:
            return render(request, "ecommerce/register.html", context={
                "message": "As senhas devem ser iguais.",
            })
           
        try:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
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