import sqlite3
from typing import List, Dict

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None

    def initialize_database(self):
        """
        Initialize the database with tables for option contracts.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS option_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            option_type TEXT NOT NULL, -- 'call' or 'put'
            strike_price REAL NOT NULL,
            expiration_date TEXT NOT NULL,
            bid_price REAL,
            ask_price REAL
        );
        """
        self._execute_query(create_table_query)

    def insert_option_contracts(self, contracts: List[Dict]):
        """
        Insert multiple option contracts into the database.

        :param contracts: A list of dictionaries, each representing an option contract.
        """
        insert_query = """
        INSERT INTO option_contracts (symbol, option_type, strike_price, expiration_date, bid_price, ask_price)
        VALUES (:symbol, :option_type, :strike_price, :expiration_date, :bid_price, :ask_price);
        """
        self._execute_query(insert_query, contracts, many=True)

    def retrieve_option_chain(self, symbol: str) -> List[Dict]:
        """
        Retrieve all option contracts for a given symbol.

        :param symbol: The symbol to filter option contracts.
        :return: A list of dictionaries representing the option chain.
        """
        select_query = """
        SELECT * FROM option_contracts WHERE symbol = ?;
        """
        return self._execute_query(select_query, (symbol,), fetch=True)

    def _execute_query(self, query: str, params=None, many=False, fetch=False):
        """
        Internal helper method to execute a query.

        :param query: SQL query to execute.
        :param params: Parameters for the query.
        :param many: Whether to execute many queries.
        :param fetch: Whether to fetch results.
        :return: Query results if fetch is True, otherwise None.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)

        cursor = self.connection.cursor()
        try:
            if many:
                cursor.executemany(query, params)
            else:
                cursor.execute(query, params or ())

            if fetch:
                return [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

            self.connection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        """
        Close the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
