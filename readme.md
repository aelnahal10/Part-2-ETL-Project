```markdown
# 🏪 Retail ETL Project – From OLTP to OLAP with SQL Server, Python & Prefect

A complete end-to-end ETL pipeline that transforms a normalized OLTP schema (from an e-commerce retail system) into a clean OLAP star schema, using **SQL Server**, **Python**, **Prefect**, and **SQLAlchemy**.

---

## 🚀 Project Overview

- ✅ **OLTP Dataset**: [Bike Store Sample](https://www.kaggle.com/datasets/dillonmyrick/bike-store-sample-database)
- 🎯 **Goal**: Build a data warehouse (`retail_dw`) for analytics, based on star schema and SCDs
- 🛠️ **Tech Stack**: SQL Server, Python, Pandas, Prefect, SQLAlchemy
- 📊 **BI Ready**: Designed for Power BI or Tableau consumption

---

## 📁 Project Structure

```

etl\_project/
├── sql/
│   ├── create\_olap\_schema.sql
│   ├── stage\_tables.sql
│   ├── populate\_dim\_date.sql
│   ├── scd\_type1\_product.sql
│   ├── scd\_type2\_customer.sql
│   ├── scd\_type1\_store.sql
│   ├── scd\_type2\_staff.sql
│   └── build\_fact\_sales.sql
├── python/
│   ├── flow\.py
│   ├── load\_staging.py
├── config.py
├── .env
├── README.md
└── data/
├── customers.csv
├── products.csv
├── ...

````

---

## 🧱 Features

- ✅ Builds staging, dimension & fact tables
- 🔁 Handles **SCD Type 1** and **SCD Type 2** logic
- 🧠 Supports surrogate keys and time-based tracking
- ⚙️ Automates workflow using **Prefect**
- 🧪 Easily testable with `.csv` source files

---

## 🔧 Requirements

Install the following dependencies:

```bash
pip install -r requirements.txt
````

### `requirements.txt`:

```
pandas
sqlalchemy
pymssql
prefect
python-dotenv
```

---

## 🖥️ Database Setup

Ensure **SQL Server** is running locally 
---

## 🔐 .env Configuration

Create a `.env` file at the root with your DB credentials:

```ini
SQL_SERVER=localhost
SQL_PORT=1433
SQL_USER=sa
SQL_PASSWORD=your_password
SQL_DATABASE=retail_dw
```

---

## 🧩 Step-by-Step Execution

### 1. Create OLAP Schema

```bash
python python/load_staging.py
```

* Runs `create_olap_schema.sql` and `stage_tables.sql`
* Loads CSVs into staging tables (`stg_*`)

### 2. Run Full ETL

```bash
python python/flow.py
```

* Executes all SQL scripts:

  * Dimensions: SCD Type 1 & 2
  * Date generator
  * Fact builder
* Logs steps to console or Prefect Cloud

---

## 🕒 Optional: Schedule Daily Run (Prefect)

Start Prefect agent:

```bash
prefect agent start --pool default-agent-pool
```

Then deploy flow (already included in `flow.py`):

```bash
python python/flow.py
```

Flow is now scheduled daily via `.serve()`.

---

## 📊 Power BI / BI Tools

* Connect to `retail_dw` via DirectQuery or Import
* Use `fact_sales` as base table
* Join to `dim_*` via surrogate keys

---

## 🧠 Learn More

This project is part of an educational YouTube series on:

* Dimensional Modeling
* SCDs
* ETL Design
* Workflow Automation

Follow the playlist and subscribe for more videos.

---

## 📬 Questions?

Reach out via LinkedIn or YouTube if you have questions, suggestions, or want to contribute.

---

```

Let me know if you want a `requirements.txt` generated or a version tailored to self-hosted SQL Server only.
```
