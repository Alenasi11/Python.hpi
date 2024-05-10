import sqlite3
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Script to setup initial database structure.')
parser.add_argument('--unique_names', action='store_true', help='Set uniqueness on User.Name and User.Surname')
args = parser.parse_args()

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Bank (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Transaction (
    id INTEGER PRIMARY KEY,
    Bank_sender_name TEXT NOT NULL,
    Account_sender_id INTEGER NOT NULL,
    Bank_receiver_name TEXT NOT NULL,
    Account_receiver_id INTEGER NOT NULL,
    Sent_Currency TEXT NOT NULL,
    Sent_Amount REAL NOT NULL,
    Datetime TEXT
);
''')

# Determine uniqueness constraints for User table
user_uniqueness = ''
if args.unique_names:
    user_uniqueness = 'UNIQUE (Name, Surname),'

cursor.execute(f'''
CREATE TABLE IF NOT EXISTS User (
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Surname TEXT NOT NULL,
    Birth_day TEXT,
    Accounts TEXT NOT NULL,
    {user_uniqueness}
    FOREIGN KEY (Accounts) REFERENCES Account(Id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Account (
    Id INTEGER PRIMARY KEY,
    User_id INTEGER NOT NULL,
    Type TEXT NOT NULL CHECK (Type IN ('credit', 'debit')),
    Account_Number TEXT NOT NULL UNIQUE,
    Bank_id INTEGER NOT NULL,
    Currency TEXT NOT NULL,
    Amount REAL NOT NULL,
    Status TEXT CHECK (Status IN ('gold', 'silver', 'platinum')),
    FOREIGN KEY (User_id) REFERENCES User(Id),
    FOREIGN KEY (Bank_id) REFERENCES Bank(Id)
);
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database setup complete.")
