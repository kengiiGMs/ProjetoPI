from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("carrinho", views.carrinho, name="carrinho"),
    path("checkout", views.checkout, name="checkout"),
    path("user_page", views.user_page, name="user_page"),
    path("search_bar", views.search_bar, name="search_bar"),
    path("add_produto", views.add_produto, name="add_produto"),
    path("produto/<int:produto_pk>", views.produto_page, name="produto_page"),
    path("produtos/<str:category_name>", views.produtos, name="produtos"),
    path("carrinho_action/<int:item_pk>/<str:action>", views.carrinho_action, name="carrinho_action"),

    # Auth
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]