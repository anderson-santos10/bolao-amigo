from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from campeonatos.models import Grupo, Jogo, Palpite
from usuarios.models import Profile

User = get_user_model()


# =====================================================
# FAZER PALPITES
# =====================================================
@login_required
def fazer_palpites(request):

    grupos = Grupo.objects.prefetch_related('times').all()

    # =====================================================
    # POST - SALVAR PALPITES
    # =====================================================
    if request.method == "POST":
        palpites_cache = {}

        for key, value in request.POST.items():
            if not key.startswith("jogo_"):
                continue

            if value == "" or value is None:
                continue

            try:
                parts = key.split("_")
                if len(parts) != 3:
                    continue

                _, jogo_id, tipo = parts

                if not jogo_id.isdigit():
                    continue

                jogo_id = int(jogo_id)

                if jogo_id not in palpites_cache:
                    palpites_cache[jogo_id] = {}

                palpites_cache[jogo_id][tipo] = value

            except Exception:
                continue

        for jogo_id, dados in palpites_cache.items():
            try:
                jogo = Jogo.objects.get(id=jogo_id)

                palpite, created = Palpite.objects.get_or_create(
                    usuario=request.user,
                    jogo=jogo
                )

                casa = dados.get("casa")
                visitante = dados.get("visitante")

                if casa not in [None, ""]:
                    palpite.gols_casa = int(casa)

                if visitante not in [None, ""]:
                    palpite.gols_visitante = int(visitante)

                palpite.save()

            except (Jogo.DoesNotExist, ValueError):
                continue

        return redirect("fazer_palpites")

    # =====================================================
    # GET - FILTRAR GRUPOS PENDENTES
    # =====================================================
    grupos_filtrados = []

    for grupo in grupos:

        jogos = Jogo.objects.filter(
            campeonato=grupo.campeonato,
            time_casa__grupo=grupo
        ).select_related('time_casa', 'time_visitante')

        total_jogos = jogos.count()

        palpites_usuario = Palpite.objects.filter(
            usuario=request.user,
            jogo__campeonato=grupo.campeonato,
            jogo__time_casa__grupo=grupo
        ).count()

        if total_jogos > 0 and palpites_usuario >= total_jogos:
            continue

        grupo.jogos = jogos
        grupo.selecoes = grupo.times.filter(grupo=grupo).distinct()

        grupos_filtrados.append(grupo)

    if not grupos_filtrados:
        return render(request, "campeonatos/palpites.html", {
            "finalizado": True
        })

    return render(request, "campeonatos/palpites.html", {
        "grupos": grupos_filtrados,
        "finalizado": False
    })


# =====================================================
# MEUS PALPITES
# =====================================================
@login_required
def meus_palpites(request):
    palpites = Palpite.objects.select_related(
        'jogo',
        'jogo__time_casa',
        'jogo__time_visitante'
    ).filter(usuario=request.user).order_by('-criado_em')

    return render(request, 'campeonatos/meus_palpites.html', {
        'palpites': palpites
    })


# =====================================================
# RANKING
# =====================================================
EXCLUDED_USERS = ["rootmaster"]

def ranking(request):

    ranking = Profile.objects.select_related('user').exclude(
        user__username__in=EXCLUDED_USERS
    ).exclude(
        user__is_superuser=True
    ).exclude(
        user__is_staff=True
    ).order_by('-pontuacao_total')

    return render(request, 'campeonatos/ranking.html', {
        'ranking': ranking
    })


# =====================================================
# FINALIZAR JOGO
# =====================================================
def finalizar_jogo(request, jogo_id):
    jogo = Jogo.objects.get(id=jogo_id)

    jogo.gols_casa = request.POST['gols_casa']
    jogo.gols_visitante = request.POST['gols_visitante']
    jogo.encerrado = True
    jogo.save()

    return redirect('admin_jogos')



# PALPITES DO USUÁRIO


def palpites_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)

    palpites = Palpite.objects.filter(
        usuario=usuario
    ).select_related('jogo', 'jogo__time_casa', 'jogo__time_visitante')

    palpites_dict = {p.jogo_id: p for p in palpites}

    total_jogos = Jogo.objects.count()
    total_palpites = palpites.count()

    # ESTATÍSTICAS (BÁSICAS)
    estatisticas = {
        "pontos_totais": getattr(usuario.profile, "pontuacao_total", 0),
        "palpites_feitos": total_palpites,
        "total_jogos": total_jogos,
        "erros": max(total_jogos - total_palpites, 0),
        "acertos_cheios": 0,  # depois podemos calcular real
        "vitorias_certas": 0,  # placeholder
        "jogos_pendentes": max(total_jogos - total_palpites, 0),
        "posicao_ranking": 0,  # depois podemos calcular ranking real
        "total_participantes": Profile.objects.count()
    }

    return render(request, 'campeonatos/palpites_usuario.html', {
        'usuario_visualizado': usuario,
        'palpites_dict': palpites_dict,
        'estatisticas': estatisticas,
    })