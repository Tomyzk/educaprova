from django.conf import settings
from django.db import models
from django.utils import timezone


class Prova(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="provas")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    questoes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.titulo} ({self.user})"


class ProvaJob(models.Model):
    class Tipo(models.TextChoices):
        GERAR = "GERAR", "Gerar"
        IMPORTAR_PDF = "IMPORTAR_PDF", "Importar PDF"

    class Status(models.TextChoices):
        PROCESSANDO = "processando", "Processando"
        CONCLUIDO = "concluido", "Concluído"
        CANCELADO = "cancelado", "Cancelado"
        ERRO = "erro", "Erro"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="jobs")
    prova = models.ForeignKey(Prova, null=True, blank=True, on_delete=models.SET_NULL, related_name="jobs")
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PROCESSANDO)
    progress = models.PositiveIntegerField(default=0)
    texto = models.TextField(blank=True)
    pdf_name = models.CharField(max_length=255, blank=True)
    questoes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Job {self.id} ({self.tipo} - {self.status})"
