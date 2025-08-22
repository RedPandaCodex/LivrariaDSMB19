from rest_framework import serializers
from .models import Autor, Editora, Livro

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class EditoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

class LivroSerializer(serializers.ModelSerializer):
    editora = EditoraSerializer(read_only=True)
    editora_id = serializers.PrimaryKeyRelatedField(
        queryset = Editora.objects.all(), source='editora', write_only=True
    )
    
    class Meta:
        model = Livro
        fields = ['id', 'titulo','subtitulo','autor','editora','isbn','descricao',
                  'idioma','ano','paginas', 'preco', 'estoque','desconto', 
                  'disponivel', 'dimensoes', 'peso', 'editora', 'editora_id' ]