from django.urls import path
from mono_app.views import (
    index,
    DishListView,
    CooksListView,
    DishTypeListView,
    IngredientListView
)

urlpatterns = [
    path("", index, name="index"),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('cooks/', CooksListView.as_view(), name='cooks'),
    path('dishtypes/', DishTypeListView.as_view(),name='dish-types'),
path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
]

app_name = "mono_app"
