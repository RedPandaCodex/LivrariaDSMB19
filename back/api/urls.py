from django.urls import path
from .views import AutoresView, listar_autores

urlpatterns = [
    path('autores', AutoresView.as_view()),
    path('authors', listar_autores) 
]