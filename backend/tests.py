from django.test import Client, TestCase, RequestFactory
from django.urls import reverse
import random
from .models import *
from random import randint
import json
import requests
from datetime import datetime
from django.contrib.auth.models import User
from backend.models import User

from frontend.views import profile

# Create your tests here.

#region Front-end

##### FRONT-END TESTS #####
class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_profile_view(self):
        url = reverse('profile')  # Replace 'profile' with the actual URL name for your profile view
        self.client.force_login(self.user)

        # Mock the response from the external API
        mock_response = {
            "skill1": "value1",
            "skill2": "value2"
        }
        requests.get = lambda url: MockResponse(json_data=mock_response)

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'isit950/account/profile/dashboard-profile.html')
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.context['skills'], mock_response)

class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


from frontend.views import tasks

class TasksViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_tasks_view(self):
        url = reverse('tasks')  # Replace 'tasks' with the actual URL name for your tasks view

        # Mock the response from the external API
        mock_response = [
            {"task": "Task 1"},
            {"task": "Task 2"}
        ]
        requests.get = lambda url: MockResponse(json_data=mock_response)

        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'isit950/index.html')
        self.assertEqual(response.context['tasks'], mock_response)
        self.assertEqual(response.context['user'], self.user)
        self.assertFalse('usid' not in response.cookies)  # Verify that 'usid' cookie is not set
    
    def test_tasks_view2(self):
        url = reverse('tasks')  # Replace 'tasks' with the actual URL name for your tasks view

        # Mock the response from the external API
        mock_response = [
            { "id": 1, "category_name": "Bicycle Repair", "user_client_id": "tina", "img_profile": "null", "rating": 0.0, "first_name": "Xinyu", "last_name": "Chen", "task_title_to_url": "Kids-bike-service1-1", "my_bookmark": [ 1, 3, 2 ], "task_title": "Kids bike service1", "description": "I have 3 kids bike I want serviced to make sure they’re good to ride (Trek 12 inch, Cannondale 16 inch and Liv Adore 16 inch)", "price": "150.00", "booking_price": "0.00", "total_price": "0.00", "location": "Wollongong NSW, Australia", "location_link": "https://goo.gl/maps/CV7LYozNvraBYJBQ8", "lat": -34.424394, "long": 150.89385, "completed_on": "2023-04-29", "status": 1, "is_paid": "false", "create_date": "2023-05-08T14:05:19", "modify_date": "2023-05-21T14:05:45", "offer": "false", "category": 2, "user": 6, "user_provider": "null" },
            { "id": 2, "category_name": "Locksmith", "user_client_id": "anne", "user_provider_name": "ferry", "img_profile": "null", "rating": 0.0, "first_name": "Min Anne", "last_name": "Tan", "task_title_to_url": "Door-lock-fixed-2", "my_bookmark": [ 3, 1 ], "task_title": "Door lock fixed", "description": "Door handle is hard to open from the outside and inside will need someone who can fix or change it.", "price": "40.00", "booking_price": "6.00", "total_price": "46.00", "location": "Wollongong NSW, Australia", "location_link": "https://goo.gl/maps/CV7LYozNvraBYJBQ8", "lat": -34.424394, "long": 150.89385, "completed_on": "2023-05-22", "status": 1, "is_paid": 'false', "create_date": "2023-05-08T14:05:26", "modify_date": "2023-05-21T14:05:46", "offer": "false", "category": 1, "user": 3, "user_provider": 1 }
            ]
        requests.get = lambda url: MockResponse(json_data=mock_response)

        self.client.force_login(self.user)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'isit950/index.html')
        self.assertEqual(response.context['tasks'], mock_response)
        self.assertEqual(response.context['user'], self.user)

class MockResponse:
    def __init__(self, json_data=None, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
    

# from requests.models import PreparedRequest
# from frontend.views import updateCompletion

# class UpdateCompletionViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username='testuser', password='testpassword')

#     def test_update_completion_view_success(self):
#         url = reverse('update_completion', args=['task_id', 'client_id'])  # Replace 'update_completion' with the actual URL name for your updateCompletion view
#         request = self.factory.get(url)
#         request.user = self.user

#         # Mock the request's put method
#         def mock_put(request: PreparedRequest, **kwargs):
#             return MockResponse(status_code=200)

#         with requests.Session() as session:
#             session.put = mock_put
#             response = updateCompletion(request, 'task_id', 'client_id')

#         self.assertRedirects(response, reverse('tasks') + '?name=task_id')
#         self.assertContains(response, "You have completed task.")
#         self.assertEqual(len(response.context['messages']), 1)
#         self.assertEqual(response.context['messages'][0].level, 25)  # 25 corresponds to the 'success' level

#     def test_update_completion_view_error(self):
#         url = reverse('update_completion', args=['task_id', 'client_id'])  # Replace 'update_completion' with the actual URL name for your updateCompletion view
#         request = self.factory.get(url)
#         request.user = self.user

#         # Mock the request's put method
#         def mock_put(request: PreparedRequest, **kwargs):
#             return MockResponse(status_code=500)

#         with requests.Session() as session:
#             session.put = mock_put
#             response = updateCompletion(request, 'task_id', 'client_id')

#         self.assertRedirects(response, reverse('tasks') + '?name=task_id')
#         self.assertContains(response, "Error when completing task.")
#         self.assertEqual(len(response.context['messages']), 1)
#         self.assertEqual(response.context['messages'][0].level, 40)  # 40 corresponds to the 'error' level

# class MockResponse:
#     def __init__(self, status_code):
#         self.status_code = status_code

#endregion


#region Back-end

##### BACKEND TESTS #####

class FunctionsTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="category1", slug="category1")
        user = User.objects.create(username="ferry", email="ferry@gmail.com", first_name="Ferry",last_name="Susanto", email_verified=1)
        user.set_password('password')
        user.save() 
        task=Task.objects.create(task_title = "Kids bike service1",
        category=category,
        description ="I have 3 kids bike I want serviced to make sure they’re good to ride (Trek 12 inch, Cannondale 16 inch and Liv Adore 16 inch)",
        price = 150.00,
        location = "Wollongong NSW, Australia",
        location_link = "https://goo.gl/maps/CV7LYozNvraBYJBQ8",
        lat = -34.424394,long = 150.89385,
        completed_on = "2023-04-29",status = 0,user=user)

        offer=Offer.objects.create(price= 150.00,
        admin_fee=15.00,
        total_price= 165.00,
        description="I am confident to provide with high quality result you are looking for",
        task=task,
        user=user
       )
#-----GetCategory---------------------------
    def test_get_category(self):
        a1 = Category.objects.get(name="category1")
        c = Client()
        response = c.get(f"/api/category/{a1.id}")
        self.assertEqual(response.status_code, 200)
        # Check for the value
        json_data = json.loads(response.content.decode('utf-8'))
        data_to_check = {"name": json_data[0]["name"]}
        data_to_compare = {"name": "category1"}
        self.assertEqual(data_to_check, data_to_compare)
    
    def test_get_category2(self):
        try:
            a1 = Category.objects.get(name="category3")
        except Category.DoesNotExist:
            a1 = ""
        
        c = Client()
        if a1:
            response = c.get(f"/api/category/{a1.id}")
            self.assertEqual(response.status_code, 200)
            # Check for the value
            json_data = json.loads(response.content.decode('utf-8'))
            data_to_check = {"name": json_data[0]["name"]}
            data_to_compare = {"name": "category3"}
            self.assertEqual(data_to_check, data_to_compare)
        else:
            response = c.get(f"/api/category/{a1}")
            self.assertEqual(response.status_code, 404)

#----PostCategory----------------------------    
    def test_post_category(self):
        data={"name":"category2", "slug":"category2"}
        c = Client()
        response = c.post("/api/category", data=data)
        self.assertEqual(response.status_code, 200)
#-------------GetUserProfile-correct username-------------
    def test_get_userProfile1(self):
        user=User.objects.get(username='ferry')
        c = Client()
        response = c.get(f"/api/profile_api/{user.username}")
        self.assertEqual(response.status_code, 200)

    #Register----username not available 400----------------------------------------------------------
    def test_register1(self):
        data = {'username':'ferry','first_name': 'Ferry', 'last_name': 'Susanto','email': 'ferry@gmail.com','password': 'password'}
        c = Client()
        response = c.post('/api/register_api', data=data)
        self.assertEqual(response.status_code, 400)
    #     #Register----username not available 400----------------------------------------------------------
    def test_register1(self):
        data = {'username':'ferry','first_name': 'Ferry', 'last_name': 'Susanto','email': 'ferry@gmail.com','password': 'password'}
        c = Client()
        response = c.post('/api/register_api', data=data)
        self.assertEqual(response.status_code, 400)
    #Register----password too common 400----------------------------------------------------------
    def test_register2(self):
        data = {'username':'ferry','first_name': 'Ferry', 'last_name': 'Susanto','email': 'ferryx@gmail.com','password': 'password'}
        c = Client()
        response = c.post('/api/register_api', data=data)
        self.assertEqual(response.status_code, 400)
    #Register-succeed-------------------------------------------------------------
    def test_register3(self):
        data = {'username':'fersus'+str(randint(100,999)),'first_name': 'Ferry', 'last_name': 'Susanto','email': 'a405595077@gmail.com','password': 'Uow7549647zzzzzzzzzzzz'}
        c = Client()
        response = c.post('/api/register_api', data=data)
        self.assertEqual(response.status_code, 200)
#FORGOTPASSOWRD----200-#getToken--------------------------
    def test_forgotPassword1(self):
        
        data = {"username": "ferry", "email": "ferry@gmail.com"}
        c = Client()
        response = c.post('/api/forgot_password_api', data=data)
        
#         # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
#         #getToken
        print(response.content)
#FORGOTPASSOWRD--------200 #Email is incorrect!"-----------------------     
    def test_forgotPassword2(self):
        
        data = {"username": "ferry", "email": "ferryx@gmail.com"}
        c = Client()
        response = c.post('/api/forgot_password_api', data=data)
        
#         # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)
#         #Email is incorrect!"
        print(response.content)

 #CHANGEPASSOWRD-------------------------------
#change password successfully-----------------------------
    def test_changePassword1(self):
        user=User.objects.get(username="ferry")
        data={"username":"ferry","old_password":"password","password":"password1"}
        c = Client()
        response = c.post(f'/api/change_password/{user.id}', data=data)
        self.assertEqual(response.status_code, 200)

 #old password wrong---400-----------------------------------------
    def test_changePassword2(self):
        user=User.objects.get(username="ferry")
        data={"username":"ferry","old_password":"passwordx","password":"password1"}
        c = Client()
        response = c.post(f'/api/change_password/{user.id}', data=data)
        self.assertEqual(response.status_code, 400)
     
    #LOGIN-use correct username and password--200-----------------------------------------------------------
    def test_login_OK(self):
        
        data = {'username': 'ferry', 'password': 'password'}
        c = Client()
        response = c.post('/api/user_login', data=data)
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

    #LOGIN-use wrong  password--404---------------------------------------------------------
    def test_login_fail(self):
        
        data = {'username': 'ferry', 'password': 'passwordx'}
        c = Client()
        response = c.post('/api/user_login', data=data)
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 404)

     #GET_TASKDETAIL-----------------------------------------------------------
    def test_get_taskdetail(self):
        task=Task.objects.get(task_title="Kids bike service1")
        c = Client()
        response = c.get(f'/api/task/{task.id}')
        self.assertEqual(response.status_code, 200)

#----------------------getOfferDetailForTask----------------
    def test_get_offerDetail(self):
        task=Task.objects.get(task_title = "Kids bike service1")
        c = Client()
        response = c.get(f"/api/offer/{task.id}")
        self.assertEqual(response.status_code, 200)

#endregion