from django.contrib import admin
from .models import Campeonato, Grupo, Time, Jogo, Palpite


@admin.register(Campeonato)
class CampeonatoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'temporada',
        'rodada_atual',
        'premiacao'
    )


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'campeonato'
    )


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'grupo'
    )


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = (
        'time_casa',
        'time_visitante',
        'data_jogo',
        'encerrado'
    )

    list_filter = (
        'campeonato',
        'encerrado'
    )


@admin.register(Palpite)
class PalpiteAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'jogo',
        'gols_casa',
        'gols_visitante'
    )