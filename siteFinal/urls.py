from django.urls import path, include, re_path
from django.contrib import admin
from .views import IndexView, DetalheView, DetalhePDFView
from . import views


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path("register", views.register_request, name="register"),
    path("detalhe/<int:pk>", views.DetalheView.as_view(), name="detalhe"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path('ternos/', DetalhePDFView.as_view(), name='terno'),

]
