from django.urls import path
from mono_app.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "mono_app"
