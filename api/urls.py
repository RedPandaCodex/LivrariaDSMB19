from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   

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

    ###### AUTENTICAÇÃO ######
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view(), name='register'),
]