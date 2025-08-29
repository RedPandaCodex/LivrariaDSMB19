import pandas as pd
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from api.models import Autor

class Command(BaseCommand):
    help = "Importa autores de population/autores.csv usando pandas (com limpeza e validação)."

    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default=str(Path("population") / "autores.csv"))
        parser.add_argument("--truncate", action="store_true", help="Apaga todos os autores antes de importar")
        parser.add_argument("--update", action="store_true", help="Faz upsert (update_or_create) em vez de inserir em massa")

    @transaction.atomic 
    # @transaction.atomic  👉 garante que tudo dentro do método será executado dentro de uma única transação de banco. 
    # Se der erro no meio, o Django desfaz tudo (rollback).
    def handle(self, *args, **opts): # é o método principal que o Django executa quando você roda python manage.py popular.
        # *args, **opts: recebe os argumentos/flags passados na linha de comando (ex.: --truncate, --update).
        csv_path = Path(opts["arquivo"]) # pega o caminho do CSV passado por argumento (ou o default definido).
        if not csv_path.exists(): #Se o arquivo não existir, lança um CommandError → o Django mostra a mensagem de erro e interrompe.
            raise CommandError(f"Arquivo não encontrado: {csv_path}")

        # 1) Ler CSV
        df = pd.read_csv(csv_path)

        # 2) Limpeza básica
        for col in ["nome", "sobrenome", "nacionalidade"]:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
            else:
                df[col] = ""

        if "biografia" not in df.columns:
            df["biografia"] = ""

        df["data_nascimento"] = pd.to_datetime(df.get("data_nascimento"), errors="coerce", format="%Y-%m-%d")
        df["nacionalidade"] = df["nacionalidade"].str.capitalize()

        # 3) Remover vazios/duplicados
        df = df.dropna(how="all")
        df = df.drop_duplicates(subset=["nome", "sobrenome", "data_nascimento"], keep="first").reset_index(drop=True)

        # 4) Validar obrigatórios
        obrigatorios = df["nome"].ne("") & df["sobrenome"].ne("") & df["data_nascimento"].notna()
        invalidos = df[~obrigatorios] #pega os que não cumprem
        if not invalidos.empty: #Se houver inválidos → mostra aviso e remove do DataFrame.
            self.stdout.write(self.style.WARNING(f"Pulando {len(invalidos)} linha(s) inválida(s)."))

        df = df[obrigatorios]

        #Truncate (limpar tabela antes de importar)
        if opts["truncate"]:#Se o usuário passou --truncate, apaga todos os registros antes de importar.
            self.stdout.write(self.style.WARNING("Limpando tabela api_autor..."))
            Autor.objects.all().delete()

        criados = 0
        atualizados = 0

        if opts["update"]: 
            # UPSERT registro a registro (mais didático, porém mais lento)
            for row in df.itertuples(index=False):
                # df.itertuples() é um método do pandas DataFrame.
                # Ele percorre cada linha e devolve um objeto parecido com uma tupla, chamado namedtuple.
                # Cada campo da linha vira um atributo desse objeto.
                # O parâmetro:
                # index=False → não inclui a coluna de índice (0,1,2...) no resultado.
                # Assim, você só recebe as colunas do CSV.
                obj, created = Autor.objects.update_or_create(
                    nome=row.nome,
                    sobrenome=row.sobrenome,
                    data_nascimento=row.data_nascimento.date(),
                    defaults={
                        "nacionalidade": row.nacionalidade or None,
                        "biografia": (row.biografia or "").strip() or None,
                    },
                )
                    # Retorno:
                    #  obj → o autor encontrado/criado.
                    #  created → True se foi um novo autor, False se apenas atualizou um existente.
                    
                    # Suponha que já existe no banco:
                    #   Autor(nome="Jorge", sobrenome="Amado", data_nascimento="1912-08-10", nacionalidade="Brasileira", biografia="...")
                    # Se no CSV vem:
                    #   Jorge,Amado,1912-08-10,Brasileira,Autor famoso
                    # O Django encontra esse autor pelo trio (nome, sobrenome, data_nascimento).
                    #    Atualiza biografia para "Autor famoso".
                    #    created = False.
                if created:
                    criados += 1
                else:
                    atualizados += 1
        else:
            # Inserção em massa (rápida)
            buffer = []
            for row in df.itertuples(index=False):
                buffer.append(Autor(
                    nome=row.nome,
                    sobrenome=row.sobrenome,
                    data_nascimento=row.data_nascimento.date(),
                    nacionalidade=row.nacionalidade or None,
                    biografia=(row.biografia or "").strip() or None,
                ))
            Autor.objects.bulk_create(buffer, ignore_conflicts=True)
            criados = len(buffer)

        msg = f"Concluído. Criados: {criados}"
        if opts["update"]:
            msg += f" | Atualizados: {atualizados}"
        self.stdout.write(self.style.SUCCESS(msg))