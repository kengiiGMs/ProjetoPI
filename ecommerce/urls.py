from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("commands", views.commands, name="commands"),
    path("produtos", views.produtos, name="produtos"),
    path("carrinho", views.carrinho, name="carrinho"),
    path("search_bar", views.search_bar, name="search_bar"),
    path("add_produto", views.add_produto, name="add_produto"),
    path("produto/<int:produto_pk>", views.produto_page, name="produto_page"),
    path("delete_carrinho_index/<int:pedido_pk>", views.delete_carrinho_index, name="delete_carrinho_index"),
    path("delete_carrinho_produtos/<int:pedido_pk>", views.delete_carrinho_produtos, name="delete_carrinho_produtos"),
    path("delete_carrinho_produto/<int:pedido_pk>/<int:produto_pk>", views.delete_carrinho_produto, name="delete_carrinho_produto"),

    # Auth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]