from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from campeonatos.models import Grupo, Jogo, Palpite
from usuarios.models import Profile



@login_required # Garante que request.user existe e está logado
def fazer_palpites(request):

    # Otimização: busca os grupos trazendo os times corretos vinculados a eles
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
        # Busca apenas os jogos pertencentes a ESTE grupo específico
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

        # ✔ bloqueia grupo quando já completou tudo
        if total_jogos > 0 and palpites_usuario >= total_jogos:
            continue
        
        grupo.jogos = jogos
        
        # Filtramos explicitamente os times que pertencem a ESTE ID de grupo
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
    
def finalizar_jogo(request, jogo_id):
    jogo = Jogo.objects.get(id=jogo_id)

    jogo.gols_casa = request.POST['gols_casa']
    jogo.gols_visitante = request.POST['gols_visitante']
    jogo.encerrado = True
    jogo.save()

    return redirect('admin_jogos')