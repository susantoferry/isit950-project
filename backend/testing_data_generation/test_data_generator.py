import random
import string
import datetime
import mysql.connector
from faker import faker

# Connect to the MySQL database
conn = mysql.connector.connect(
    host='awsdbisit950.cmoar4du3hp3.ap-southeast-2.rds.amazonaws.com',
    user='admin',
    password='password',
    database='test_isit950'
)
cursor = conn.cursor()

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
    location = generate_random_string(20)
    longitude = random.uniform(-180, 180)
    latitude = random.uniform(-90, 90)
    is_paid = random.choice([True, False])
    completed_on_date = datetime.datetime.now() if random.choice([True, False]) else None
    create_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
    status = random.choice(['pending', 'in_progress', 'completed'])
    category_id = random.randint(1, 10)
    user_id = random.randint(1, 100)
    user_provider_id = random.randint(1, 100)
    location_link = 'https://example.com'
    modify_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 10))
    offer = random.uniform(0, 10)
    provider_review = random.randint(1, 5)
    user_review = random.randint(1, 5)

    # Insert the generated data into the database
    query = "INSERT INTO your_table (task_title, description, price, booking_price, total_price, location, longitude, latitude, is_paid, completed_on_date, create_date, status, category_id, user_id, user_provider_id, location_link, modify_date, offer, provider_review, user_review) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (task_title, description, price, booking_price, total_price, location, longitude, latitude, is_paid, completed_on_date, create_date, status, category_id, user_id, user_provider_id, location_link, modify_date, offer, provider_review, user_review)
    cursor.execute(query, values)

# Commit the changes and close the connection
conn.commit()
conn.close()