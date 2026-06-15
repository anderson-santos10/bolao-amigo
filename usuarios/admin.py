from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'image','pontuacao_total','criado_em')
    
    def email(self, obj):
        return obj.user.email