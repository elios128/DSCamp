from sqlalchemy import create_engine
from utils import clean_customers, clean_order_items, clean_orders, clean_products
import pandas as pd
import os


def main():
    #read data
    data_dir = "/data/raw"
    customers = pd.read_csv(os.path.join(data_dir, "customers.csv"))
    order_items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))
    orders = pd.read_csv(os.path.join(data_dir, "orders.csv"))
    products = pd.read_csv(os.path.join(data_dir, "products.csv"))

    #clean data
    customers = clean_customers(customers)
    orders = clean_orders(orders, customers)
    products = clean_products(products)
    order_items = clean_order_items(order_items, orders, products)

    #create analytical table
    super_df = order_items.merge(right=orders,
                             how="inner",
                             on="order_id")
    super_df = super_df.merge(right=products,
                             how="inner",
                             on="product_id")
    super_df = super_df.merge(right=customers,
                             how="inner",
                             on="customer_id")
    
    #connect to the local db
    engine = create_engine(
    'postgresql+psycopg2://postgres:admin@db/db'  #we should keep that info in .env in production
)
    
    #load clean data into db
    super_df.to_sql(
    "analytical_table",
    engine,
    if_exists="replace",
    index=False
)   
    
    #get data from the db
    querry = "SELECT * FROM analytical_table"
    loaded = pd.read_sql(querry, engine)
    print(loaded)
    


if __name__ == "__main__":
    main()