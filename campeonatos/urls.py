from django.urls import path
from usuarios.views import regras_bolao_view
from . import views

urlpatterns = [
    path('fazer-palpites/', views.fazer_palpites, name='fazer_palpites'),
    path('ranking/', views.ranking, name='ranking'),
    path('regras/', regras_bolao_view, name='regras_bolao'),
]


