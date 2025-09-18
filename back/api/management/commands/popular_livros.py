import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor, Editora, Livro

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo_editoras", default="population/editoras.csv")
        parser.add_argument("--arquivo_autores", default="population/autores.csv")
        parser.add_argument("--arquivo_livros", default="population/livros.csv")
        parser.add_argument("--truncade", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        df_editoras = pd.read_csv(o["arquivo_editoras"], encoding="utf-8-sig")
        df_autores = pd.read_csv(o["arquivo_autores"], encoding="utf-8-sig")
        df_livros = pd.read_csv(o["arquivo_livros"], encoding="utf-8-sig")

        df_editoras.columns = [c.strip().lower().lstrip("\ufeff") for c in df_editoras.columns]
        df_autores.columns = [c.strip().lower().lstrip("\ufeff") for c in df_autores.columns]
        df_livros.columns = [c.strip().lower().lstrip("\ufeff") for c in df_livros.columns]
        #normaliza os nomes das colunas: tira espaços extras, deixa em minusculo e remove o ufeff
        #o \ufeff é um caracter especial invisível

        ####### Livros e Autores #######

        #1) Unir nome e sobrenome do autor
        df_autores['full_name'] = df_autores['autor']+" "+df_autores['surname']

        #2) Criar coluna "id" em autores
        df_autores['id'] = df_autores.index + 1

        #3) Criar dicionario de mapeamento
        mapa_autores = dict(zip(df_autores['full_name'], df_autores['id']))

        #4) Buscar autor de livros no dicionario e retornar "id"
        df_livros['id_autor'] = df_livros['autor'].map(mapa_autores)

        ####### Livros e Editoras #######

        #1) Criar coluna "id"
        df_editoras['id'] = df_editoras.index +1

        #2) Criar dicionario de mapeamento
        mapa_editoras = dict(zip(df_editoras['editora'], df_editoras['id']))
        
        #3) Criar o "id_editora" em livros
        df_livros['id_editora'] = df_livros['editora'].map(mapa_editoras)

    
        # if o["truncade"]: Livros.objects.all().delete()

        df_livros['titulo'] = df_livros['titulo'].astype(str).str.strip()
        
        df_livros['subtitulo'] = df_livros['subtitulo'].astype(str).str.strip()
        
        df_livros['autor'] = df_livros['id_autor'].astype(int)
        
        df_livros['editora'] = df_livros['id_editora'].astype(int)
        
        df_livros['isbn'] = df_livros['isbn'].astype(str).str.strip()
        
        df_livros['descricao'] = df_livros['descricao'].astype(str).str.strip()
        
        df_livros['idioma'] = df_livros['idioma'].astype(str).str.strip()
        
        df_livros['ano'] = df_livros['ano'].astype(str)
        
        df_livros['paginas'] = df_livros['paginas'].astype(int)
        
        df_livros['preco'] = df_livros['preco'].astype(float)
        
        df_livros['estoque'] = df_livros['estoque'].astype(int)
        
        df_livros['desconto'] = df_livros['desconto'].astype(float)
        
        df_livros['disponivel'] = df_livros['disponivel'].astype(bool)
        
        df_livros['dimensoes'] = df_livros['dimensoes'].astype(str).str.strip()
        
        df_livros['peso'] = df_livros['peso'].astype(float)

        # #df = df.dropna(subset=['nationality']) #apaga a linha que contem erros
        # #df = df.query("autor != '' and surname != '' ")

        if o["update"]:
            criados = atualizados = 0
            for r in df_livros.itertuples(index=False):
                _, created = Livro.objects.update_or_create(
                    isbn=r.isbn,
                    defaults={
                        "titulo": r.titulo,
                        "subtitulo": r.subtitulo or "",
                        "autor_id": int(r.id_autor),
                        "editora_id": int(r.id_editora),
                        "descricao": r.descricao or "",
                        "idioma": r.idioma or "",
                        "ano_publicacao": int(r.ano) if pd.notna(r.ano) else None,
                        "paginas": int(r.paginas),
                        "preco": float(r.preco),
                        "estoque": int(r.estoque),
                        "desconto": float(r.desconto),
                        "disponivel": bool(r.disponivel),
                        "dimensoes": r.dimensoes or "",
                        "peso": float(r.peso),
                    }
                )

                criados += int(created)           # conta os novos
            atualizados += int(not created)   # conta os atualizados
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
 
        else:
            objs = []
            for r in df_livros.itertuples(index=False):
                objs.append(
                    Livro(
                        isbn=r.isbn,
                        titulo=r.titulo,
                        subtitulo=r.subtitulo or "",
                        autor_id=int(r.id_autor),
                        editora_id=int(r.id_editora),
                        descricao=r.descricao or "",
                        idioma=r.idioma or "",
                        ano=int(r.ano) if pd.notna(r.ano) else None,
                        paginas=int(r.paginas),
                        preco=float(r.preco),
                        estoque=int(r.estoque),
                        desconto=float(r.desconto),
                        disponivel=bool(r.disponivel),
                        dimensoes=r.dimensoes or "",
                        peso=float(r.peso),
                    )
                )
            Livro.objects.bulk_create(objs, ignore_conflicts=True)
            criados = len(objs)
 
 
            self.stdout.write(self.style.SUCCESS(f"Criados: {len(objs)}"))