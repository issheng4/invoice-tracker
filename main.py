"""Invoice Tracker"""

import sys
from datetime import date
import sqlite3

DB_NAME = 'invoices.db'

#--------------------------------------
# Database config functions
#--------------------------------------

def get_db_connection():
    """Returns a new SQLite database connection."""
    return sqlite3.connect(DB_NAME)

def init_db() -> None:
    """Initialises the database and creates the Invoices table if it does not exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                has_been_paid INTEGER NOT NULL
            )
        ''')
        conn.commit()

#--------------------------------------
# Database command functions
#--------------------------------------

ALLOWED_FIELDS = {'date', 'description', 'amount', 'has_been_paid'}

def add_invoice(event_date: date, description: str, amount: float, has_been_paid: bool) -> None:
    """Adds a new invoice to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Invoices (date, description, amount, has_been_paid)
            VALUES (?, ?, ?, ?)
        ''', (event_date.isoformat(), description, amount, int(has_been_paid)))
        conn.commit()

def retrieve_invoice_data(id: int, field: str) -> str:
    """Retrieves a value of an invoice in the database."""
    if field not in ALLOWED_FIELDS:
        raise ValueError('Invalid field name')

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT {field} FROM Invoices
            WHERE id = ?
        ''', (id,))
        row = cursor.fetchone()
        if row is None:
            raise ValueError('Invoice not found')
        value = row[0]
        if field == 'has_been_paid':
            return 'paid' if value else 'awaiting'
        return str(value)
    
def validate_invoice_id(id: int) -> bool:
    """Checks if invoice ID number input is valid."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM Invoices
            WHERE id = ?
        ''', (id,))
        row = cursor.fetchone()
        return row is not None

def edit_invoice(id: int, field: str, value: object) -> None:
    """Edits a value of an invoice in the database."""

    if field not in ALLOWED_FIELDS:
        raise ValueError('Invalid field name')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE Invoices
            SET {field} = ?
            WHERE id = ?
        ''', (value, id))
        conn.commit()

def get_total_amount() -> float:
    """Returns the total amount of all invoices."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(amount) FROM Invoices')
        total = cursor.fetchone()[0]
        return total or 0.0

def display_invoices() -> None:
    """Displays all invoices in a formatted table with a total row."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, date, description, amount, has_been_paid
            FROM Invoices
        ''')
        rows = cursor.fetchall()
        print('-' * 80)
        print(f"{'ID':<10} {'Date':<12} {'Description':<35} {'Amount':>9}  {'Status':<10}")
        print('-' * 80)
        for row in rows:
            invoice_id, date_str, description, amount, has_been_paid = row
            status = 'paid' if has_been_paid else 'awaiting'
            print(f'{invoice_id:<10} {date_str:<12} {description:<35} £{amount:>8.2f}  {status:<10}')
        total = get_total_amount()
        print('-' * 80)
        print(f"{'':<10} {'':<12} {'TOTAL':<35} £{total:>8.2f}  {'':<10}")
        print('-' * 80)

#--------------------------------------
# Ask-for-valid-input functions
#--------------------------------------

def ask_for_main_menu_option() -> str:
    """Prompts the user for a main menu option and validates the input."""
    while True:
        print('\nChoose one of the following options by entering the corresponding number:')
        print('  (1) Add an invoice')
        print('  (2) Edit an invoice')
        print('  (3) View all invoices')
        print('  (4) Exit')
        main_menu_input = input()
        if main_menu_input in ('1', '2', '3', '4'):
            return main_menu_input
        else:
            print('Invalid choice. Please enter a number between 1 and 4.')

def ask_for_invoice_date() -> date:
    """Prompts the user for an invoice date and validates the input."""
    while True:
        date_str = input('\nEnter the date of the event (YYYY-MM-DD): ')
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            print('Invalid date. Please use valid date in YYYY-MM-DD format.')

def ask_for_invoice_description() -> str:
    """Prompts the user for an invoice description."""
    return input('\nEnter a description of the event: ')

def ask_for_invoice_amount() -> float:
    """Prompts the user for an invoice amount and validates the input."""
    while True:
        try:
            amount_str = input('\nEnter the total fee on the invoice: ')
            amount = float(amount_str)
            if amount <= 0:
                print('Invalid number. Please enter an amount greater than 0.')
                continue
            if '.' in amount_str:
                if len(amount_str.split('.')[-1]) > 2:
                    print('Invalid number. Please enter an amount with no more than 2 decimal places')
                    continue
            return amount
        except ValueError:
            print('Invalid input. Please enter a number.')

def ask_for_invoice_paid_status() -> bool:
    """Prompts the user for the paid status of the invoice and validates the input."""
    while True:
        has_been_paid = input('\nHas this invoice been paid yet? (y/n): ')
        if has_been_paid.lower() in ('y', 'n'):
            return has_been_paid.lower() == 'y'
        else:
            print('Invalid input. Please enter y or n.')

def ask_for_invoice_id() -> int:
    """Prompts the user for an invoice ID and validates the input."""
    while True:
        try:
            invoice_id_str = input('\nEnter the ID number of the invoice you would like to edit: ')
            invoice_id = int(invoice_id_str)
            if not validate_invoice_id(invoice_id):
                print('Invalid number. Please enter a valid invoice ID.')
                continue
            return invoice_id
        except ValueError:
            print('Invalid input. Please enter a number.')

def ask_for_edit_invoice_option() -> str:
    """Prompts the user for an invoice edit option and validates the input."""
    while True:
        print('\nChoose one of the following options by entering the corresponding number:')
        print('  (1) Mark invoice as paid/not yet paid')
        print('  (2) Edit event date')
        print('  (3) Edit event description')
        print('  (4) Edit fee amount')
        edit_invoice_input = input()
        if edit_invoice_input in ('1', '2', '3', '4'):
            return edit_invoice_input
        else:
            print('Invalid choice. Please enter a number between 1 and 4.')

#--------------------------------------
# Main
#--------------------------------------

def main() -> None:
    """Main program loop."""
    init_db()
    while True:
        main_menu_input = ask_for_main_menu_option()
        try:
            if main_menu_input == '1':
                event_date = ask_for_invoice_date()
                description = ask_for_invoice_description()
                amount = ask_for_invoice_amount()
                has_been_paid = ask_for_invoice_paid_status()
                add_invoice(event_date, description, amount, has_been_paid)
            elif main_menu_input == '2':
                invoice_id = ask_for_invoice_id()
                edit_invoice_input = ask_for_edit_invoice_option()
                if edit_invoice_input == '1':
                    print(f'\nCurrent status: {retrieve_invoice_data(invoice_id, "has_been_paid")}')
                    edit_invoice(invoice_id, 'has_been_paid', ask_for_invoice_paid_status())
                elif edit_invoice_input == '2':
                    print(f'\nCurrent date: {retrieve_invoice_data(invoice_id, "date")}')
                    edit_invoice(invoice_id, 'date', ask_for_invoice_date())
                elif edit_invoice_input == '3':
                    print(f'\nCurrent description: {retrieve_invoice_data(invoice_id, "description")}')
                    edit_invoice(invoice_id, 'description', ask_for_invoice_description())
                else:
                    print(f'\nCurrent fee amount: {retrieve_invoice_data(invoice_id, "amount")}')
                    edit_invoice(invoice_id, 'amount', ask_for_invoice_amount())
            elif main_menu_input == '3':
                display_invoices()
            else:
                print('\nBye!')
                sys.exit(0)
        except ValueError as e:
            print(f'Error: {e}')

if __name__ == '__main__':
    main()