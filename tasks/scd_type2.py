import pandas as pd
from config import get_engine
from sqlalchemy import text
from prefect import task, get_run_logger

@task
def update_dim_staff():
    logger = get_run_logger()
    logger.info("Updating dim_staff (SCD Type 2)...")

    merge_sql = """
    -- Mark old records as historical
    UPDATE dim_staff
    SET end_date = GETDATE(), current_flag = 'N'
    WHERE current_flag = 'Y'
      AND EXISTS (
        SELECT 1 FROM stg_staffs s
        WHERE s.staff_id = dim_staff.staff_id
          AND (
              ISNULL(ISNULL(s.first_name, '') + ' ' + ISNULL(s.last_name, ''), '') <> ISNULL(dim_staff.full_name, '') OR
              ISNULL(s.email, '') <> ISNULL(dim_staff.email, '') OR
              ISNULL(CAST(s.phone AS NVARCHAR), '') <> ISNULL(CAST(dim_staff.phone AS NVARCHAR), '') OR
              ISNULL(s.store_id, -1) <> ISNULL(dim_staff.store_id, -1) OR
              ISNULL(s.manager_id, -1) <> ISNULL(dim_staff.manager_id, -1)
          )
      );

    -- Insert new or changed records
    INSERT INTO dim_staff (
        staff_id, full_name, email, phone, store_id, manager_id,
        start_date, end_date, current_flag
    )
    SELECT
        s.staff_id,
        ISNULL(s.first_name, '') + ' ' + ISNULL(s.last_name, ''),
        s.email, s.phone, s.store_id, s.manager_id,
        GETDATE(), NULL, 'Y'
    FROM stg_staffs s
    LEFT JOIN dim_staff d
        ON s.staff_id = d.staff_id AND d.current_flag = 'Y'
    WHERE d.staff_id IS NULL
       OR (
           ISNULL(ISNULL(s.first_name, '') + ' ' + ISNULL(s.last_name, ''), '') <> ISNULL(d.full_name, '') OR
           ISNULL(s.email, '') <> ISNULL(d.email, '') OR
           ISNULL(CAST(s.phone AS NVARCHAR), '') <> ISNULL(CAST(d.phone AS NVARCHAR), '') OR
           ISNULL(s.store_id, -1) <> ISNULL(d.store_id, -1) OR
           ISNULL(s.manager_id, -1) <> ISNULL(d.manager_id, -1)
       );
    """

    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(merge_sql))
        logger.info("dim_staff updated successfully.")
    except Exception as e:
        logger.error(f"Error updating dim_staff: {e}")
        raise



@task
def update_dim_customer():
    logger = get_run_logger()
    logger.info("Updating dim_customer (SCD Type 2)...")

    merge_sql = """
    -- Mark old records as historical
    UPDATE dim_customer
    SET end_date = GETDATE(), current_flag = 'N'
    WHERE current_flag = 'Y'
      AND EXISTS (
        SELECT 1 FROM stg_customers s
        WHERE s.customer_id = dim_customer.customer_id
          AND (
              ISNULL(s.first_name + ' ' + s.last_name, '') <> ISNULL(dim_customer.full_name, '') OR
              ISNULL(s.email, '') <> ISNULL(dim_customer.email, '') OR
              ISNULL(s.phone, '') <> ISNULL(dim_customer.phone, '') OR
              ISNULL(s.city, '') <> ISNULL(dim_customer.city, '') OR
              ISNULL(s.state, '') <> ISNULL(dim_customer.state, '') OR
              ISNULL(s.zip_code, '') <> ISNULL(dim_customer.zip_code, '')
          )
      );

    -- Insert new records
    INSERT INTO dim_customer (
        customer_id, full_name, email, phone, city, state, zip_code,
        start_date, end_date, current_flag
    )
    SELECT
        s.customer_id,
        s.first_name + ' ' + s.last_name,
        s.email, s.phone, s.city, s.state, s.zip_code,
        GETDATE(), NULL, 'Y'
    FROM stg_customers s
    LEFT JOIN dim_customer d
        ON s.customer_id = d.customer_id AND d.current_flag = 'Y'
    WHERE d.customer_id IS NULL
       OR (
           ISNULL(s.first_name + ' ' + s.last_name, '') <> ISNULL(d.full_name, '') OR
           ISNULL(s.email, '') <> ISNULL(d.email, '') OR
           ISNULL(s.phone, '') <> ISNULL(d.phone, '') OR
           ISNULL(s.city, '') <> ISNULL(d.city, '') OR
           ISNULL(s.state, '') <> ISNULL(d.state, '') OR
           ISNULL(s.zip_code, '') <> ISNULL(d.zip_code, '')
       );
    """

    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(merge_sql))
        logger.info("dim_customer updated successfully.")
    except Exception as e:
        logger.error(f"Error updating dim_customer: {e}")
        raise
