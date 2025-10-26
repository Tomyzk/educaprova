from django.conf import settings
from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Prova, ProvaJob
from .serializers import ProvaSerializer, ProvaJobSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user_id", None) == request.user.id


class ProvaViewSet(viewsets.ModelViewSet):
    serializer_class = ProvaSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Prova.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        total = Prova.objects.filter(user=request.user).count()
        is_free = getattr(request.user, "plan", "FREE") == getattr(request.user.Plan, "FREE", "FREE")
        monthly_limit = settings.EDUCAPROVA.get("FREE_MAX_MONTHLY_ATTEMPTS", 3) if is_free else None
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        attempts = ProvaJob.objects.filter(user=request.user, created_at__gte=month_start).count() if is_free else None
        remaining = max(0, (monthly_limit - attempts)) if is_free else None
        return Response(
            {
                "total": total,
                "plan": request.user.plan,
                "monthly_limit": monthly_limit,
                "attempts_used": attempts,
                "remaining": remaining,
            }
        )

    @action(detail=False, methods=["post"], url_path="gerar")
    def gerar(self, request):
        user = request.user
        texto = request.data.get("texto") or ""
        try:
            questoes = int(request.data.get("questoes", 0))
        except Exception:
            questoes = 0

        if not texto:
            return Response({"detail": "Campo 'texto' é obrigatório."}, status=400)
        if questoes < 1 or questoes > 30:
            return Response({"detail": "'questoes' deve estar entre 1 e 30."}, status=400)

        if user.plan == getattr(user.Plan, "FREE", "FREE"):
            limit = settings.EDUCAPROVA.get("FREE_MAX_MONTHLY_ATTEMPTS", 3)
            now = timezone.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            used = ProvaJob.objects.filter(user=user, created_at__gte=month_start).count()
            if used >= limit:
                return Response({"detail": f"Limite mensal de {limit} tentativas atingido."}, status=403)

        job = ProvaJob.objects.create(
            user=user,
            tipo=ProvaJob.Tipo.GERAR,
            status=ProvaJob.Status.PROCESSANDO,
            texto=texto,
            questoes=questoes,
        )
        return Response(ProvaJobSerializer(job).data, status=201)

    @action(detail=False, methods=["post"], url_path="importar_pdf")
    def importar_pdf(self, request):
        user = request.user
        if user.plan != getattr(user.Plan, "PREMIUM", "PREMIUM"):
            return Response({"detail": "Apenas usuários Premium podem importar PDF."}, status=403)

        pdf = request.FILES.get("pdf")
        try:
            questoes = int(request.data.get("questoes", 0))
        except Exception:
            questoes = 0
        if not pdf:
            return Response({"detail": "Arquivo 'pdf' é obrigatório."}, status=400)
        if questoes < 1 or questoes > 30:
            return Response({"detail": "'questoes' deve estar entre 1 e 30."}, status=400)

        job = ProvaJob.objects.create(
            user=user,
            tipo=ProvaJob.Tipo.IMPORTAR_PDF,
            status=ProvaJob.Status.PROCESSANDO,
            pdf_name=getattr(pdf, "name", "uploaded.pdf"),
            questoes=questoes,
        )
        return Response(ProvaJobSerializer(job).data, status=201)


class JobViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        try:
            job = ProvaJob.objects.get(pk=pk, user=request.user)
        except ProvaJob.DoesNotExist:
            return Response(status=404)
        return Response(ProvaJobSerializer(job).data)

    @action(detail=True, methods=["post"], url_path="cancelar")
    def cancelar(self, request, pk=None):
        try:
            job = ProvaJob.objects.get(pk=pk, user=request.user)
        except ProvaJob.DoesNotExist:
            return Response(status=404)
        if job.status == ProvaJob.Status.PROCESSANDO:
            job.status = ProvaJob.Status.CANCELADO
            job.progress = 0
            job.save()
        return Response(ProvaJobSerializer(job).data)
