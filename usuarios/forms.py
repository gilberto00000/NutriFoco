from django import forms

from .models import DailyLog, NutritionPlan


class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['patient', 'start_date', 'end_date', 'plan_text', 'active']
        labels = {
            'patient': 'Paciente',
            'start_date': 'Data de inicio',
            'end_date': 'Data de fim',
            'plan_text': 'Plano alimentar',
            'active': 'Plano ativo',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'plan_text': forms.Textarea(attrs={'rows': 10, 'placeholder': '07:00 - ...'}),
        }


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ['date', 'meal', 'followed']
        labels = {
            'date': 'Data',
            'meal': 'Refeicao',
            'followed': 'Seguiu o plano?',
        }
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
