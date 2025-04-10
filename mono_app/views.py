from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
