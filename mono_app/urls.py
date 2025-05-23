from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mono_app.views import (
    index,
    CookProfileView,
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView,
    CooksListView,
    CookDetailView,
    CookCreateView,
    CookUpdateView,
    CookDeleteView,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    IngredientListView,
    IngredientDetailView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
)

urlpatterns = [
    path("", index, name="index"),
    path("personal_profile/", CookProfileView.as_view(), name="personal-profile"),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('dishes/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('dishes/create/', DishCreateView.as_view(), name='dish-create'),
    path('dishes/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dishes/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),

    path('cooks/', CooksListView.as_view(), name='cooks'),
    path('cooks/<int:pk>/', CookDetailView.as_view(), name='cook-detail'),
    path('cooks/create/', CookCreateView.as_view(), name='cook-create'),
    path('cooks/<int:id>/update/', CookUpdateView.as_view(), name='cook-update'),
    path('cooks/<int:id>/delete/', CookDeleteView.as_view(), name='cook-delete'),
    path('dishtypes/', DishTypeListView.as_view(),name='dish-types'),
    path("dishtypes/<int:pk>/", DishTypeDetailView.as_view(), name="dish_type_detail"),
    path("dishtypes/create/", DishTypeCreateView.as_view(), name="dish_type_create"),
    path("dishtypes/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish_type_update"),
    path("dishtypes/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish_type_delete"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("ingredients/create/", IngredientCreateView.as_view(), name="ingredient_create"),
    path("ingredients/<int:pk>/", IngredientDetailView.as_view(), name="ingredient_detail"),
    path("ingredients/<int:pk>/update/", IngredientUpdateView.as_view(), name="ingredient_update"),
    path("ingredients/<int:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "mono_app"
