from prefect import task, get_run_logger
from sqlalchemy import text
from config import get_engine

@task
def reload_recent_fact_sales():
    logger = get_run_logger()
    logger.info("Reloading fact_sales for last 30 days...")
    # CDC: Change Data Capture for last 30 days
    # Partial Refresh: Delete and Insert for last 30 days
    sql = """ 
    DELETE FROM fact_sales
    WHERE order_date_sk IN (
        SELECT date_sk
        FROM dim_date
        WHERE full_date BETWEEN CAST(GETDATE() - 30 AS DATE) AND CAST(GETDATE() AS DATE)
    );

    INSERT INTO fact_sales (
        order_id,
        item_id,
        customer_sk,
        product_sk,
        staff_sk,
        store_sk,
        order_date_sk,
        quantity,
        list_price,
        discount,
        total_price
    )
    SELECT 
        oi.order_id,
        oi.item_id,
        dc.customer_sk,
        dp.product_sk,
        dsf.staff_sk,
        dst.store_sk,
        dd.date_sk,
        oi.quantity,
        oi.list_price,
        oi.discount,
        oi.quantity * oi.list_price * (1 - oi.discount) AS total_price
    FROM stg_order_items oi
    JOIN stg_orders o ON oi.order_id = o.order_id
    JOIN dim_customer dc ON o.customer_id = dc.customer_id AND dc.current_flag = 'Y'
    JOIN dim_product dp ON oi.product_id = dp.product_id
    JOIN dim_staff dsf ON o.staff_id = dsf.staff_id AND dsf.current_flag = 'Y'
    JOIN dim_store dst ON o.store_id = dst.store_id
    JOIN dim_date dd ON o.order_date = dd.full_date
    WHERE dd.full_date BETWEEN CAST(GETDATE() - 30 AS DATE) AND CAST(GETDATE() AS DATE);
    """
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text(sql))

    logger.info("Reload complete.")
