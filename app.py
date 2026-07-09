import streamlit as st
import pandas as pd
from src.database import init_db, seed_initial_data, get_connection
from src.analytics import get_inventory_status, get_low_stock_items, get_sales_summary
from src.ai_engine import generate_ai_insights, draft_supplier_message

# Page Configuration
st.set_page_config(page_title="Kirana Pro | AI Inventory", layout="wide", page_icon="⚡")

# Initialize database components on app run
init_db()
seed_initial_data()

# --- HIGH-END PREMIUM CSS DESIGN ENGINE ---
st.markdown("""
    <style>
    /* Global Background and Canvas Reset */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1e38 100%);
        color: #f8fafc;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Container Styling */
    .main-title {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #94a3b8 !important;
        font-size: 1.1rem !important;
        margin-bottom: 2rem;
    }

    /* Premium Metric Card Grid */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        text-transform: uppercase;
        font-size: 0.78rem !important;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Elegant Modern Glassmorphism Container Wraps */
    div[data-testid="metric-container"] {
        background: rgba(30, 41, 59, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2) !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        backdrop-filter: blur(8px);
    }

    /* Tab Customizations */
    button[data-baseweb="tab"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #94a3b8 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease;
    }
    button[aria-selected="true"] {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.1) !important;
        border-radius: 8px 8px 0px 0px;
    }

    /* High-contrast Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.4) !important;
        transition: transform 0.1s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.5) !important;
    }
    
    /* Clean Interactive Inputs */
    div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #1e293b !important;
        border-radius: 8px !important;
    }
    
    /* Modern Scrollbar customization */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
    </style>
""", unsafe_allow_html=True)

# Top Premium Branding Row
st.markdown('<p class="main-title">⚡ Kirana Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Smart Autonomous Inventory Engine & Analytics Workspace</p>', unsafe_allow_html=True)

# Fetch fresh database parameters
df_inventory = get_inventory_status()
low_stock_items = get_low_stock_items()
sales_history = get_sales_summary()

# --- TOP ROW: GLASS-UI KPI SCORE CARDS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Inventory Size", value=f"{len(df_inventory)} SKUs")

with col2:
    low_stock_count = len(low_stock_items)
    st.metric(
        label="Critical Alerts", 
        value=low_stock_count, 
        delta=f"{low_stock_count} Reorder Items" if low_stock_count > 0 else "Optimal Status",
        delta_color="inverse" if low_stock_count > 0 else "normal"
    )

with col3:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total_amount) FROM sales")
    total_sales = cursor.fetchone()[0] or 0.0
    st.metric(label="Gross Income", value=f"₹{total_sales:,.2f}")

with col4:
    cursor.execute("SELECT COUNT(*) FROM sales")
    sales_count = cursor.fetchone()[0] or 0
    st.metric(label="Total Invoices", value=f"{sales_count} Transactions")
    conn.close()

st.markdown("<br>", unsafe_allow_html=True)

# --- CENTRAL WORKSPACE NAVIGATION TABS ---
tab_dashboard, tab_billing, tab_ai_reorder = st.tabs([
    "📈 Performance Analytics", 
    "🛒 Terminal Billing", 
    "🤖 Autonomous Supply Logic"
])

# ----------------- TAB 1: MODERN PERFORMANCE ANALYTICS -----------------
with tab_dashboard:
    st.markdown("### 📊 Active Stock Registry Matrix")
    search_query = st.text_input("⚡ Filter matrix records instantly by item description or department classification:", "")
    
    if search_query:
        filtered_df = df_inventory[
            df_inventory['name'].str.contains(search_query, case=False, na=False) |
            df_inventory['category'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_df = df_inventory

    st.dataframe(
        filtered_df[['product_id', 'name', 'category', 'current_stock', 'min_stock', 'price', 'supplier_name']], 
        use_container_width=True,
        hide_index=True
    )

# ----------------- TAB 2: TERMINAL BILLING INTERFACE -----------------
with tab_billing:
    col_form, col_log = st.columns([1, 1.2])
    
    with col_form:
        st.markdown("### 💳 Dispatch Customer Checkout")
        product_options = {row['name']: row['product_id'] for _, row in df_inventory.iterrows()}
        
        with st.form("billing_form_entry", clear_on_submit=True):
            selected_product = st.selectbox("SKU Target Reference", list(product_options.keys()))
            quantity_sold = st.number_input("Transactional Batch Size Units", min_value=1, step=1)
            
            submit_sale = st.form_submit_button("Post Transaction Entry")
            
            if submit_sale:
                prod_id = product_options[selected_product]
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT current_stock, price FROM products WHERE product_id = ?", (prod_id,))
                current_stock, price = cursor.fetchone()
                
                if quantity_sold > current_stock:
                    st.error(f"Execution Aborted: Insufficient product density. Only {current_stock} available.")
                else:
                    new_stock = current_stock - quantity_sold
                    cursor.execute("UPDATE products SET current_stock = ? WHERE product_id = ?", (new_stock, prod_id))
                    
                    total_cost = price * quantity_sold
                    cursor.execute("INSERT INTO sales (product_id, quantity, total_amount) VALUES (?, ?, ?)", (prod_id, quantity_sold, total_cost))
                    conn.commit()
                    
                    st.success(f"Finalized Receipt: ₹{total_cost:,.2f} posted.")
                    st.rerun()
                conn.close()

    with col_log:
        st.markdown("### 📄 Terminal Audit Feed")
        if not sales_history.empty:
            st.dataframe(sales_history.tail(6), use_container_width=True, hide_index=True)
        else:
            st.caption("Active pipeline clear. No historical metrics found today.")

# ----------------- TAB 3: AUTONOMOUS SUPPLY CHAIN LOGIC -----------------
with tab_ai_reorder:
    if low_stock_items.empty:
        st.success("Logistics Optimized. All systems executing smoothly within acceptable threshold metrics.")
    else:
        col_ai_left, col_ai_right = st.columns([1, 1])
        
        with col_ai_left:
            st.markdown("### ⚠️ Active Supply Breaches")
            st.dataframe(
                low_stock_items[['name', 'current_stock', 'min_stock', 'supplier_name']], 
                use_container_width=True, 
                hide_index=True
            )
            
            st.markdown("---")
            st.markdown("### ✉️ AI B2B Dispatch Draft Generator")
            selected_item = st.selectbox("Select Target Supplier Route:", low_stock_items['name'].unique())
            
            if selected_item:
                row_data = low_stock_items[low_stock_items['name'] == selected_item].iloc[0]
                if st.button("Generate Vendor Message Draft", type="primary"):
                    with st.spinner("Drafting layout parameters..."):
                        message_draft = draft_supplier_message(
                            row_data['supplier_name'], 
                            row_data['name'], 
                            int(row_data['current_stock']), 
                            int(row_data['min_stock'])
                        )
                        st.text_area("Ready-to-Send Template:", value=message_draft, height=180)
        
        with col_ai_right:
            st.markdown("### 💡 AI Intelligence Reports")
            st.markdown("Click below to process sales acceleration matrices using deep predictive models.")
            
            if st.button("Execute Predictive Stock Diagnostics"):
                with st.spinner("Compiling structural telemetry matrices..."):
                    sales_csv_str = sales_history.to_csv(index=False)
                    low_stock_csv_str = low_stock_items.to_csv(index=False)
                    
                    ai_insights_output = generate_ai_insights(sales_csv_str, low_stock_csv_str)
                    st.info(ai_insights_output)