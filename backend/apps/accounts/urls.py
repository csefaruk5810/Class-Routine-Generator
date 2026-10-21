from django.http import JsonResponse
from django.urls import path


def auth_healthcheck(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", auth_healthcheck, name="auth-health"),
]

