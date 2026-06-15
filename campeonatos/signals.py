from django.db.models.signals import post_save
from django.dispatch import receiver
from campeonatos.models import Jogo
from campeonatos.utils import recalcular_tudo


@receiver(post_save, sender=Jogo)
def jogo_finalizado(sender, instance, created, **kwargs):

    if created:
        return

    if (
        instance.encerrado
        or instance.gols_casa is None
        or instance.gols_visitante is None
    ):
        recalcular_tudo()