from django.contrib import admin
from .models import Prova, ProvaJob


@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "user", "questoes", "created_at")
    search_fields = ("titulo", "descricao", "user__email", "user__username")
    list_filter = ("created_at",)
    autocomplete_fields = ("user",)


@admin.register(ProvaJob)
class ProvaJobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tipo", "status", "questoes", "progress", "created_at", "updated_at")
    list_filter = ("tipo", "status", "created_at")
    search_fields = ("user__email", "user__username", "texto", "pdf_name")
    autocomplete_fields = ("user", "prova")

