from django.urls import path
from mono_app.views import index,DishListView, CooksListView

urlpatterns = [
    path("", index, name="index"),
    path('dishes/', DishListView.as_view(), name='dish-list'),
    path('cooks/', CooksListView.as_view(), name='cooks')
]

app_name = "mono_app"
