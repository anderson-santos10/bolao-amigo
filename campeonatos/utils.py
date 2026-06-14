from django.db.models import Sum
from campeonatos.models import Jogo, Palpite
from usuarios.models import Profile


def calcular_pontos_jogo(jogo_id):
    jogo = Jogo.objects.get(id=jogo_id)

    palpites = Palpite.objects.filter(jogo=jogo)

    for p in palpites:

        pontos = 0

        # acerto exato
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

    # 🔥 RESETA E RECALCULA TUDO (CORREÇÃO DEFINITIVA)
    for profile in Profile.objects.all():
        total = Palpite.objects.filter(usuario=profile.user).aggregate(
            total=Sum('pontos')
        )['total'] or 0

        profile.pontuacao_total = total
        profile.save()

    jogo.pontos_calculados = True
    jogo.save()