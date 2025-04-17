from django.urls import path
from mono_app.views import (
    index,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    CooksListView,
    DishTypeListView,
    IngredientListView,
)

urlpatterns = [
    path("", index, name="index"),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('dishes/create/', DishCreateView.as_view(), name='dish-create'),
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),

    path('cooks/', CooksListView.as_view(), name='cooks'),
    path('dishtypes/', DishTypeListView.as_view(),name='dish-types'),
path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
]

app_name = "mono_app"
