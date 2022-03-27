CREATE DATABASE jennys_db;

CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category VARCHAR(128)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories (category_id) ON DELETE CASCADE
);

CREATE TABLE Customers (
    customer_id INT(10) PRIMARY KEY,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL
);
