import pandas as pd
import psycopg2
from datetime import datetime
from .config import DB_CONFIG  # Ensure config.py contains DB credentials

def fetch_table_names():
    """Fetch all table names from the database and return as a DataFrame."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)

        tables = cursor.fetchall()
        df_tables = pd.DataFrame(tables, columns=['Table Name'])

        cursor.close()
        conn.close()
        return df_tables

    except Exception as e:
        print(f"Error fetching table names: {e}")
        return None

def spot_table(df_tables):
    """Extract spot table names from table names."""
    nifty_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_spot$', case=False)].copy()
    sensex_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_spot$', case=False)].copy()
    return nifty_spot_table, sensex_spot_table

def spot_query(table_name, input_date):
    """Execute a query to fetch spot data for a given instrument on a specified date."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        spot_query = f'SELECT * FROM "{table_name}" WHERE timestamp::date = %s;'
        cursor.execute(spot_query, (input_date,))
        rows = cursor.fetchall()

        spot_data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

        cursor.close()
        conn.close()
        return spot_data
    except Exception as e:
        print(f"Error executing query: {e}")
        return None

def get_table_name(df, input_date):
    """Find the matching table name based on input date."""
    input_year = input_date.year
    input_month = input_date.strftime('%b').upper()
    pattern = f"_{input_year}_{input_month}_"

    matching_table = df[df["Table Name"].str.contains(pattern, na=False, regex=False)]
    return matching_table.iloc[0]["Table Name"] if not matching_table.empty else None

def get_spot_data(date_str, instrument_type):
    """Reusable function to fetch spot data for a given date and instrument."""
    try:
        input_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None

    df_tables = fetch_table_names()
    if df_tables is None:
        return None

    nifty_spot_table, sensex_spot_table = spot_table(df_tables)

    if instrument_type.lower() == "nifty":
        spot_table_name = get_table_name(nifty_spot_table, input_date)
    elif instrument_type.lower() == "sensex":
        spot_table_name = get_table_name(sensex_spot_table, input_date)
    else:
        print("Invalid instrument. Choose 'nifty' or 'sensex'.")
        return None

    if not spot_table_name:
        print("No matching table found.")
        return None

    return spot_query(spot_table_name, input_date)
