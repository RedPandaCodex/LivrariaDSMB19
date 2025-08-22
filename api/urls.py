from django.urls import path
from .views import AutoresView, listar_autores, EditoraView, LivroView

urlpatterns = [
    path('autores', AutoresView.as_view()),
    path('authors', listar_autores),
    path('editors', EditoraView.as_view()),
    path('books', LivroView.as_view()),
]