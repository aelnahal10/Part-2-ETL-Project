
-- 1. Customers
CREATE TABLE stg_customers (
    customer_id INT,
    first_name NVARCHAR(100),
    last_name NVARCHAR(100),
    email NVARCHAR(200),
    phone NVARCHAR(50),
    street NVARCHAR(200),
    city NVARCHAR(100),
    state NVARCHAR(100),
    zip_code NVARCHAR(20)
);
 

-- 2. Products
CREATE TABLE stg_products (
    product_id INT,
    product_name NVARCHAR(200),
    brand_id INT,
    category_id INT,              
    model_year INT,
    list_price DECIMAL(10,2)
);

 

-- 3. Brands
CREATE TABLE stg_brands (
    brand_id INT,
    brand_name NVARCHAR(100)
);
 

-- 4. Cate ries
CREATE TABLE stg_categories ( 
    category_id INT,
    category_name NVARCHAR(100)
);
 

-- 5. Orders
CREATE TABLE stg_orders (
    order_id INT,
    customer_id INT,
    order_status INT,
    order_date DATE,
    required_date DATE,
    shipped_date DATE,
    store_id INT,
    staff_id INT
);
 

-- 6. Order Items
CREATE TABLE stg_order_items (
    order_id INT,
    item_id INT,
    product_id INT,
    quantity INT,
    list_price DECIMAL(10,2),
    discount DECIMAL(5,2)
);
 

-- 7. Staff
CREATE TABLE stg_staffs (
    staff_id INT,
    first_name NVARCHAR(100),
    last_name NVARCHAR(100),
    email NVARCHAR(200),
    phone NVARCHAR(50),
    active BIT,
    store_id INT,
    manager_id INT
);
 

-- 8. Stores
CREATE TABLE stg_stores (
    store_id INT,
    store_name NVARCHAR(200),
    phone NVARCHAR(50),
    email NVARCHAR(200),
    street NVARCHAR(200),
    city NVARCHAR(100),
    state NVARCHAR(100),
    zip_code NVARCHAR(20)
);
 
