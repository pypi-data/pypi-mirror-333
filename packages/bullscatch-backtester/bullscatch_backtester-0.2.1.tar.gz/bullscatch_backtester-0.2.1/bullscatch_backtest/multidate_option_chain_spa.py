import concurrent.futures
import time
from typing import Dict, Tuple, List, Union
import pandas as pd
import psycopg2
from .config import DB_CONFIG

def get_db_connection():
    """Establish and return a database connection."""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def execute_query(table_name, fetch_date):
    """Fetch data from a given table on a specified date."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE timestamp::date = '{fetch_date}';"
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
    """Fetch all table names from the database."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
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
    nifty_options = df_tables[df_tables['Table Name'].str.contains(r'^nifty_.*_options$', case=False)].copy()
    sensex_options = df_tables[df_tables['Table Name'].str.contains(r'^sensex_.*_options$', case=False)].copy()

    nifty_options['Expiry Date'] = nifty_options['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')
    sensex_options['Expiry Date'] = sensex_options['Table Name'].str.extract(r'_(\d{4}_\d{2}_\d{2})_options$')

    return nifty_options, sensex_options

def get_expiry_type(date_str):
    """Determine whether the expiry is monthly ('m') or a weekly expiry."""
    date = pd.to_datetime(date_str, format='%Y_%m_%d')
    week_number = (date.day - 1) // 7 + 1  
    last_expiry = (date + pd.DateOffset(weeks=1)).month != date.month
    return 'm' if last_expiry else str(week_number)

def get_option_chain(fetch_date, nearest_expiry, instrument_name="nifty"):
    """
    Fetch the option chain for a particular instrument and date.

    Args:
        fetch_date (str): Date in 'YYYY-MM-DD' format.
        nearest_expiry (str): Expiry date in 'YYYY_MM_DD' format.
        instrument_name (str): "nifty" or "sensex". Default is "nifty".

    Returns:
        pd.DataFrame: Data from the fetched option chain table.
    """
    df_tables = fetch_table_names()
    if df_tables is None:
        return None

    # Extract expiry dates
    nifty_options, sensex_options = extract_expiry_dates(df_tables)

    # Choose the right dataset
    options_table = nifty_options if instrument_name == "nifty" else sensex_options

    # Get corresponding table name for the provided expiry
    expiry_table = options_table[options_table['Expiry Date'] == nearest_expiry]['Table Name']

    if expiry_table.empty:
        print(f"No table found for expiry {nearest_expiry}")
        return None

    table_name = expiry_table.values[0]
    return execute_query(table_name, fetch_date)

# from bullscatch_backtest.option_chain_spa import get_option_chain

class OptionDataFetcher:
    def __init__(self, max_workers: int = 10):
        """
        Initializes the OptionDataFetcher with a specified number of worker threads.
        """
        self.max_workers = max_workers

    def fetch_data(self, date_to_fetch: str, expiry_date: str) -> Tuple[Tuple[str, str], Union[dict, str]]:
        """
        Fetches option chain data for a given date and expiry.

        :param date_to_fetch: The date to fetch data for.
        :param expiry_date: The expiry date of the option contract.
        :return: A tuple containing (date, expiry) and the fetched data or an error message.
        """
        try:
            return (date_to_fetch, expiry_date), get_option_chain(date_to_fetch, expiry_date, "nifty")
        except Exception as e:
            return (date_to_fetch, expiry_date), f"Error: {e}"

    def fetch_all_data(self, date_expiry_pairs: List[Tuple[str, str]]) -> Dict[Tuple[str, str], Union[dict, str]]:
        """
        Fetches option chain data for multiple date-expiry pairs concurrently.

        :param date_expiry_pairs: List of tuples containing (date, expiry).
        :return: Dictionary mapping (date, expiry) to fetched data.
        """
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self.fetch_data, date, expiry): (date, expiry) for date, expiry in date_expiry_pairs}
            
            for future in concurrent.futures.as_completed(futures):
                (date, expiry), data = future.result()
                results[(date, expiry)] = data
                print(f"Fetched data for {date} - {expiry}")
        
        return results
