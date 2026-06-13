from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        upload_to='profiles/',
        default='profiles/default.jpg'
    )

    pontuacao_total = models.IntegerField(
        default=0
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.first_name or self.user.username