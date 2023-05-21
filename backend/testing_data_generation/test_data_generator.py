import random
import string
import datetime
import mysql.connector
from faker import Faker

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='awsdbisit950.cmoar4du3hp3.ap-southeast-2.rds.amazonaws.com',
    user='admin',
    password='password',
    database='CI_test_isit950'
)
cursor = conn.cursor()

#Utilise faker
fakeAU = Faker('en_AU')
fakeEN = Faker('en')

# Function to generate a random string
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Generate testing data
num_rows = 100  # Number of rows to generate

for _ in range(num_rows):
    task_title = "test_" + generate_random_string(8)
    description = "test_" + generate_random_string(50)
    price = round(random.uniform(30, 170),-1)
    booking_price = price/10
    total_price = price + booking_price
    location = fakeAU.city()
    longitude = random.uniform(-180, 180)
    latitude = random.uniform(-90, 90)
    is_paid = random.choice([True, False])
    completed_on_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(7, 30))
    create_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    status = 0
    category_id = random.randint(1, 12)
    user_id = random.randint(1, 30)
    user_provider_id = random.randint(1, 30)
    location_link = 'https://example.com'
    modify_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 10))
    offer = 0
    # provider_review = 0
    # user_review = 0

    # Insert the generated data into the database
    query = "insert into backend_task (task_title, description, price, booking_price, total_price, location, location_link, lat, longitude, completed_on, status, is_paid, create_date, modify_date, offer, category_id, user_id, user_provider_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    values = (task_title, description, price, booking_price, total_price, location, location_link, longitude, latitude, completed_on_date, status, is_paid, create_date, modify_date, offer, category_id, user_id, user_provider_id)
    cursor.execute(query, values)

# Commit the changes and close the connection
conn.commit()
conn.close()