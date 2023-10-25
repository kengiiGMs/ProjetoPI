from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("commands", views.commands, name="commands"),
    path("add_produto", views.add_produto, name="add_produto"),
    path("produto/<int:produto_pk>", views.produto_page, name="produto_page")
]