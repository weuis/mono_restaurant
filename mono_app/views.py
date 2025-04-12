from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic

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


class DishListView(generic.ListView):
    model = Dish
    template_name = 'mono_app/dishes_list.html'
    context_object_name = 'dishes'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        dish_type = self.request.GET.get('type')
        search_query = self.request.GET.get('q')

        if dish_type:
            queryset = queryset.filter(dish_type__name__iexact=dish_type)

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dish_types'] = DishType.objects.all()
        context['selected_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mono_app:index')

class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully. Come back soon!")
        return super().dispatch(request, *args, **kwargs)

