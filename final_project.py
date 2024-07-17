import pandas as pd
import sqlite3
from datetime import datetime

class DatabaseConnection:

    def __init__(self, db_name='customer_order_management.db'):
        self.db_name = db_name
        self.conn = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
    
    def execute_query(self, query, params=()):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query, params)
            self.conn.commit()
    
    def fetch_data(self, query, params=()):
        with self.conn:
            cur = self.conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()

class TableManager:
    @staticmethod
    def create_tables(db_conn):
        create_customers_table_query = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_info TEXT NOT NULL
        )
        """
        db_conn.execute_query(create_customers_table_query)

        create_products_table_query = """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        """
        db_conn.execute_query(create_products_table_query)

        create_orders_table_query = """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        """
        db_conn.execute_query(create_orders_table_query)

        create_order_details_table_query = """
        CREATE TABLE IF NOT EXISTS order_details (
            order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
        """
        db_conn.execute_query(create_order_details_table_query)

class Customer:

    def __init__(self, customer_id, name, contact_info):
        self.customer_id = customer_id
        self.name = name
        self.contact_info = contact_info

    @staticmethod
    def add_customer(db_conn, name, contact_info):
         query = "INSERT INTO customers (name, contact_info) VALUES (?, ?)"
         db_conn.execute_query(query, (name, contact_info))

    @staticmethod
    def update_customer(db_conn, customer_id, updated_name, updated_contact_info):
        query = "UPDATE customers SET name = ?, contact_info = ? WHERE customer_id = ?"
        db_conn.execute_query(query, (updated_name, updated_contact_info, customer_id))

    @staticmethod
    def delete_customer(db_conn, customer_id):
        query = "DELETE FROM customers WHERE customer_id = ?"
        db_conn.execute_query(query, (customer_id,))

    @staticmethod
    def get_all_customers(db_conn):
        query = "SELECT * FROM customers"
        return db_conn.fetch_data(query)   
    
class Product:

    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    @staticmethod
    def add_product(db_conn, name, price, quantity):
        query="INSERT INTO products (name, price, quantity) VALUES(?, ?, ?)"
        db_conn.execute_query(query, (name, price, quantity))

    @staticmethod
    def update_product(db_conn, product_id, updated_price, updated_quantity):
        query="UPDATE products SET price = ?, quantity = ? WHERE product_id = ?"
        db_conn.execute_query(query, (updated_price, updated_quantity, product_id))

    @staticmethod
    def delete_product(db_conn, product_id):
        query="DELETE FROM products WHERE product_id = ?"
        db_conn.execute_query(query, (product_id,))

    @staticmethod
    def get_all_products(db_conn):
        query="SELECT * FROM products"
        return db_conn.fetch_data(query)

class Order:
    def __init__(self, order_id, customer_id, date, details):
        self.order_id = order_id
        self.customer_id = customer_id
        self.date = date
        self.details = details
    
    @staticmethod
    def add_order(db_conn, customer_id, details):
        date = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")
        query = "INSERT INTO orders (customer_id, date) VALUES(?, ?)"
        db_conn.execute_query(query, (customer_id, date))
        order_id = db_conn.fetch_data("SELECT last_insert_rowid()")[0][0]
        for product_id, quantity in details:
            query = "INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)"
            db_conn.execute_query(query, (order_id, product_id, quantity))

    @staticmethod
    def update_order(db_conn, order_id, updated_order_details):
        date = datetime.now().strftime("%d/%m/%Y,%H:%M:%S")
        query = "UPDATE orders SET date = ? WHERE order_id = ?"
        db_conn.execute_query(query, (date, order_id))
        query = "DELETE FROM order_details WHERE order_id = ?"
        db_conn.execute_query(query, (order_id,))
        for product_id, quantity in updated_order_details:
            query = "INSERT INTO order_details (order_id, product_id, quantity) VALUES (?, ?, ?)"
            db_conn.execute_query(query, (order_id, product_id, quantity))

    @staticmethod
    def delete_order(db_conn, order_id):
        query = "DELETE FROM order_details WHERE order_id = ?"
        db_conn.execute_query(query, (order_id,))
        query = "DELETE FROM orders WHERE order_id = ?"
        db_conn.execute_query(query, (order_id,))

    @staticmethod
    def get_all_orders(db_conn):
        query = """
        SELECT o.order_id, o.customer_id, o.date, od.product_id, od.quantity
        FROM orders o
        LEFT JOIN order_details od ON o.order_id = od.order_id
        """
        return db_conn.fetch_data(query)

    @staticmethod
    def generate_report(db_conn, csv_file_path='orders_report.csv'):
        query = """
        SELECT o.order_id, o.customer_id, c.name as customer_name, o.date, 
               od.product_id, p.name as product_name, od.quantity, p.price,
               (od.quantity * p.price) as total_price
        FROM orders o
        LEFT JOIN order_details od ON o.order_id = od.order_id
        LEFT JOIN customers c ON o.customer_id = c.customer_id
        LEFT JOIN products p ON od.product_id = p.product_id
        """
        orders_data = db_conn.fetch_data(query)
        
        # Define column names
        columns = ['order_id', 'customer_id', 'customer_name', 'date', 
                   'product_id', 'product_name', 'quantity', 'price', 'total_price']
        
        # Create a DataFrame
        df = pd.DataFrame(orders_data, columns=columns)
        
        # Save to CSV
        df.to_csv(csv_file_path, index=False)
        print(f"Report generated and saved to {csv_file_path}")

def display_menu():
    print("""
  ____          _                                             
 / __ \        | |                                            
| |  | |_ __ __| | ___ _ __                                   
| |  | | '__/ _` |/ _ \ '__|                                  
| |__| | | | (_| |  __/ |                                     
 \____/|_|  \__,_|\___|_|                                 _   
|  \/  |                                                 | |  
| \  / | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
| |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
 / ____|         | |       __/ |                              
| (___  _   _ ___| |_ ___ |___/___                            
 \___ \| | | / __| __/ _ \ '_ ` _ \                           
 ____) | |_| \__ \ ||  __/ | | | | |                          
|_____/ \__, |___/\__\___|_| |_| |_|                          
         __/ |                                                
        |___/                                                               
      
           """)
    print("1. Add Customer")
    print("2. Update Customer")
    print("3. Delete Customer")
    print("4. View All Customers")
    print("5. Add Product")
    print("6. Update Product")
    print("7. Delete Product")
    print("8. View All Products")
    print("9. Add Order")
    print("10. Update Order")
    print("11. Delete Order")
    print("12. View All Orders")
    print("13. Generate Report")
    print("14. Exit")

def main():
    db_conn = DatabaseConnection()
    db_conn.connect()
    TableManager.create_tables(db_conn)

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter customer name: ")
            contact_info = input("Enter customer contact info: ")
            Customer.add_customer(db_conn, name, contact_info)

        elif choice == '2':
            customer_id = int(input("Enter customer ID: "))
            updated_name = input("Enter updated name: ")
            updated_contact_info = input("Enter updated contact info: ")
            Customer.update_customer(db_conn, customer_id, updated_name, updated_contact_info)

        elif choice == '3':
            customer_id = int(input("Enter customer ID to delete: "))
            Customer.delete_customer(db_conn, customer_id)

        elif choice == '4':
            customers = Customer.get_all_customers(db_conn)
            for customer in customers:
                print(customer)

        elif choice == '5':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            Product.add_product(db_conn, name, price, quantity)

        elif choice == '6':
            product_id = int(input("Enter product ID: "))
            updated_price = float(input("Enter updated price: "))
            updated_quantity = int(input("Enter updated quantity: "))
            Product.update_product(db_conn, product_id, updated_price, updated_quantity)

        elif choice == '7':
            product_id = int(input("Enter product ID to delete: "))
            Product.delete_product(db_conn, product_id)

        elif choice == '8':
            products = Product.get_all_products(db_conn)
            for product in products:
                print(product)

        elif choice == '9':
            customer_id = int(input("Enter customer ID: "))
            details = []
            while True:
                product_id = int(input("Enter product ID (or 0 to finish): "))
                if product_id == 0:
                    break
                quantity = int(input("Enter quantity: "))
                details.append((product_id, quantity))
            Order.add_order(db_conn, customer_id, details)

        elif choice == '10':
            order_id = int(input("Enter order ID: "))
            details = []
            while True:
                product_id = int(input("Enter product ID (or 0 to finish): "))
                if product_id == 0:
                    break
                quantity = int(input("Enter quantity: "))
                details.append((product_id, quantity))
            Order.update_order(db_conn, order_id, details)

        elif choice == '11':
            order_id = int(input("Enter order ID to delete: "))
            Order.delete_order(db_conn, order_id)

        elif choice == '12':
            orders = Order.get_all_orders(db_conn)
            for order in orders:
                print(order)

        elif choice == '13':
            Order.generate_report(db_conn)

        elif choice == '14':
            db_conn.disconnect()
            break

        else:
            print("Invalid choice. Please try again.")
main()
