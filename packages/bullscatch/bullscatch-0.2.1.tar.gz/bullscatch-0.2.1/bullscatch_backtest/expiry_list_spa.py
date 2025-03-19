import pandas as pd
import psycopg2
from .config import DB_CONFIG

def execute_query(table_name, fetch_date):
    """Execute a query to fetch data from a given table on a specified date."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = f"SELECT * FROM {table_name} WHERE timestamp::date = '{fetch_date}' LIMIT 10;"
        cursor.execute(query)
        rows = cursor.fetchall()

        df_data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

        cursor.close()
        conn.close()
        return df_data

    except Exception as e:
        print(f"Error executing query: {e}")
        return None

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

def extract_expiry_dates(df_tables):
    """Extract expiry dates from table names."""
    nifty_options_table = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_options$', case=False)].copy()
    sensex_options_table = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_options$', case=False)].copy()

    nifty_options_table['Expiry Date'] = nifty_options_table['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')
    sensex_options_table['Expiry Date'] = sensex_options_table['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')

    return nifty_options_table, sensex_options_table

def get_expiry_type(date_str):
    """Determine whether the expiry is monthly ('m') or a specific weekly expiry."""
    date = pd.to_datetime(date_str, format='%Y_%m_%d')
    week_number = (date.day - 1) // 7 + 1  
    last_expiry = (date + pd.DateOffset(weeks=1)).month != date.month
    return 'm' if last_expiry else str(week_number)

def spot_table(df_tables):
    """Extract spot table name from table names."""
    nifty_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_spot$', case=False)].copy()
    sensex_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_spot$', case=False)].copy()
    return nifty_spot_table, sensex_spot_table

def get_expiries(instrument_name, instrument_type, user_date):
    """Fetch available expiry dates for the selected month and the next two months."""
    df_tables = fetch_table_names()
    if df_tables is None:
        return None

    # Extract expiry dates
    nifty_options_table, sensex_options_table = extract_expiry_dates(df_tables)

    # Create expiry DataFrames
    nifty_expiry = nifty_options_table[['Expiry Date']].dropna().reset_index(drop=True)
    sensex_expiry = sensex_options_table[['Expiry Date']].dropna().reset_index(drop=True)

    # Assign expiry types
    nifty_expiry['expiry_type'] = nifty_expiry['Expiry Date'].apply(get_expiry_type)
    sensex_expiry['expiry_type'] = sensex_expiry['Expiry Date'].apply(get_expiry_type)

    # Select expiry DataFrame based on instrument
    if instrument_name == "nifty" and instrument_type == "options":
        expiry_df = nifty_expiry
    elif instrument_name == "sensex" and instrument_type == "options":
        expiry_df = sensex_expiry
    else:
        print("Invalid instrument name or type.")
        return None

    # Convert expiry dates to datetime format
    expiry_df['Expiry Date'] = pd.to_datetime(expiry_df['Expiry Date'], format='%Y_%m_%d')

    # Convert user input date to datetime
    user_date_obj = pd.to_datetime(user_date, format='%Y-%m-%d')

    # Get the first day of the selected month
    start_date = user_date_obj.replace(day=1)

    # Get the first day of the month 2 months ahead
    end_date = (start_date + pd.DateOffset(months=3)).replace(day=1)

    # Filter expiry dates within the range
    selected_expiries = expiry_df[(expiry_df['Expiry Date'] >= start_date) & (expiry_df['Expiry Date'] < end_date)]

    return selected_expiries


# import pandas as pd
# import psycopg2
# from config import DB_CONFIG

# def execute_query(table_name, fetch_date):
#     """Execute a query to fetch data from a given table on a specified date."""
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()

#         query = f"SELECT * FROM {table_name} WHERE timestamp::date = '{fetch_date}' LIMIT 10;"
#         cursor.execute(query)
#         rows = cursor.fetchall()

#         # Convert to DataFrame
#         df_data = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
#         spot = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])


#         cursor.close()
#         conn.close()
#         return df_data, spot

#     except Exception as e:
#         print(f"Error executing query: {e}")
#         return None
    
# def fetch_table_names():
#     """Fetch all table names from the database and return as a DataFrame."""
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()

#         cursor.execute("""
#             SELECT table_name 
#             FROM information_schema.tables 
#             WHERE table_schema = 'public';
#         """)

#         tables = cursor.fetchall()
#         df_tables = pd.DataFrame(tables, columns=['Table Name'])

#         cursor.close()
#         conn.close()
#         return df_tables

#     except Exception as e:
#         print(f"Error fetching table names: {e}")
#         return None

# def extract_expiry_dates(df_tables):
#     """Extract expiry dates from table names."""
#     nifty_options_table = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_options$', case=False)].copy()
#     sensex_options_table = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_options$', case=False)].copy()


#     nifty_options_table['Expiry Date'] = nifty_options_table['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')
#     sensex_options_table['Expiry Date'] = sensex_options_table['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')

#     return nifty_options_table, sensex_options_table

# def get_expiry_type(date_str):
#     """Determine whether the expiry is monthly ('m') or a specific weekly expiry."""
#     date = pd.to_datetime(date_str, format='%Y_%m_%d')
#     week_number = (date.day - 1) // 7 + 1  
#     last_expiry = (date + pd.DateOffset(weeks=1)).month != date.month
#     return 'm' if last_expiry else str(week_number)

# def spot_table(df_tables):
#     """Extract spot table name from table names."""
#     nifty_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_spot$', case=False)].copy()
#     sensex_spot_table = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_spot$', case=False)].copy()
#     return nifty_spot_table, sensex_spot_table

# def main():
#     # Fetch table names
#     df_tables = fetch_table_names()
#     if df_tables is None:
#         print("Failed to fetch table names. Exiting.")
#         return
    
#     # Extract expiry dates
#     nifty_options_table, sensex_options_table = extract_expiry_dates(df_tables)

#     # Create expiry DataFrames
#     nifty_expiry = nifty_options_table[['Expiry Date']].dropna().reset_index(drop=True)
#     sensex_expiry = sensex_options_table[['Expiry Date']].dropna().reset_index(drop=True)

#     # Assign expiry types
#     nifty_expiry['expiry_type'] = nifty_expiry['Expiry Date'].apply(get_expiry_type)
#     sensex_expiry['expiry_type'] = sensex_expiry['Expiry Date'].apply(get_expiry_type)

#     # Get user input
#     user_date = input("Enter the date (YYYY-MM-DD): ").strip()
#     instrument_name = 'nifty' #input("Enter the instrument name (nifty/sensex): ").strip().lower()
#     instrument_type = 'options' #input("Enter the instrument type (options/spot): ").strip().lower()
    
    
#     user_date_obj = pd.to_datetime(user_date, format='%Y-%m-%d')

#     # Select expiry DataFrame based on user input
#     if instrument_name == "nifty" and instrument_type == "options":
#         expiry_df = nifty_expiry
#         options_table = nifty_options_table
#     elif instrument_name == "sensex" and instrument_type == "options":
#         expiry_df = sensex_expiry
#         options_table = sensex_options_table
#     else:
#         print("Invalid instrument name or type. Exiting.")
#         return

#     # Get available expiries for the given month
#     selected_month_expiries = expiry_df[expiry_df['Expiry Date'].str.startswith(user_date_obj.strftime('%Y_%m'))]

#     if selected_month_expiries.empty:
#         print(f"No expiry found for {instrument_name} {instrument_type} in {user_date_obj.strftime('%B %Y')}")
#         return

#     # Display expiry options
#     print("\nAvailable Expiries:")
#     for i, expiry in enumerate(selected_month_expiries['Expiry Date']):
#         print(f"{i + 1}. {expiry}")

     
# if __name__ == "__main__":
#     main()