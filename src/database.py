import sqlite3
import os

DB_PATH = "kirana_inventory.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Products Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            current_stock INTEGER NOT NULL,
            min_stock INTEGER NOT NULL,
            price REAL NOT NULL,
            supplier_id INTEGER,
            FOREIGN KEY(supplier_id) REFERENCES suppliers(supplier_id)
        )
    ''')
    
    # 2. Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            sale_date DATE DEFAULT CURRENT_DATE,
            total_amount REAL,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    ''')
    
    # 3. Suppliers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_initial_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    if cursor.fetchone()[0] == 0:
        # Seed Suppliers
        suppliers = [
            ('Sharma Wholesale', 'Rahul Sharma', '9876543210', 'sharma@wholesale.com'),
            ('Verma General Distributors', 'Amit Verma', '9123456789', 'verma@dist.com')
        ]
        cursor.executemany("INSERT INTO suppliers (name, contact_person, phone, email) VALUES (?, ?, ?, ?)", suppliers)
        
        # Seed Products
        products = [
            ('Aashirvaad Atta 5kg', 'Groceries', 12, 15, 290.0, 1),
            ('Amul Butter 500g', 'Dairy', 5, 10, 275.0, 2),
            ('Tata Salt 1kg', 'Groceries', 45, 20, 28.0, 1),
            ('Surf Excel Easy Wash 1kg', 'Household', 8, 12, 140.0, 2),
            ('Maggi Noodles 12-Pack', 'Packaged Foods', 25, 15, 168.0, 1)
        ]
        cursor.executemany("INSERT INTO products (name, category, current_stock, min_stock, price, supplier_id) VALUES (?, ?, ?, ?, ?, ?)", products)
        
        # Seed Mock Sales (Recent trends)
        sales = [
            (1, 5, '2026-07-01', 1450.0),
            (2, 8, '2026-07-02', 2200.0),
            (1, 4, '2026-07-03', 1160.0),
            (5, 10, '2026-07-04', 1680.0),
            (2, 4, '2026-07-05', 1100.0)
        ]
        cursor.executemany("INSERT INTO sales (product_id, quantity, sale_date, total_amount) VALUES (?, ?, ?, ?)", sales)
        
        conn.commit()
    conn.close()