from django.contrib import admin
from django.urls import path
from app.views import simple_view

urlpatterns = [
    path("", simple_view),
    path('admin/', admin.site.urls),
]
