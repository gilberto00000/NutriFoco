from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import NutritionPlan, DailyLog, Patient

#Tela principal do cliente (Lista de Planos)
class DashboardPacienteView(LoginRequiredMixin, ListView):
    model = NutritionPlan
    template_name = 'paciente/dashboard.html'
    context_object_name = 'planos'
    paginate_by = 5 

    def get_queryset(self):
        # pega os planos onde o paciente é o usuário logado
        return NutritionPlan.objects.filter(patient__user=self.request.user).order_by('-id')

#Onde o paciente registra se seguiu a dieta
class CriarRegistroDiarioView(LoginRequiredMixin, CreateView):
    model = DailyLog
    fields = ['date', 'meal', 'followed']
    template_name = 'paciente/registro_form.html'
    success_url = '/usuarios/dashboard/'

    def form_valid(self, form):
        # Vincula o registro ao perfil de paciente (ou de quem logar)
        form.instance.patient = Patient.objects.get(user=self.request.user)
        return super().form_valid(form)