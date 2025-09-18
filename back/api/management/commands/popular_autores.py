import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Autor

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--arquivo", default="population/autores.csv")
        parser.add_argument("--truncade", action="store_true")
        parser.add_argument("--update", action="store_true")

    @transaction.atomic
    def handle(self, *a, **o):
        df = pd.read_csv(o["arquivo"], encoding="utf-8-sig")
        df.columns = [c.strip().lower().lstrip("\ufeff") for c in df.columns]
        #normaliza os nomes das colunas: tira espaços extras, deixa em minusculo e remove o ufeff
        #o \ufeff é um caracter especial invisível
        if o["truncade"]:
            Autor.objects.all().delete()

        df['autor'] = df['autor'].astype(str).str.strip()

        df['surname'] = df['surname'].astype(str).str.strip()

        df['birthdate'] = pd.to_datetime(df['birthdate'], errors="coerce", format="%Y-%m-%d").dt.date
        
        df['nationality'] = df.get('nationality',"").astype(str).str.strip().str.capitalize().replace({"": None})

        #df = df.dropna(subset=['nationality']) #apaga a linha que contem erros
        #df = df.query("autor != '' and surname != '' ")

        if o["update"]:
            criados = atualizados = 0
            for r in df.itertuples(index=False):
                _, created = Autor.objects.update_or_create(
                    autor = r.autor, surname= r.surname, birthdate = r.birthdate,
                    defaults={'nationality': r.nationality}
                )

                criados += int(created)
                atualizados += int(not created)
            self.stdout.write(self.style.SUCCESS(f"Criados: {criados} | Atualizados: {atualizados}"))
        else:
            objs = [Autor(
                autor = r.autor, surname= r.surname, birthdate = r.birthdate, nationality = r.nationality
                ) for r in df.itertuples(index=False)
            ]
            
            Autor.objects.bulk_create(objs, ignore_conflicts=True)
            #BULK_CREATE esta jogando no banco os dados sem conflito

            self.stdout.write(self.style.SUCCESS(f"Criados: {len(objs)}"))