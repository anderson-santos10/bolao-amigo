from django.utils import timezone
from datetime import timedelta
from campeonatos.data import GRUPOS
from .models import Campeonato, Grupo, Jogo, Time


def gerar_jogos_campeonato(campeonato_id):
    campeonato = Campeonato.objects.get(id=campeonato_id)

    grupos = Grupo.objects.filter(campeonato=campeonato)

    data_base = timezone.make_aware(
        timezone.datetime(2026, 6, 11, 16, 0)
    )

    for grupo in grupos:
        times = list(grupo.times.all())

        if len(times) < 4:
            print(f"Grupo {grupo.nome} ignorado (menos de 4 times)")
            continue

        confrontos = [
            (0,1),
            (2,3),
            (0,2),
            (1,3),
            (0,3),
            (1,2),
        ]

        for i, (a, b) in enumerate(confrontos):

            Jogo.objects.get_or_create(
                campeonato=campeonato,
                rodada=i+1,
                time_casa=times[a],
                time_visitante=times[b],
                defaults={
                    "estadio": "Estádio FIFA",
                    "data_jogo": data_base + timedelta(days=i*6),
                }
            )