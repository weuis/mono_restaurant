from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from mono_app.models import DishType, Ingredient, Cook, Dish

@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "is_allergen", "unit", "quantity")
    list_filter = ("is_allergen", "unit")
    search_fields = ("name",)

@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "specialization", "years_of_experience")
    list_filter = ("specialization",)
    search_fields = ("username", "first_name", "last_name", "specialization")

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "dish_type", "price", "is_vegetarian")
    list_filter = ("is_vegetarian", "dish_type")
    search_fields = ("name", "description")
    filter_horizontal = ("cooks", "ingredients")

