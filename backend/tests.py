from django.test import Client, TestCase

from .models import *
# Create your tests here.

class LoginTestCase(TestCase):
    def setUp(self):

        # Create airports.
        a1 = Category.objects.create(name="category1", slug="category1")
        user = User.objects.create(username="ferry", email="ferry@gmail.com", email_verified=1)
        user.set_password('password')
        user.save()        

    def test_valid_flight_page(self):
        a1 = Category.objects.get(name="category1")

        c = Client()
        response = c.get(f"/api/category/{a1.id}")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        
        u2 = {'username': 'ferry', 'password': 'password'}
        # u1 = User.objects.all()
        u1 = User.objects.get(username='ferry')
        for user in u1:
            data = {'username': user.username, 'password': user.password}    
            c = Client()
            print(type(u1))
            print(type(u2))
            response = c.post('/api/user_login', data=data)
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the expected content
        # self.assertContains(response, 'You submitted: bar')
        # u1 = User.objects.filter(username="ferry")
        # c = Client()
        # print(u1)
        # response = c.post(f"/api/user_login", data=u1)
        # self.assertEqual(response.status_code, 200)