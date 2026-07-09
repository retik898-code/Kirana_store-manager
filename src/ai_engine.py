import google.generativeai as genai
import os

# Configure the API key using environment variables for security
API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_ai_insights(sales_data_csv, low_stock_csv):
    """Generates analytical insights regarding movement speed and inventory optimization."""
    if not API_KEY:
        return "⚠️ Please set your GEMINI_API_KEY environment variable to see smart AI analytics insights."
        
    prompt = f"""
    You are an expert Kirana Store retail consultant optimizer. Analyze the data below:
    
    RECENT SALES HISTORIC TRENDS:
    {sales_data_csv}
    
    CRITICAL LOW STOCK ITEMS:
    {low_stock_csv}
    
    Provide a concise, 3-bullet point summary identifying:
    1. Which products are moving fastest.
    2. Any clear urgent restock prioritization recommendations based strictly on data trends.
    Keep the tone simple and direct for a local shop owner.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error connecting to AI module: {str(e)}"

def draft_supplier_message(supplier_name, product_name, current_stock, min_stock):
    """Drafts a structured restock message intended for immediate business messaging."""
    if not API_KEY:
        return "AI Draft Unavailable: API Key missing."

    prompt = f"""
    Draft a polite, highly concise business WhatsApp/SMS restock order message to the distributor '{supplier_name}'.
    The item '{product_name}' has dropped below critical levels (Current Stock: {current_stock}, Threshold Limit: {min_stock}).
    Ask them to deliver an optimal baseline batch standard sizing order as early as possible. 
    Include placeholders like [Insert Quantity] clearly. No extra fluff.
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error drafting message: {str(e)}"