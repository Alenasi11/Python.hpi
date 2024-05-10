import csv
import re
from functools import wraps
import logging
import requests
import pymysql

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
def establish_db_connection():
    connection = pymysql.connect(
        host='Student',
        user='aliona.si',
        password='015673',
        database='allesha',
        cursorclass=pymysql.cursors.DictCursor
    )
    logger.info("Established DB connection.")
    return connection

# Database disconnection
def close_db_connection(connection):
    connection.close()
    logger.info("Closed DB connection.")

# Decorator for establishing DB connection
def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = establish_db_connection()
        result = func(connection, *args, **kwargs)
        close_db_connection(connection)
        return result
    return wrapper

# Placeholder for currency conversion logic
def convert_currency(amount, base_currency, target_currency, rates):
    # Placeholder logic for currency conversion
    if base_currency == target_currency:
        return amount
    if target_currency in rates:
        return amount * rates[target_currency]
    raise ValueError("Currency conversion not supported or rates not available.")

# Get exchange rates using API
def get_exchange_rates(api_key):
    endpoint = f"https://freecurrencyapi.com/api/v1/rates?apikey={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        return response.json()['rates']
    else:
        raise Exception("Failed to fetch exchange rates. Check API key and try again.")

# Validate user_full_name and split into name and surname
def validate_full_name(full_name):
    validated_name = re.sub(r'[^a-zA-Z\s]', '', full_name)
    name_parts = validated_name.split()
    if len(name_parts) >= 2:
        return name_parts[0], name_parts[1]
    else:
        raise ValueError("Invalid full name format. Please provide both name and surname.")

# API functions
@db_connection
def add_user(connection, user_data):
    try:
        name, surname = validate_full_name(user_data.get('user_full_name'))
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (name, surname) VALUES (%s, %s)", (name, surname))
            connection.commit()
        return "User added successfully."
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        return "Failed to add user."

@db_connection
def transfer_money(connection, sender_account, receiver_account, amount, base_currency, api_key):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT balance, currency FROM accounts WHERE account_number = %s", (sender_account,))
            sender_data = cursor.fetchone()
            sender_balance, sender_currency = sender_data

            rates = get_exchange_rates(api_key)
            converted_amount = convert_currency(amount, base_currency, sender_currency, rates)

            if sender_balance >= converted_amount:
                cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_number = %s", (converted_amount, sender_account))
                cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (converted_amount, receiver_account))
                connection.commit()
                return "Money transferred successfully."
            else:
                return "Insufficient balance for transfer."
    except Exception as e:
        logger.error(f"Error transferring money: {e}")
        return "Failed to transfer money."

# Example usage
if __name__ == "__main__":
    # Replace with your actual database credentials and API key
    db_host = 'Student'
    db_user = 'aliona.si'
    db_password = '015673'
    db_name = 'allesha'
    api_key = 'fca_live_FDCLgC96kvPo6cHWQJ90PyeKP6Ll5ZKT7Iq9UUze'

    # Example usage of functions
    print(add_user({'user_full_name': 'Alena Name'}))
    print(transfer_money('sender_account', 'receiver_account', 100, 'USD', api_key))
