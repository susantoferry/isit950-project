import random
import string
import datetime
import mysql.connector
from faker import Faker


#region auto-generate test-data
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

#region TASK TABLE Test-data
# Function to generate a random string
# def generate_random_string(length):
#     letters = string.ascii_letters
#     return ''.join(random.choice(letters) for i in range(length))

# # Generate testing data
# num_rows = 100  # Number of rows to generate

# for _ in range(num_rows):
#     task_title = "test_" + generate_random_string(8)
#     description = "test_" + fakeEN.paragraph(nb_sentences=2)
#     price = round(random.uniform(30, 170),-1)
#     booking_price = price/10
#     total_price = price + booking_price
#     location = fakeAU.city()
#     longitude = random.uniform(-180, 180)
#     latitude = random.uniform(-90, 90)
#     is_paid = random.choice([True, False])
#     completed_on_date = datetime.datetime.now() + datetime.timedelta(days=random.randint(7, 30))
#     create_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
#     status = 0
#     category_id = random.randint(1, 12)
#     user_id = random.randint(1, 30)
#     user_provider_id = random.randint(1, 30)
#     location_link = 'https://example.com'
#     modify_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 10))
#     offer = 0
#     # provider_review = 0
#     # user_review = 0

#     # Insert the generated data into the database
#     query = "insert into backend_task (task_title, description, price, booking_price, total_price, location, location_link, lat, longitude, completed_on, status, is_paid, create_date, modify_date, offer, category_id, user_id, user_provider_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
#     values = (task_title, description, price, booking_price, total_price, location, location_link, longitude, latitude, completed_on_date, status, is_paid, create_date, modify_date, offer, category_id, user_id, user_provider_id)
#     cursor.execute(query, values)

# # Commit the changes and close the connection
# conn.commit()

#endregion


#region USER TABLE Test-data

# Generate testing data
num_rows = 25  # Number of rows to generate

for _ in range(num_rows):
    password = "pbkdf2_sha256$600000$XUZF4n7dtIXe1QmY2axOem$pqZYJgDB2N34MmJW4nGJR2zb9ctKo4VcnGmG9rPE7V4="
    last_login = datetime.datetime.now()
    is_superuser = 0
    first_name = fakeEN.first_name()
    last_name = fakeEN.last_name()
    username = "test_" + str(random.randint(1,99)) + first_name + last_name
    email = username +"@gmail.com"
    is_staff = 0
    is_active = 1
    date_joined = datetime.datetime.now() - datetime.timedelta(days=random.randint(14, 30))
    address = fakeAU.street_address()
    description = fakeEN.paragraph(nb_sentences=3)
    unit = fakeAU.secondary_address() 
    city = 0
    state = fakeAU.state_abbr()
    zip = fakeAU.postcode()
    rating = random.randint(1, 5)
    email_verified = 1


    # Insert the generated data into the database
    query = "insert into backend_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, address, description, unit, city, state, zip, rating, email_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    values = (password, last_login, is_superuser, first_name, last_name, username, email, is_staff, is_active, date_joined, address, description, unit, city, state, zip, rating, email_verified)
    cursor.execute(query, values)

# Commit the changes and close the connection
conn.commit()

#endregion

#region MEMBERSHIP TRANSACTION TABLE Test-data

# Generate testing data
num_rows = 25  # Number of rows to generate

for _ in range(num_rows):
    password = "pbkdf2_sha256$600000$XUZF4n7dtIXe1QmY2axOem$pqZYJgDB2N34MmJW4nGJR2zb9ctKo4VcnGmG9rPE7V4="
    last_login = datetime.datetime.now()
    is_superuser = 0
    first_name = fakeEN.first_name()
    last_name = fakeEN.last_name()
    username = "test_" + str(random.randint(1,99)) + first_name + last_name
    email = username +"@gmail.com"
    is_staff = 0
    is_active = 1
    date_joined = datetime.datetime.now() - datetime.timedelta(days=random.randint(14, 30))
    address = fakeAU.street_address()
    description = fakeEN.paragraph(nb_sentences=3)
    unit = fakeAU.secondary_address() 
    city = 0
    state = fakeAU.state_abbr()
    zip = fakeAU.postcode()
    rating = random.randint(1, 5)
    email_verified = 1


    # Insert the generated data into the database
    query = "insert into backend_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, address, description, unit, city, state, zip, rating, email_verified) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    values = (password, last_login, is_superuser, first_name, last_name, username, email, is_staff, is_active, date_joined, address, description, unit, city, state, zip, rating, email_verified)
    cursor.execute(query, values)

# Commit the changes and close the connection
conn.commit()

#endregion

conn.close()
#endregion
