from django.urls import path
from .views import *

urlpatterns = [
    path('authors', listar_autores),

    ###### GET = POST ######
    path('autores', AutoresView.as_view()),
    path('editors', EditoraView.as_view()),
    path('books', LivroView.as_view()),

    ###### UPDATE = DELETE ######
    path('autor/<int:pk>', AutoresDetailView.as_view()),
    path('editor/<int:pk>', EditoraDetailView.as_view()),  
    path('book/<int:pk>', LivroDetailView.as_view()),
]