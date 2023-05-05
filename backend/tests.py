from django.test import Client,TestCase
from backend.models import Category
import unittest
class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Gardening", slug="Gardening")
    def test_category(self):
        c=Client()
        response=c.get(f"/category/")
        self.assertEqual(response.status_code, 200)


    



