CREATE DATABASE cloud;

\c cloud;

-- Create the User table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create the Product table
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    image VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    category VARCHAR(255) NOT NULL
);

-- Create the Cart table
CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    category VARCHAR(255) NOT NULL,
    image VARCHAR(255),
    CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
      REFERENCES "user"(id),
    CONSTRAINT fk_product
      FOREIGN KEY(product_id) 
      REFERENCES product(id)
);

-- Insert initial data into the Product table
INSERT INTO product (id, name, description, price, quantity, image, is_active, category)
VALUES 
(1, 'Red Printed T-Shirt', 'Red elegant t-shirt', 50.00, 10, 'product-1.jpg', TRUE, 'T-shirt'),
(2, 'Black Sneakers', 'Black sporty sneakers', 50.00, 10, 'product-2.jpg', TRUE, 'Sneakers'),
(3, 'Grey Pants', 'Grey sporty pants', 50.00, 10, 'product-3.jpg', TRUE, 'Pants'),
(4, 'Navy Puma T-Shirt', 'Puma elegant t-shirt', 50.00, 10, 'product-4.jpg', TRUE, 'T-shirt'),
(5, 'Black Puma T-Shirt', 'Puma elegant t-shirt', 50.00, 10, 'product-5.jpg', TRUE, 'T-shirt'),
(6, '3x Printed Socks', 'Printed Socks', 50.00, 10, 'product-6.jpg', TRUE, 'Socks'),
(7, 'FOSSIL Black Watch', 'Black FOSSIL Watch', 50.00, 10, 'product-7.jpg', TRUE, 'Watches');


