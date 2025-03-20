from django.urls import path

from promy.internal.views import health_check
from promy.station.views import query_publisher

urlpatterns = [
    path(
        "health",
        health_check,
        name="health_check",
    ),
    path("station/publisher/query", query_publisher),
]
