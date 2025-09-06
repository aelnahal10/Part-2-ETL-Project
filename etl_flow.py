import pandas as pd
from config import get_engine
from sqlalchemy import text
from prefect import flow, task, get_run_logger
from tasks.scd_type1 import update_dim_store, update_dim_product
from tasks.scd_type2 import update_dim_customer, update_dim_staff

# -------------------------
# Task: Run SQL file (schema or staging)
# -------------------------
@task
def run_sql_script(file_path: str):
    logger = get_run_logger()
    logger.info(f"⚙️ Running SQL script: {file_path}")
    engine = get_engine()

    try:
        with engine.begin() as conn:
            with open(file_path, 'r') as file:
                sql = file.read()
            conn.execute(text(sql))
        logger.info(f"✅ Executed: {file_path}")
    except Exception as e:
        logger.error(f"❌ Failed to execute {file_path}: {e}")
        raise

# -------------------------
# Task: Load CSV into staging table
# -------------------------
@task
def load_csv_to_staging(table_name: str, csv_path: str):
    logger = get_run_logger()
    logger.info(f"📥 Loading: {csv_path} into {table_name}")

    try:
        df = pd.read_csv(csv_path)
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name}"))  # CDC: Delete last 30 days of data from the target, and then insert the newest 30 days of data from the source.
            df.to_sql(table_name, con=conn, if_exists="append", index=False)
        logger.info(f"✅ Loaded {len(df)} records into {table_name}")
    except Exception as e:
        logger.error(f"❌ Error loading {csv_path} → {table_name}: {e}")
        raise


# -------------------------
# Flow: Load all staging data
# -------------------------
@flow(name="ETL Flow")
def load_staging_flow():

    # Load CSV files into corresponding staging tables
    load_csv_to_staging("stg_customers", "data/customers.csv")
    load_csv_to_staging("stg_products", "data/products.csv")
    load_csv_to_staging("stg_brands", "data/brands.csv")
    load_csv_to_staging("stg_categories", "data/categories.csv")
    load_csv_to_staging("stg_orders", "data/orders.csv")
    load_csv_to_staging("stg_order_items", "data/order_items.csv")
    load_csv_to_staging("stg_staffs", "data/staffs.csv")
    load_csv_to_staging("stg_stores", "data/stores.csv")

    # Build the Date Dimension
    run_sql_script("sql/build_dim_date.sql")
    
    # Run SCD Type 2 updates
    update_dim_customer()
    update_dim_staff()

    # Run SCD Type 1 updates
    update_dim_store()
    update_dim_product()

    # Run Fact SQL scripts
    run_sql_script("sql/insert_fact_table.sql")

    
# -------------------------
# Trigger locally
# -------------------------
if __name__ == "__main__":
    load_staging_flow()
