from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from .models import Profile



# LOGIN

def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        senha = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=senha
        )

        if usuario:
            login(request, usuario)
            return redirect('dashboard')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')


def regras_bolao_view(request):
    return render(request, 'campeonatos/regras.html')


# =====================================================
# POSIÇÃO DO USUÁRIO (UTIL)
# =====================================================
def get_posicao_usuario(ranking, user):
    for index, obj in enumerate(ranking, start=1):
        if obj.user == user:
            return index
    return None


# =====================================================
# DASHBOARD
# =====================================================
@login_required(login_url='login')
def dashboard_view(request):

    ranking = list(
    Profile.objects
    .select_related('user')
    .exclude(user__username="rootmaster")  # remove rootmaster
    .exclude(user__is_superuser=True)      # opcional (mais seguro)
    .order_by('-pontuacao_total')
    )

    # garante profile do usuário
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # cria ranking mínimo seguro
    top1 = ranking[0] if len(ranking) > 0 else None
    top2 = ranking[1] if len(ranking) > 1 else None
    top3 = ranking[2] if len(ranking) > 2 else None

    # posição correta (mais seguro)
    user_rank = None
    for i, p in enumerate(ranking, start=1):
        if p.user_id == request.user.id:
            user_rank = i
            break

    return render(request, 'usuarios/dashboard.html', {
        'ranking': ranking,
        'top1': top1,
        'top2': top2,
        'top3': top3,
        'user_points': profile.pontuacao_total,
        'user_rank': user_rank,
    })


# =====================================================
# LOGOUT
# =====================================================
def logout_view(request):
    logout(request)
    return redirect('login')


# =====================================================
# CADASTRO
# =====================================================
def cadastro_view(request):

    if request.method == 'POST':

        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
            return redirect('cadastro')

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Este e-mail já está cadastrado.')
            return redirect('cadastro')

        User.objects.create_user(
            username=email,
            email=email,
            first_name=nome,
            password=senha
        )

        messages.success(request, 'Conta criada com sucesso!')
        return redirect('login')

    return render(request, 'usuarios/cadastro.html')


# =====================================================
# UPDATE PERFIL
# =====================================================
@login_required(login_url='login')
def update_profile(request):

    if request.method == "POST":

        user = request.user
        profile, _ = Profile.objects.get_or_create(user=user)

        # nome
        user.first_name = request.POST.get("first_name")
        user.save()

        # senha (mantém login)
        password = request.POST.get("password")
        if password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)

        # imagem
        if request.FILES.get("image"):
            profile.image = request.FILES["image"]
            profile.save()

    return redirect("dashboard")