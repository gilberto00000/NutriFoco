from django.contrib import admin

# Register your models here.
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf', 'phone', 'birth_date')
    search_fields = ('user__username', 'cpf')
    from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from contas.models import Profile



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'user_type', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Informações extras', {
            'fields': ('user_type',)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações extras', {
            'fields': ('user_type',)
        }),
    )


admin.site.register(User, CustomUserAdmin)