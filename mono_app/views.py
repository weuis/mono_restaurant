from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Q

from mono_app.models import Dish, Cook, DishType, Ingredient


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


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = 'mono_app/dish_detail.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chefs'] = self.object.cooks.all()
        return context


class DishUpdateView(generic.UpdateView):
    model = Dish
    fields = ['name', 'description', 'dish_type', 'cooks']
    template_name = 'mono_app/dish_update.html'

    def form_valid(self, form):
        messages.success(self.request, "Dish updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mono_app:dish-detail', kwargs={'pk': self.object.pk})


class DishCreateView(generic.CreateView):
    model = Dish
    fields = ['name', 'description', 'dish_type', 'cooks', 'image']
    template_name = 'mono_app/dish_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Dish created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mono_app:dish-list')

class DishDeleteView(generic.DeleteView):
    model = Dish
    template_name = 'mono_app/dish_confirm_delete.html'
    success_url = reverse_lazy('mono_app:dish-list')


class CooksListView(generic.ListView):
    model = Cook
    template_name = 'mono_app/cooks.html'
    context_object_name = 'cooks'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                username__icontains=search_query
            ) | queryset.filter(
                first_name__icontains=search_query
            ) | queryset.filter(
                last_name__icontains=search_query
            )
        return queryset.order_by('-years_of_experience')


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = 'mono_app/dish_type_list.html'
    context_object_name = 'dish_types'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(name__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = 'mono_app/ingredient_list.html'
    context_object_name = 'ingredients'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(unit__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
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

