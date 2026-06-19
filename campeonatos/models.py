from django.db import models
from django.contrib.auth.models import User


class Campeonato(models.Model):
    nome = models.CharField(max_length=100)
    temporada = models.IntegerField()

    premiacao = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    rodada_atual = models.IntegerField(default=1)

    def __str__(self):
        return self.nome


class Grupo(models.Model):
    campeonato = models.ForeignKey(
        Campeonato,
        on_delete=models.CASCADE,
        related_name='grupos'
    )

    nome = models.CharField(max_length=7)

    def __str__(self):
        return self.nome


class Time(models.Model):
    nome = models.CharField(max_length=100)

    codigo_pais = models.CharField(max_length=2)
    grupo = models.ForeignKey(Grupo,
        on_delete=models.SET_NULL, null=True, blank=True, related_name='times')

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    codigo_jogo = models.CharField(max_length=20, unique=True, null=True, blank=True)
    campeonato = models.ForeignKey(
        Campeonato,
        on_delete=models.CASCADE,
        related_name='jogos'
    )

    estadio = models.CharField(
        max_length=200,
        blank=True
    )

    rodada = models.IntegerField()

    time_casa = models.ForeignKey(
        Time,
        on_delete=models.CASCADE,
        related_name='jogos_casa'
    )

    time_visitante = models.ForeignKey(
        Time,
        on_delete=models.CASCADE,
        related_name='jogos_visitante'
    )

    data_jogo = models.DateTimeField()

    gols_casa = models.IntegerField(null=True, blank=True)
    gols_visitante = models.IntegerField(null=True, blank=True)

    pontos_calculados = models.BooleanField(default=False)
    encerrado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.time_casa} x {self.time_visitante}'


class Palpite(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='palpites')
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE, related_name='palpites')

    gols_casa = models.PositiveIntegerField(default=0)
    gols_visitante = models.PositiveIntegerField(default=0)

    pontos = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'jogo')

    def __str__(self):
        return f'{self.usuario.username} - {self.jogo}'