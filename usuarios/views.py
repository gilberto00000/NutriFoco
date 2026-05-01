from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, RedirectView, UpdateView

from contas.mixins import NutritionistRequiredMixin, PatientRequiredMixin
from .forms import NutritionPlanForm
from .models import NutritionPlan, Patient


class NutritionPlanListView(LoginRequiredMixin, NutritionistRequiredMixin, ListView):
    model = NutritionPlan
    template_name = 'usuarios/planos_alimentares_lista.html'
    context_object_name = 'plans'
    paginate_by = 8

    def get_queryset(self):
        queryset = NutritionPlan.objects.filter(nutritionist=self.request.user).select_related(
            'patient', 'patient__user'
        ).order_by('-start_date')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(patient__user__first_name__icontains=query) |
                Q(patient__user__username__icontains=query)
            )
        return queryset


class NutritionPlanCreateView(LoginRequiredMixin, NutritionistRequiredMixin, CreateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'usuarios/plano_alimentar_formulario.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['patient'].queryset = Patient.objects.filter(
            Q(nutritionist=self.request.user) | Q(nutritionist__isnull=True)
        ).select_related('user')
        return form

    def form_valid(self, form):
        form.instance.nutritionist = self.request.user
        patient = form.cleaned_data['patient']
        if patient.nutritionist_id is None:
            patient.nutritionist = self.request.user
            patient.save(update_fields=['nutritionist'])
        return super().form_valid(form)


class NutritionPlanUpdateView(LoginRequiredMixin, NutritionistRequiredMixin, UpdateView):
    model = NutritionPlan
    form_class = NutritionPlanForm
    template_name = 'usuarios/plano_alimentar_formulario.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_queryset(self):
        return NutritionPlan.objects.filter(nutritionist=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['patient'].queryset = Patient.objects.filter(nutritionist=self.request.user)
        return form


class NutritionPlanDeleteView(LoginRequiredMixin, NutritionistRequiredMixin, DeleteView):
    model = NutritionPlan
    template_name = 'shared/confirmar_exclusao.html'
    success_url = reverse_lazy('nutrition_plan_list')

    def get_queryset(self):
        return NutritionPlan.objects.filter(nutritionist=self.request.user)


class DashboardPacienteView(LoginRequiredMixin, PatientRequiredMixin, RedirectView):
    pattern_name = 'patient_limited_area'


class CriarRegistroDiarioView(LoginRequiredMixin, PatientRequiredMixin, RedirectView):
    pattern_name = 'patient_limited_area'