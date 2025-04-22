from django.test import TestCase
from django.contrib.auth import get_user_model
from mono_app.models import DishType, Ingredient, Dish, Cook


class DishModelTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(name="Pizza")
        self.ingredient = Ingredient.objects.create(name="Tomato", unit="grams", quantity=100, is_allergen=False)
        self.cook = get_user_model().objects.create_user(
            username="chef1", password="testpass123", years_of_experience=5
        )

    def test_create_dish(self):
        dish = Dish.objects.create(
            name="Margherita",
            description="Classic pizza with tomato and cheese",
            price=8.99,
            dish_type=self.dish_type
        )
        dish.ingredients.add(self.ingredient)
        dish.cooks.add(self.cook)

        self.assertEqual(str(dish), "Margherita")
        self.assertIn(self.ingredient, dish.ingredients.all())
        self.assertIn(self.cook, dish.cooks.all())


class CookModelTests(TestCase):
    def test_create_cook(self):
        cook = get_user_model().objects.create_user(
            username="testcook", password="pass", years_of_experience=3
        )
        self.assertEqual(cook.username, "testcook")
        self.assertEqual(cook.years_of_experience, 3)
        self.assertTrue(cook.check_password("pass"))

