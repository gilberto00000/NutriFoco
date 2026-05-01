from django.urls import path
from .views import (
    CriarRegistroDiarioView,
    DashboardPacienteView,
    NutritionPlanCreateView,
    NutritionPlanDeleteView,
    NutritionPlanListView,
    NutritionPlanUpdateView,
)

urlpatterns = [
    path('planos/', NutritionPlanListView.as_view(), name='nutrition_plan_list'),
    path('planos/novo/', NutritionPlanCreateView.as_view(), name='nutrition_plan_create'),
    path('planos/<int:pk>/editar/', NutritionPlanUpdateView.as_view(), name='nutrition_plan_update'),
    path('planos/<int:pk>/excluir/', NutritionPlanDeleteView.as_view(), name='nutrition_plan_delete'),
    path('dashboard/', DashboardPacienteView.as_view(), name='dashboard_paciente'),
    path('diario/novo/', CriarRegistroDiarioView.as_view(), name='novo_registro'),
]