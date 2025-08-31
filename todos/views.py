from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("completed", "-created_at")
    serializer_class = TaskSerializer

    # filtro por query param (sigue disponible)
    def get_queryset(self):
        qs = super().get_queryset()
        completed = self.request.query_params.get("completed")
        if completed is not None:
            val = str(completed).lower() in ("1", "true", "t", "yes", "y")
            qs = qs.filter(completed=val)
        return qs

    @action(detail=False, methods=["get"], url_path="completed")
    def completed(self, request):
        qs = self.get_queryset().filter(completed=True)
        s = self.get_serializer(qs, many=True)
        return Response(s.data)

    @action(detail=False, methods=["get"], url_path="pending")
    def pending(self, request):
        qs = self.get_queryset().filter(completed=False)
        s = self.get_serializer(qs, many=True)
        return Response(s.data)

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        return Response({
            "total": Task.objects.count(),
            "completed": Task.objects.filter(completed=True).count(),
            "pending": Task.objects.filter(completed=False).count(),
        })
    queryset = Task.objects.all().order_by("completed", "-created_at")
    serializer_class = TaskSerializer