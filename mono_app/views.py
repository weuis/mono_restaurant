from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.contrib import messages

from mono_app.models import Dish, Cook, DishType


def index(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all()
    cooks = Cook.objects.all()
    dish_types = DishType.objects.all()
    latest_dishes = Dish.objects.select_related("dish_type").prefetch_related("cooks")[:6]
    top_cooks = Cook.objects.order_by("-years_of_experience")[:4]
    return render(
        request,
        "mono_app/index.html",
        context={
            "dishes": dishes,
            "cooks": cooks,
            "dish_types": dish_types,
            "latest_dishes": latest_dishes,
            "top_cooks": top_cooks,
        }
    )


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mono_app:index')

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'
    success_url = reverse_lazy('mono_app:index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully. Come back soon!.")
        return super().dispatch(request, *args, **kwargs)
