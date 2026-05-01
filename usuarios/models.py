from django.db import models
from django.conf import settings
from nutriFoco.models import BaseModel

User = settings.AUTH_USER_MODEL


class Patient(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients')

    height = models.FloatField()  # metros
    initial_weight = models.FloatField()
    goal = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user}"


class Progress(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='progress')

    date = models.DateField(auto_now_add=True)
    weight = models.FloatField()
    imc = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.patient.height:
            self.imc = self.weight / (self.patient.height ** 2)
        super().save(*args, **kwargs)


class Food(BaseModel):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()

    def __str__(self):
        return self.name


class NutritionPlan(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='plans')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Plano - {self.patient}"


class Meal(BaseModel):
    plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, related_name='meals')

    name = models.CharField(max_length=50)
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.plan}"


class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    quantity = models.FloatField()  # gramas

    def __str__(self):
        return f"{self.food} - {self.quantity}g"


class DailyLog(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='logs')

    date = models.DateField()
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    followed = models.BooleanField()

    def __str__(self):
        return f"{self.patient} - {self.date}"