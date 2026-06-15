from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.png'
    )

    pontuacao_total = models.IntegerField(
        default=0
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.first_name or self.user.username or self.user.email