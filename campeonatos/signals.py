from django.db.models.signals import post_save
from django.dispatch import receiver
from campeonatos.models import Jogo
from campeonatos.utils import calcular_pontos_jogo


@receiver(post_save, sender=Jogo)
def jogo_finalizado(sender, instance, created, **kwargs):

    if created:
        return

    # sempre pega estado atualizado do banco
    instance.refresh_from_db()

    if instance.encerrado and not instance.pontos_calculados:

        calcular_pontos_jogo(instance.id)

        instance.pontos_calculados = True
        instance.save(update_fields=['pontos_calculados'])