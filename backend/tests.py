# from django.test import Client, TestCase

# from .models import *
# # Create your tests here.

# class LoginTestCase(TestCase):
#     def setUp(self):

#         # Create airports.
#         a1 = Category.objects.create(name="category1", slug="category1")
#         user = User.objects.create(username="ferry", email="ferry@gmail.com", email_verified=1)
#         user.set_password('password')
#         user.save()        

#     def test_valid_flight_page(self):
#         a1 = Category.objects.get(name="category1")

#         c = Client()
#         response = c.get(f"/api/category/{a1.id}")
#         self.assertEqual(response.status_code, 200)

#     def test_login(self):
        
#         u2 = {'username': 'ferry', 'password': 'password'}
#         # u1 = User.objects.all()
#         u1 = User.objects.get(username='ferry')
#         for user in u1:
#             data = {'username': user.username, 'password': user.password}    
#             c = Client()
#             print(type(u1))
#             print(type(u2))
#             response = c.post('/api/user_login', data=data)
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
        
        # Check that the response contains the expected content
        # self.assertContains(response, 'You submitted: bar')
        # u1 = User.objects.filter(username="ferry")
        # c = Client()
        # print(u1)
        # response = c.post(f"/api/user_login", data=u1)
        # self.assertEqual(response.status_code, 200)


from django.test import Client, TestCase
import randomimport random
from .models import *
from random import randint
import json

<<<<<<< HEAD
from random import randint

# Create your tests here.

=======
>>>>>>> 11fe67a (Tests commit)
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
        a1 = Category.objects.get(name="category3")
        c = Client()
        response = c.get(f"/api/category/{a1.id}")
        self.assertEqual(response.status_code, 200)
        # Check for the value
        json_data = json.loads(response.content.decode('utf-8'))
        data_to_check = {"name": json_data[0]["name"]}
        data_to_compare = {"name": "category3"}
        self.assertEqual(data_to_check, data_to_compare)

# #----PostCategory----------------------------    
#     def test_post_category(self):
#         data={"name":"category2", "slug":"category2"}
#         c = Client()
#         response = c.post("/api/category", data=data)
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
# #-------------GetUserProfile-correct username-------------
#     def test_get_userProfile1(self):
#         user=User.objects.get(username='ferry')
#         c = Client()
#         response = c.get(f"/api/profile_api/{user.username}")
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
# #-------------GetUserProfile(WronguserName)--------------
#     def test_get_userProfile2(self):
#         try:
#             user=User.objects.get(username='ferryx')
#         except User.DoesNotExist:
#             print("User.DoesNotExist")
#         # c = Client()
#         # response = c.get(f"/api/profile_api/{user.username}")

#     #Register----username not available 400----------------------------------------------------------
#     def test_register1(self):
#         data = {'username':'ferry','first_name': 'Ferry', 'last_name': 'Susanto','email': 'ferry@gmail.com','password': 'password'}
#         c = Client()
#         response = c.post('/api/register_api', data=data)
#         self.assertEqual(response.status_code, 400)
#         print(response.content)
#     #Register----password too common 400----------------------------------------------------------
#     def test_register2(self):
#         data = {'username':'ferry','first_name': 'Ferry', 'last_name': 'Susanto','email': 'ferryx@gmail.com','password': 'password'}
#         c = Client()
#         response = c.post('/api/register_api', data=data)
#         print(response.content)
#         self.assertEqual(response.status_code, 400)
#     #Register-succeed-------------------------------------------------------------
#     def test_register3(self):
#         data = {'username':'fersus'+str(randint(100,999)),'first_name': 'Ferry', 'last_name': 'Susanto','email': 'a405595077@gmail.com','password': 'Uow7549647zzzzzzzzzzzz'}
#         c = Client()
#         response = c.post('/api/register_api', data=data)
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
# #FORGOTPASSOWRD----200-#getToken--------------------------
#     def test_forgotPassword1(self):
        
#         data = {"username": "ferry", "email": "ferry@gmail.com"}
#         c = Client()
#         response = c.post('/api/forgot_password_api', data=data)
        
# #         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
# #         #getToken
#         print(response.content)
# #FORGOTPASSOWRD--------200 #Email is incorrect!"-----------------------     
#     def test_forgotPassword2(self):
        
#         data = {"username": "ferry", "email": "ferryx@gmail.com"}
#         c = Client()
#         response = c.post('/api/forgot_password_api', data=data)
        
# #         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
# #         #Email is incorrect!"
#         print(response.content)

#  #CHANGEPASSOWRD-------------------------------
# #change password successfully-----------------------------
#     def test_changePassword1(self):
#         user=User.objects.get(username="ferry")
#         data={"username":"ferry","old_password":"password","password":"password1"}
#         c = Client()
#         response = c.post(f'/api/change_password/{user.id}', data=data)
#         self.assertEqual(response.status_code, 200)
#  #old password wrong---400-----------------------------------------
#     def test_changePassword2(self):
#         user=User.objects.get(username="ferry")
#         data={"username":"ferry","old_password":"passwordx","password":"password1"}
#         c = Client()
#         response = c.post(f'/api/change_password/{user.id}', data=data)
#         self.assertEqual(response.status_code, 400)
#         print(response.content)
     
#     #LOGIN-use correct username and password--200-----------------------------------------------------------
#     def test_login_OK(self):
        
#         data = {'username': 'ferry', 'password': 'password'}
#         c = Client()
#         response = c.post('/api/user_login', data=data)
        
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
#     #LOGIN-use wrong  password--404---------------------------------------------------------
#     def test_login_fail(self):
        
#         data = {'username': 'ferry', 'password': 'passwordx'}
#         c = Client()
#         response = c.post('/api/user_login', data=data)
        
<<<<<<< HEAD
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 404)
        print(response.content)
    #CREATE_TASK-----------------------------------------------------------
    def test_create_task(self):
        print(response.content)
    #LOGIN-use wrong  password--404---------------------------------------------------------
    def test_login_fail(self):
        
        data = {'username': 'ferry', 'password': 'passwordx'}
        c = Client()
        response = c.post('/api/user_login', data=data)
        
        # Check that the response status code is 200
        self.assertEqual(response.status_code, 404)
        print(response.content)
    #CREATE_TASK-----------------------------------------------------------
    def test_create_task(self):
=======
#         # Check that the response status code is 200
#         self.assertEqual(response.status_code, 404)
#         print(response.content)
#     #CREATE_TASK-----------------------------------------------------------
#     def test_create_task(self):
>>>>>>> 11fe67a (Tests commit)
        
#         data = {"task_title": "Kids bike service1",
#         "description": "I have 3 kids bike I want serviced to make sure they’re good to ride (Trek 12 inch, Cannondale 16 inch and Liv Adore 16 inch)",
#         "price": 150.00,
#         "location": "Wollongong NSW, Australia",
#         "location_link": "https://goo.gl/maps/CV7LYozNvraBYJBQ8",
#         "lat": -34.424394,
#         "long": 150.89385,
#         "completed_on": "2023-04-29",
#         "status": 0,
#         "user":User.objects.get(username="ferry").id,
#         "category":Category.objects.get(name="category1").id,
#         }
#         c = Client()
#         response = c.post('/api/task', data=data)
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
#      #GET_TASKDETAIL-----------------------------------------------------------
#     def test_get_taskdetail(self):
#         task=Task.objects.get(task_title="Kids bike service1")
#         c = Client()
#         response = c.get(f'/api/task/{task.id}')
#         self.assertEqual(response.status_code, 200)
#         print(response.content)
# #---POSTOFFER-----------------------------------------------------------------------

#     def test_post_offer(self):
#         data = {"price": 150.0,
#         "admin_fee": 15.00,
#         "total_price": 165.00,
#         "description": "I am confident to provide with high quality result you are looking for",
#          "task":Task.objects.get(task_title = "Kids bike service1").id,
#          "user":User.objects.get(username="ferry").id
#         }
#         c = Client()
#         response = c.post('/api/my-task/accept-offer/'+str(data['task'])+'/'+str(data['user']), data=data)
#         self.assertEqual(response.status_code, 200)
# #----------------------getOfferDetailForTask----------------
#     def test_get_offerDetail(self):
#         task=Task.objects.get(task_title = "Kids bike service1")
#         c = Client()
#         response = c.get(f"/api/offer/{task.id}")
#         self.assertEqual(response.status_code, 200)
#         print(response.content)


        data = {"task_title": "Kids bike service1",
        "description": "I have 3 kids bike I want serviced to make sure they’re good to ride (Trek 12 inch, Cannondale 16 inch and Liv Adore 16 inch)",
        "price": 150.00,
        "location": "Wollongong NSW, Australia",
        "location_link": "https://goo.gl/maps/CV7LYozNvraBYJBQ8",
        "lat": -34.424394,
        "long": 150.89385,
        "completed_on": "2023-04-29",
        "status": 0,
        "user":User.objects.get(username="ferry").id,
        "category":Category.objects.get(name="category1").id,
        }
        c = Client()
        response = c.post('/api/task', data=data)
        self.assertEqual(response.status_code, 200)
        print(response.content)
     #GET_TASKDETAIL-----------------------------------------------------------
    def test_get_taskdetail(self):
        task=Task.objects.get(task_title="Kids bike service1")
        c = Client()
        response = c.get(f'/api/task/{task.id}')
        self.assertEqual(response.status_code, 200)
        print(response.content)
#---POSTOFFER-----------------------------------------------------------------------

    # def test_post_offer(self):
    #     data = {"price": 150.0,
    #     "admin_fee": 15.00,
    #     "total_price": 165.00,
    #     "description": "I am confident to provide with high quality result you are looking for",
    #      "task":Task.objects.get(task_title = "Kids bike service1").id,
    #      "user":User.objects.get(username="ferry").id
    #     }
    #     c = Client()
    #     response = c.post('/api/my-task/accept-offer/'+str(data['task'])+'/'+str(data['user']), data=data)
    #     self.assertEqual(response.status_code, 200)
#----------------------getOfferDetailForTask----------------
    def test_get_offerDetail(self):
        task=Task.objects.get(task_title = "Kids bike service1")
        c = Client()
        response = c.get(f"/api/offer/{task.id}")
        self.assertEqual(response.status_code, 200)
        print(response.content)
