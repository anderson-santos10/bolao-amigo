from django.db.models import Sum
from campeonatos.models import Jogo, Palpite
from usuarios.models import Profile


def recalcular_tudo():

    # Zera todos os pontos dos palpites
    Palpite.objects.update(pontos=0)

    # Recalcula jogo por jogo
    jogos = Jogo.objects.filter(
        encerrado=True,
        gols_casa__isnull=False,
        gols_visitante__isnull=False
    )

    for jogo in jogos:

        palpites = Palpite.objects.filter(jogo=jogo)

        for p in palpites:

            pontos = 0

            # Acertou placar exato
            if (
                p.gols_casa == jogo.gols_casa and
                p.gols_visitante == jogo.gols_visitante
            ):
                pontos = 3

            else:

                if jogo.gols_casa > jogo.gols_visitante:
                    resultado_jogo = "C"
                elif jogo.gols_casa < jogo.gols_visitante:
                    resultado_jogo = "F"
                else:
                    resultado_jogo = "E"

                if p.gols_casa > p.gols_visitante:
                    resultado_palpite = "C"
                elif p.gols_casa < p.gols_visitante:
                    resultado_palpite = "F"
                else:
                    resultado_palpite = "E"

                if resultado_jogo == resultado_palpite:
                    pontos = 1

            p.pontos = pontos
            p.save()

    # Recalcula ranking
    for profile in Profile.objects.all():

        total = (
            Palpite.objects
            .filter(usuario=profile.user)
            .aggregate(total=Sum('pontos'))['total']
            or 0
        )

        profile.pontuacao_total = total
        profile.save()