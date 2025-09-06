import pandas as pd
from config import get_engine
from sqlalchemy import text
from prefect import task, get_run_logger


@task
def update_dim_store():
    logger = get_run_logger()
    logger.info("Updating dim_store using MERGE...")
    merge_sql = '''
    MERGE dim_store AS target
    USING stg_stores AS source
    ON target.store_id = source.store_id
    WHEN MATCHED THEN
        UPDATE SET
            store_name = source.store_name,
            city = source.city,
            state = source.state,
            zip_code = source.zip_code
    WHEN NOT MATCHED BY TARGET THEN
        INSERT (store_id, store_name, city, state, zip_code)
        VALUES (source.store_id, source.store_name, source.city, source.state, source.zip_code);
    '''

    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(merge_sql))
        logger.info("dim_store updated successfully.")
    except Exception as e:
        logger.error(f"Error updating dim_store: {e}")
        raise


@task
def update_dim_product():
    logger = get_run_logger()
    logger.info("Updating dim_product using MERGE...")
    merge_sql = '''
    MERGE dim_product AS target
    USING (
        SELECT
            p.product_id,
            p.product_name,
            c.category_name,
            b.brand_name,
            p.model_year,
            p.list_price
        FROM stg_products p
        LEFT JOIN stg_brands b ON p.brand_id = b.brand_id
        LEFT JOIN stg_categories c ON p.category_id = c.category_id
    ) AS source
    ON target.product_id = source.product_id
    WHEN MATCHED THEN
        UPDATE SET
            product_name = source.product_name,
            category_name = source.category_name,
            brand_name = source.brand_name,
            model_year = source.model_year,
            list_price = source.list_price
    WHEN NOT MATCHED BY TARGET THEN
        INSERT (product_id, product_name, category_name, brand_name, model_year, list_price)
        VALUES (source.product_id, source.product_name, source.category_name, source.brand_name, source.model_year, source.list_price);
    '''

    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(merge_sql))
        logger.info("dim_product updated successfully.")
    except Exception as e:
        logger.error(f"Error updating dim_product: {e}")
        raise