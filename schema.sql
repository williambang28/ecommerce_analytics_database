DROP TABLE IF EXISTS shipping;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

DROP TYPE IF EXISTS region;
DROP TYPE IF EXISTS category;
DROP TYPE IF EXISTS status;
DROP TYPE IF EXISTS payment_method;

CREATE TYPE region AS ENUM ('Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Oceania');
CREATE TYPE category AS ENUM ('Arts & Collectables','Books, Films & Music','Clothing & Shoes','Electronics & Computing','Health & Beauty','Home, Garden & DIY','Pet Supplies','Sport & Activity','Stationary & Craft Supplies','Toys & Games');
CREATE TYPE status AS ENUM ('Processing','Pending','Failed','Refunded','Cancelled','Shipped','Delivered');
CREATE TYPE payment_method AS ENUM('Credit Card', 'Debit Card', 'Apple Pay', 'Google Pay', 'PayPal');

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(128),
    last_name VARCHAR(128),
    email VARCHAR(128) UNIQUE,
    country VARCHAR(128),
    signup_date DATE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY NOT NULL,
    product_name VARCHAR(128),
    category CATEGORY, 
    price NUMERIC(8, 2)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY NOT NULL,
    customer_id INT NOT NULL,
    order_date DATE,
    status STATUS,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item SERIAL PRIMARY KEY NOT NULL,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    price_at_purchase NUMERIC(8, 2),

    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id) 
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY NOT NULL,
    order_id INT NOT NULL,
    payment_method PAYMENT_METHOD,
    amount NUMERIC(8,2), -- £

    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE shipping (
    shipping_id SERIAL PRIMARY KEY NOT NULL,
    order_id INT NOT NULL,
    ship_date DATE,
    delivery_date DATE,
    region_to REGION,
    region_from REGION,

    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
