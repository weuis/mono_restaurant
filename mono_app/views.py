from django.http import HttpRequest
from django.shortcuts import render

from .models import Dish, Cook, DishType


def index(request: HttpRequest):
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    latest_dishes = Dish.objects.select_related("dish_type").prefetch_related("cooks")[:6]
    top_cooks = Cook.objects.order_by("-years_of_experience")[:4]

    return render(
        request,
        "mono_app/index.html",
        context={
            "num_dishes": num_dishes,
            "num_cooks": num_cooks,
            "num_dish_types": num_dish_types,
            "latest_dishes": latest_dishes,
            "top_cooks": top_cooks,
        }
    )
