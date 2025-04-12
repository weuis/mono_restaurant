from django.urls import path
from mono_app.views import index,DishListView

urlpatterns = [
    path("", index, name="index"),
    path('dishes/', DishListView.as_view(), name='dish-list'),
]

app_name = "mono_app"
