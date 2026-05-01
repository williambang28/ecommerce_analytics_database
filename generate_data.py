import pandas as pd
from faker import Faker
from sqlalchemy import create_engine
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(28)
random.seed(28)

# customers

data = []

europe_countries = ["UK", "France", "Germany", "Spain", "Italy"]
other_countries = ["USA", "Brazil", "India", "Australia", "Japan"]

def generate_country():
    if random.random() < 0.7:
        return random.choice(europe_countries)
    return random.choice(other_countries)

now = datetime(2026, 4, 21)
start_date = now - timedelta(days=10 * 365)

def generate_signup_date():
    ran = random.random()
    if ran < 0.1:
        period_start = start_date
        period_end = start_date + timedelta(days=1 * 365)
    elif ran < 0.3:
        period_start = start_date + timedelta(days=1 * 365)
        period_end = start_date + timedelta(days=2 * 365)
    elif ran < 0.6:
        period_start = start_date + timedelta(days=2 * 365)
        period_end = start_date + timedelta(days=3 * 365)
    else:
        period_start = start_date + timedelta(days=3 * 365)
        period_end = now
        
    delta = period_end - period_start
    random_days = random.randint(0, delta.days)
    
    return period_start + timedelta(days=random_days)


for i in range(1000, 2000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    data.append({
        "customer_id": i,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name}{last_name.lower()}{i}@{fake.free_email_domain()}",
        "country": generate_country(),
        "signup_date": generate_signup_date()
    })

df_customers = pd.DataFrame(data)



# products

data = []

def generate_price():
    ran = random.random()
    if ran < 0.15:
        return round(random.uniform(1, 6), 2)
    elif ran < 0.8:
        return round(random.uniform(7, 45), 2)
    return round(random.uniform(50, 900), 2)

categories = {
    "Arts & Collectables":["Artisan sketch Manikin", "Athena Bust Sculpture", "Sunset Vista Watercolour", "Terra Spiral Clay Vase"],
    "Books, Films & Music":["35mm Camera", "CD Pack", "Mini speaker", "Red Journal"],
    "Clothing & Shoes":["Beige Crewneck Sweater", "Black Low Top Shoes", "Blue Denim Jeans", "Pink Sleeveless Dress"],
    "Electronics & Computing":["Headphones", "Laptop", "Mouse", "SSD"],
    "Health & Beauty":["Facial Cleanser", "Lotion Pump", "Moisturiser", "Styling Comb"],
    "Home, Garden & DIY":["Cordless Power Drill 18v", "Drawer Cabinet", "Garden Watering Can 1.5 Gallon", "Steel Claw Hammer With Rubber Grip"],
    "Pet Supplies":["Dog Food Chicken Blend 10lb", "Dog Food Lamb Blend 10lb", "Plush Bone Chew Toy Coral Orange", "Retractable Dog Leash Teal 16ft", "Stainless Steel Anti Slip Pet Bowl Medium"],
    "Sport & Activity":["Adjustable Dumbells", "Flying Disc", "Snorkel Set", "Tennis Set"],
    "Stationary & Craft Supplies":["Marker Set", "Notebook", "Rainbow Spool Thread Set", "Student Scissors"],
    "Toys & Games":["Beach Buddy Lay Set", "Classic Cuddle Bear", "Magic Star Wand", "Rainbow Logic Cube"]
}

def generate_product():
    category = random.choice(list(categories.keys()))
    product = random.choice(categories[category])
    brand = fake.company()
    
    return {
        "category": category,
        "product_name": f"{brand} {product}"
    }

for i in range(2000, 4000):
    product = generate_product()
    
    data.append({
        "product_id": i,
        "product_name": product["product_name"],
        "category": product["category"],
        "price": generate_price()
    })

df_products = pd.DataFrame(data)



# orders

data = []
    
status = ['Processing','Pending','Failed','Shipped','Delivered','Refunded','Cancelled']
    
def generate_status(order_date):
    if order_date < now - timedelta(days = 31):
        if random.random() < 0.85:
            return 'Delivered'
        return random.choice(status[5:])
    return random.choice(status)

customer_ids = df_customers["customer_id"].tolist()
weights = [random.random() for _ in customer_ids]

for i in range(4000, 15000):
    customer_id = random.choices(customer_ids, weights=weights, k=1)[0]
    customer = df_customers[df_customers["customer_id"] == customer_id].iloc[0]
    
    signup_date = customer["signup_date"]
    order_date = signup_date + timedelta(days=random.randint(0, (now - signup_date).days))
    
    data.append({
        "order_id": i,
        "customer_id": customer_id,
        "order_date": order_date,
        "status": generate_status(order_date)
    })

df_orders = pd.DataFrame(data)



# order_items

data = []

def generate_quantity():
    ran = random.random()
    if ran < 0.7:
        return 1
    elif ran < 0.9:
        return random.randint(2, 3)
    return random.randint(4, 100)
    

order_ids = df_orders["order_id"].tolist()
product_ids = df_products["product_id"].tolist()

for i in range(15000, 26000):
    
    product_id = random.choice(product_ids)
    product = df_products[df_products["product_id"] == product_id].iloc[0]
    
    data.append({
        "order_item": i,
        "order_id": i - 11000,
        "product_id": product_id,
        "quantity": generate_quantity(),
        "price_at_purchase": product["price"]
    })

df_order_items = pd.DataFrame(data)



# payments

data = []

payment_methods = ['Credit Card', 'Debit Card', 'Apple Pay', 'Google Pay', 'PayPal']

def generate_payment_method():
    return random.choice(payment_methods)

for i in range(26000, 37000):
    
    order_id = i - 22000
    order_item = df_order_items[df_order_items["order_id"]==order_id].iloc[0]
    amount = order_item["quantity"] * order_item["price_at_purchase"]
    
    data.append({
        "payment_id": i,
        "order_id": order_id,
        "payment_method": generate_payment_method(),
        "amount": amount
    })

df_payments = pd.DataFrame(data)



# shipping

data = []

def generate_date(date):
    ran = random.random()
    if ran < 0.5:
        return date + timedelta(days=1)
    elif ran < 0.9:
        return date + timedelta(days=random.randint(2,5))
    else:
        return date + timedelta(days=random.randint(7,14))

regions = ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Oceania']

def generate_export_region():
    if random.random() < 0.8:
        return 'Asia'
    return 'Europe'

weights = [0.1, 0.08, 0.1, 0.07, 0.02, 0.5, 0.03]

for i in range(37000, 48000):
    
    order_id = i - 33000
    order = df_orders[df_orders["order_id"]==order_id].iloc[0]

    if order["status"] == 'Delivered':
        ship_date = generate_date(order["order_date"])
        delivery_date = generate_date(ship_date)
    else: 
        continue
    
    if ship_date > now:
        continue
    
    if delivery_date > now:
        delivery_date = None
        
    region_to = random.choices(regions, weights=weights, k=1)[0]

    data.append({
        "shipping_id": i,
        "order_id": order_id,
        "ship_date": ship_date,
        "delivery_date": delivery_date,
        "region_to": region_to,
        "region_from": generate_export_region()
    })

df_shipping = pd.DataFrame(data)



# insert into database

conn_string = 'postgresql://postgres:1234@localhost/ecommerce_database'

db = create_engine(conn_string)
with db.begin() as conn:

    df_customers.to_sql("customers", conn, if_exists='append', index=False)
    df_products.to_sql("products", conn, if_exists='append', index=False)
    df_orders.to_sql("orders", conn, if_exists='append', index=False)
    df_order_items.to_sql("order_items", conn, if_exists='append', index=False)
    df_payments.to_sql("payments", conn, if_exists='append', index=False)
    df_shipping.to_sql("shipping", conn, if_exists='append', index=False)

with db.begin() as conn:
    tables = ["customers", "products", "orders", "order_items", "payments", "shipping"]
    for table in tables:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        print(df.head())