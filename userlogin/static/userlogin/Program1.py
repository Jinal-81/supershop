import psycopg2

my_conn = psycopg2.connect(
    database='task1_database',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
)

my_conn.autocommit = True
cursor = my_conn.cursor()

# query = "CREATE DATABASE car_db"
# cursor.execute(query)
# print("successfully")

my_db_conn = psycopg2.connect(
    database='car_db',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
)

create_table_query = """
CREATE TABLE IF NOT EXISTS cars (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
model INTEGER,
number TEXT,
color TEXT,
company TEXT
);
"""

my_db_conn.autocommit = True
cursor = my_db_conn.cursor()
cursor.execute(create_table_query)
print("Table Created successfully")

cars = [
    ("Aqua", 2009, "ABC123", "Red", "Toyota"),
    ("700s", 2015, "XXXX22", "Black", "BMW"),
    ("Vezel", 2018, "XXX111", "White", "Honda"),
    ("200C", 2001, "MMMM11", "Black", "Mercedez"),
    ("Vitz", 2010, "XXXX", "Red", "Toyota"),
]

car_records = ", ".join(["%s"] * len(cars))

insert_query = (
    f"INSERT INTO cars (name, model, number, color, company) VALUES {car_records}"
)

cursor.execute(insert_query, cars)
print("Data inserted Successfully")

select_cars_query = "SELECT * FROM cars"
cursor.execute(select_cars_query)

cars = cursor.fetchall()

for car in cars:
    print(car)

update_car_colors = """
UPDATE
cars
SET
color = 'Blue'
WHERE
model >= 2010
"""

cursor.execute(update_car_colors)
print("Updated Successfully")

cursor.execute(select_cars_query)

cars = cursor.fetchall()

for car in cars:
    print(car)

delete_car_records = "DELETE FROM cars WHERE color = 'Red'"

cursor.execute(delete_car_records)
print("Deleted Successfully")

cursor.execute(select_cars_query)

cars = cursor.fetchall()

for car in cars:
    print(car)
