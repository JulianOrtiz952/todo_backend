from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import JsonResponse
from todos.views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("", health),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
