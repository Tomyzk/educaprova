from rest_framework import serializers
from .models import Prova, ProvaJob


class ProvaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prova
        fields = ["id", "titulo", "descricao", "questoes", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProvaJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvaJob
        fields = [
            "id",
            "tipo",
            "status",
            "progress",
            "texto",
            "pdf_name",
            "questoes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "progress", "created_at", "updated_at"]
