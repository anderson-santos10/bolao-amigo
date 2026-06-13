from django.core.management.base import BaseCommand

from campeonatos.models import Campeonato, Grupo, Time


class Command(BaseCommand):

    help = 'Importa grupos da Copa do Mundo 2026'

    def handle(self, *args, **kwargs):

        campeonato, _ = Campeonato.objects.get_or_create(
            nome='Copa do Mundo FIFA',
            temporada=2026
        )

        grupos = {
            'A': ['México', 'Costa Rica', 'Suriname', 'República Dominicana'],
            'B': ['Canadá', 'Honduras', 'El Salvador', 'Curaçao'],
            'C': ['Estados Unidos', 'Panamá', 'Haiti', 'Trinidad e Tobago'],
        }

        for letra, selecoes in grupos.items():

            grupo, _ = Grupo.objects.get_or_create(
                campeonato=campeonato,
                nome=letra
            )

            for nome in selecoes:

                Time.objects.get_or_create(
                    nome=nome,
                    grupo=grupo
                )

        self.stdout.write(
            self.style.SUCCESS(
                'Grupos importados com sucesso!'
            )
        )