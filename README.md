Introduction
The Customer Order Management System is a Python-based application designed to manage customer data, product information, and order processing. This system utilizes SQLite for persistent data storage and pandas for data manipulation and analysis, ensuring efficient and organized management of all operations.

Features
Add new customers to the system.
Update customer details including name and contact information.
Delete customers from the system.
Add new products to the inventory.
Update product details including price and quantity.
Delete products from the inventory.
Place orders for customers with detailed product information.
Update order details.
Delete orders.
Generate detailed order reports.
Interactive user menu for easy navigation and operation.
Technologies Used
Python: Core programming language.
SQLite: Database for persistent storage.
pandas: Data manipulation and analysis.
datetime: For handling dates and times.
Classes and Methods
DatabaseConnection
Manages the database connection and provides methods to execute queries and fetch data.

connect(): Establishes a connection to the database.
disconnect(): Closes the database connection.
execute_query(query, params=()): Executes a query with optional parameters.
fetch_data(query, params=()): Fetches data from the database.
TableManager
Handles the creation of database tables.

create_tables(db_conn): Creates the necessary tables (customers, products, orders, order_details).
Customer
Manages customer-related operations.

add_customer(db_conn, customer_id, name, contact_info): Adds a new customer.
update_customer(db_conn, customer_id, updated_name, updated_contact_info): Updates customer details.
delete_customer(db_conn, customer_id): Deletes a customer.
get_all_customers(db_conn): Retrieves all customers.
Product
Manages product-related operations.

add_product(db_conn, product_id, name, price, quantity): Adds a new product.
update_product(db_conn, product_id, updated_price, updated_quantity): Updates product details.
delete_product(db_conn, product_id): Deletes a product.
get_all_products(db_conn): Retrieves all products.
Order
Manages order-related operations.

add_order(db_conn, order_id, customer_id, details): Places a new order.
update_order(db_conn, order_id, updated_order_details): Updates order details.
delete_order(db_conn, order_id): Deletes an order.
generate_report(db_conn, csv_file_path='orders_report.csv'): Generates a detailed order report and saves it as a CSV file.
Menu Options
Add Customer: Adds a new customer to the system.
Update Customer: Updates existing customer details.
Delete Customer: Deletes a customer from the system.
View All Customers: Displays all customers.
Add Product: Adds a new product to the inventory.
Update Product: Updates existing product details.
Delete Product: Deletes a product from the inventory.
View All Products: Displays all products.
Add Order: Places a new order.
Update Order: Updates existing order details.
Delete Order: Deletes an order from the system.
View All Orders: Displays all orders.
Generate Report: Generates a detailed order report.
Exit: Exits the application.
Generating Reports
To generate a report of all orders:

Select the "Generate Report" option from the menu.
The report will be saved as orders_report.csv in the current directory.
