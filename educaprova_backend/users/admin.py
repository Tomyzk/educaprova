from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-date_joined",)
    list_display = ("id", "email", "username", "first_name", "last_name", "plan", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "plan")
    search_fields = ("email", "username", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("username", "first_name", "last_name", "plan", "is_guest", "guest_expires_at")} ),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login", "date_joined", "created_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "first_name", "last_name", "plan", "is_staff", "is_active"),
            },
        ),
    )

    readonly_fields = ("date_joined", "created_at", "last_login")

    # Use email as the primary identifier in forms
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if hasattr(form.base_fields.get("username"), "required"):
            form.base_fields["username"].required = True
        return form

