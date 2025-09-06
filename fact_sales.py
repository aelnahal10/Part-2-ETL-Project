from prefect import task, get_run_logger
from sqlalchemy import text
from config import engine

@task
def insert_fact_sales():
    logger = get_run_logger()
    logger.info("Inserting data into fact_sales...")

    with engine.begin() as conn:
        with open("sql/insert_fact_sales.sql") as f:
            conn.execute(text(f.read()))

    logger.info("fact_sales insert complete.")
