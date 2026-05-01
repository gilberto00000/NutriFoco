from django.urls import path
from .views import DashboardPacienteView, CriarRegistroDiarioView

urlpatterns = [
    # Caminho para ver os planos alimentares
    path('dashboard/', DashboardPacienteView.as_view(), name='dashboard_paciente'),
    
    # Caminho para o paciente registrar o que comeu
    path('diario/novo/', CriarRegistroDiarioView.as_view(), name='novo_registro'),
]