from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from mono_app.models import Dish, Cook, DishType, Ingredient


# Custom mixin for admin-only views
class AdminRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def index(request: HttpRequest) -> HttpResponse:
    dishes = Dish.objects.all()
    cooks = Cook.objects.all()
    dish_types = DishType.objects.all()
    latest_dishes = Dish.objects.select_related("dish_type").prefetch_related("cooks")[:6]
    top_cooks = Cook.objects.order_by("-years_of_experience")[:4]
    return render(
        request,
        "mono_app/index.html",
        {
            "dishes": dishes,
            "cooks": cooks,
            "dish_types": dish_types,
            "latest_dishes": latest_dishes,
            "top_cooks": top_cooks,
        }
    )


# ----------------- DISH ----------------- #

class DishListView(generic.ListView):
    model = Dish
    template_name = 'mono_app/dish/dishes_list.html'
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
    template_name = 'mono_app/dish/dish_detail.html'
    context_object_name = 'dish'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chefs'] = self.object.cooks.all()
        return context


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = ['name', 'description', 'dish_type', 'cooks', 'image']
    template_name = 'mono_app/dish/dish_create.html'

    def form_valid(self, form):
        messages.success(self.request, "Dish created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mono_app:dish-list')


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    fields = ['name', 'description', 'dish_type', 'cooks']
    template_name = 'mono_app/dish/dish_update.html'

    def form_valid(self, form):
        messages.success(self.request, "Dish updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mono_app:dish-detail', kwargs={'pk': self.object.pk})


class DishDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = 'mono_app/dish/dish_confirm_delete.html'
    success_url = reverse_lazy('mono_app:dish-list')


# ----------------- COOK ----------------- #

class CooksListView(generic.ListView):
    model = Cook
    template_name = 'mono_app/cooks/cooks.html'
    context_object_name = 'cooks'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return queryset.order_by('-years_of_experience')


class CookDetailView(generic.DetailView):
    model = Cook
    template_name = 'mono_app/cooks/cook_detail.html'
    context_object_name = 'cook'


class CookCreateView(AdminRequiredMixin, generic.CreateView):
    model = Cook
    fields = [
        'username', 'first_name', 'last_name',
        'years_of_experience', 'bio',
        'specialization', 'profile_picture'
    ]
    template_name = 'mono_app/cooks/cooks_create.html'
    success_url = reverse_lazy('cooks-list')

    def form_valid(self, form):
        if not form.cleaned_data.get("specialization"):
            form.add_error("specialization", "Specialization is required.")
            return self.form_invalid(form)
        if not form.cleaned_data.get("profile_picture"):
            form.add_error("profile_picture", "Please upload a profile picture.")
            return self.form_invalid(form)

        messages.success(self.request, "Cook created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please fix the errors below.")
        return super().form_invalid(form)


class CookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Cook
    fields = ['years_of_experience', 'bio', 'specialization', 'profile_picture']
    template_name = 'mono_app/cooks/cook_update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Cook, id=self.kwargs['id'])

    def test_func(self):
        cook = self.get_object()
        return self.request.user.is_staff or self.request.user == cook

    def form_valid(self, form):
        messages.success(self.request, "Cook updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('mono_app:cooks')


class CookDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = 'mono_app/cooks/cook_confirm_delete.html'
    context_object_name = 'cook'
    success_url = reverse_lazy('mono_app:cooks')

    def get_object(self, queryset=None):
        return get_object_or_404(Cook, id=self.kwargs['id'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cook has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# ----------------- DISH TYPE ----------------- #

class DishTypeListView(generic.ListView):
    model = DishType
    template_name = 'mono_app/dish_type/dish_type_list.html'
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


class DishTypeDetailView(generic.DetailView):
    model = DishType
    template_name = "mono_app/dish_type/dish_type_detail.html"
    context_object_name = "dish_type"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dish_type = self.get_object()
        dishes = dish_type.dishes.prefetch_related("cooks").all()
        context["dishes"] = dishes
        context["dish_count"] = dishes.count()
        context["vegetarian_dishes"] = dishes.filter(is_vegetarian=True)
        context["cooks"] = set(cook for dish in dishes for cook in dish.cooks.all())
        return context


class DishTypeCreateView(AdminRequiredMixin, generic.CreateView):
    model = DishType
    fields = ['name']
    template_name = "mono_app/dish_type/dish_type_create.html"
    success_url = reverse_lazy("dish_type_list")

    def form_valid(self, form):
        name = form.cleaned_data['name'].strip()
        if DishType.objects.filter(name__iexact=name).exists():
            form.add_error('name', "A dish type with this name already exists.")
            return self.form_invalid(form)

        form.instance.name = name
        messages.success(self.request, f"Dish type '{name}' was created successfully.")
        return super().form_valid(form)


class DishTypeUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = DishType
    fields = ['name']
    template_name = "mono_app/dish_type/dish_type_update.html"
    success_url = reverse_lazy("dish_type_list")
    context_object_name = "dish_type"

    def form_valid(self, form):
        name = form.cleaned_data['name'].strip()
        if DishType.objects.filter(name__iexact=name).exclude(pk=self.object.pk).exists():
            form.add_error('name', "A dish type with this name already exists.")
            return self.form_invalid(form)

        form.instance.name = name
        messages.success(self.request, f"Dish type '{name}' was successfully updated.")
        return super().form_valid(form)


class DishTypeDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "mono_app/dish_type/dish_type_delete.html"
    success_url = reverse_lazy("dish_type_list")
    context_object_name = "dish_type"

    def delete(self, request, *args, **kwargs):
        dish_type = self.get_object()
        messages.success(request, f"Dish type '{dish_type.name}' was successfully deleted.")
        return super().delete(request, *args, **kwargs)


# ----------------- INGREDIENT ----------------- #

class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = 'mono_app/ingredients/ingredient_list.html'
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


class IngredientDetailView(generic.DetailView):
    model = Ingredient
    template_name = 'mono_app/ingredients/ingredient_detail.html'
    context_object_name = 'ingredient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ingredient = self.get_object()
        context['dishes_with_ingredient'] = ingredient.dishes.all()
        return context


class IngredientCreateView(AdminRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = ['name', 'is_allergen', 'unit', 'quantity']
    template_name = 'mono_app/ingredients/ingredient_create.html'
    success_url = reverse_lazy('ingredient_list')

    def form_valid(self, form):
        name = form.cleaned_data['name'].strip()
        if Ingredient.objects.filter(name__iexact=name).exists():
            form.add_error('name', 'An ingredient with this name already exists.')
            return self.form_invalid(form)

        form.instance.name = name
        messages.success(self.request, f"Ingredient '{name}' was successfully created.")
        return super().form_valid(form)


class IngredientUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = ['name', 'is_allergen', 'unit', 'quantity']
    template_name = 'mono_app/ingredients/ingredient_update.html'
    context_object_name = 'ingredient'
    success_url = reverse_lazy('ingredient_list')

    def form_valid(self, form):
        name = form.cleaned_data['name'].strip()
        if Ingredient.objects.filter(name__iexact=name).exclude(pk=self.object.pk).exists():
            form.add_error('name', 'An ingredient with this name already exists.')
            return self.form_invalid(form)

        form.instance.name = name
        messages.success(self.request, f"Ingredient '{name}' was successfully updated.")
        return super().form_valid(form)


class IngredientDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = 'mono_app/ingredients/ingredient_confirm_delete.html'
    success_url = reverse_lazy('ingredient_list')
    context_object_name = 'ingredient'

    def delete(self, request, *args, **kwargs):
        ingredient = self.get_object()
        messages.success(request, f"Ingredient '{ingredient.name}' was successfully deleted.")
        return super().delete(request, *args, **kwargs)


# ----------------- AUTH ----------------- #

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
