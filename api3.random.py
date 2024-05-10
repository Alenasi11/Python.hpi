import random
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class User:
    def __init__(self, user_id, first_name, last_name, birth_date, credit_discount):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.credit_discount = credit_discount

    def full_name(self):
        """Returns the full name of the user."""
        return f"{self.first_name} {self.last_name}"

class Bank:
    def __init__(self, bank_id):
        self.bank_id = bank_id
        self.users = []

    def add_user(self, user):
        """Adds a user to the bank."""
        self.users.append(user)

    def oldest_client(self):
        """Returns the full name of the oldest client."""
        if not self.users:
            return None
        oldest_user = min(self.users, key=lambda u: u.birth_date)
        return oldest_user.full_name()

    def highest_discount_users(self):
        """Returns a collection of user_ids with corresponding discounts."""
        if not self.users:
            return None
        return {user.user_id: user.credit_discount for user in self.users}

    def delete_incomplete_users(self):
        """Deletes users and accounts that don't have full information."""
        self.users = [user for user in self.users if all([user.first_name, user.last_name, user.birth_date])]

    def transactions_past_3_months(self, user_id):
        """Returns transactions of a particular user for the past 3 months."""
        # Implementation for fetching transactions from a database or API
        # For simplicity, returning dummy data
        today = datetime.now()
        three_months_ago = today.replace(month=today.month - 3)
        return f"Transactions for user {user_id} from {three_months_ago} to {today}"

def generate_random_users(max_users=10):
    """Generates random users."""
    first_names = ["John", "Jane", "Michael", "Emma", "David", "Olivia"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis"]
    banks = ["Bank A", "Bank B", "Bank C"]
    users = []
    for _ in range(random.randint(1, max_users)):
        user_id = random.randint(1000, 9999)
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        birth_date = datetime.now().replace(year=random.randint(1950, 2000))
        credit_discount = random.choice([25, 30, 50])
        bank_id = random.choice(banks)
        user = User(user_id, first_name, last_name, birth_date, credit_discount)
        users.append((bank_id, user))
    return users

def main():
    try:
        users = generate_random_users()
        banks = {bank_id: Bank(bank_id) for bank_id in set([bank_id for bank_id, _ in users])}

        for bank_id, user in users:
            banks[bank_id].add_user(user)

        for bank_id, bank in banks.items():
            oldest_client = bank.oldest_client()
            highest_discount_users = bank.highest_discount_users()
            if oldest_client:
                logging.info(f"The oldest client of {bank_id} is: {oldest_client}")
            if highest_discount_users:
                logging.info(f"Highest discount users for {bank_id}: {highest_discount_users}")

            bank.delete_incomplete_users()

        user_id_to_fetch = random.choice(list(banks.values())).users[0].user_id
        for bank_id, bank in banks.items():
            transactions = bank.transactions_past_3_months(user_id_to_fetch)
            if transactions:
                logging.info(transactions)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
