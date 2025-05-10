from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from mono_app.models import DishType, Dish


class PublicDishListViewTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Burger")
        Dish.objects.create(
            name="Cheeseburger",
            description="With cheddar and pickles",
            price=5.50,
            dish_type=self.dish_type
        )

    def test_dish_list_view_status_code(self):
        url = reverse("mono_app:dish-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cheeseburger")

    def test_dish_filter_by_type(self):
        url = reverse("mono_app:dish-list") + "?type=Burger"
        response = self.client.get(url)
        self.assertContains(response, "Cheeseburger")


class CookLoginRequiredTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user", password="pass"
        )

    def test_redirect_if_not_logged_in(self):
        url = reverse("mono_app:personal-profile")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/login/?next={url}")

    def test_logged_in_user_can_access_profile(self):
        self.client.login(username="user", password="pass")
        url = reverse("mono_app:personal-profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
