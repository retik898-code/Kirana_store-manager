import pandas as pd
from src.database import get_connection

def get_inventory_status():
    conn = get_connection()
    query = """
        SELECT p.product_id, p.name, p.category, p.current_stock, p.min_stock, p.price, s.name as supplier_name 
        FROM products p
        LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_low_stock_items():
    df = get_inventory_status()
    # Logic check: Item is low stock if current stock hits or goes below minimum safety threshold
    low_stock_df = df[df['current_stock'] <= df['min_stock']]
    return low_stock_df

def get_sales_summary():
    conn = get_connection()
    query = """
        SELECT s.sale_id, p.name, p.category, s.quantity, s.sale_date, s.total_amount 
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df