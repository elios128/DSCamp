import re
import pandas as pd

def clean_customers(customers: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with: invalid/duplicate emails, duplicate/missing id's, invalid date format and lowercases emails"""

    customers["created_at"] = pd.to_datetime(customers["created_at"],
                                             format='%Y-%m-%d %H:%M:%S',
                                             errors="coerce")
    customers["email"] = customers["email"].str.lower()

    customers = customers[
        customers["customer_id"].notna() &
        (customers['customer_id'] >= 0) &
        customers["email"].notna() &
        ~customers["customer_id"].duplicated() &
        ~customers["email"].duplicated() &
        customers["email"].apply(_is_valid_email) &
        customers["created_at"].notna()
    ]
    customers["customer_id"] = customers["customer_id"].astype(int)
    return customers


def clean_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with invalid or non-existant date, customer id or duplicated/invalid order id, and lowercases order status"""
    orders["order_status"] = orders["order_status"].str.lower()
    orders["created_at"] = pd.to_datetime(orders["created_at"],
                                             format='%Y-%m-%d %H:%M:%S',
                                             errors="coerce")
    orders = orders[
        ~orders["order_id"].duplicated() &
        orders["order_id"].notna() &
        (orders["order_id"] >= 0) &
        orders["customer_id"].isin(customers["customer_id"]) &
        orders["created_at"].notna()
        ]
    orders["customer_id"] = orders["customer_id"].astype(int)
    return orders

def clean_products(products: pd.DataFrame) -> pd.DataFrame:
    """Drops rows with invalid/duplicated product ids, name, without category, or invalid price"""
    products["name"] = products["name"].str.lower()
    products = products[
        ~products["product_id"].isna() &
        (products["product_id"] >= 0) &
        ~products["product_id"].duplicated() &
        ~products["name"].isna() &
        ~products["name"].duplicated() &
        (products["price"] >= 0.01) &
        ~products["category"].isna()
    ]
    return products

def clean_order_items(order_items: pd.DataFrame, orders: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with invalid/duplicated order/product/order_item id's or invalid quantity"""
    order_items = order_items[
        order_items["order_id"].isin(orders["order_id"]) &
        order_items["product_id"].isin(products["product_id"]) &
        (order_items["order_item_id"] >= 0) &
        ~order_items["order_item_id"].duplicated() &
        (order_items["quantity"] >= 1) 
    ]
    return order_items

def _is_valid_email(email):
    """Checks for valid pattern "abc123@abc123.abc" """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, str(email)) is not None