"""Invoice Tracker"""

import sys
from datetime import date

# Type alias for invoice dictionary
Invoice = dict[str, object]

invoices: dict[int, Invoice] = {}
last_id = 0

def add_invoice(event_date: date, description: str, amount: float, has_been_paid: bool) -> None:
    """Add new invoice to invoices list"""
    global last_id
    last_id += 1
    invoice: Invoice = {
        'id': last_id,
        'date': event_date,
        'description': description,
        'amount': amount,
        'has_been_paid': has_been_paid
    }
    invoices[last_id] = invoice

def edit_invoice(id: int, field: str, value: object) -> None:
    if id in invoices:
        invoices[id][field] = value


def view_invoices() -> None:
    print()
    for invoice in invoices.values():
        print(f'INVOICE {invoice["id"]}:')
        print(f'{invoice["date"]} | {invoice["description"]}')
        print(f'£{invoice["amount"]:.2f} {"received" if invoice["has_been_paid"] else "awaiting"}')
        print()

def ask_for_main_menu_option() -> str:
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
    while True:
        date_str = input('\nEnter the date of the event (YYYY-MM-DD): ')
        try:
            return date.fromisoformat(date_str)
        except ValueError:
            print('Invalid date. Please use valid date in YYYY-MM-DD format.')

def ask_for_invoice_description() -> str:
    return input('\nEnter a description of the event: ')

def ask_for_invoice_amount() -> float:
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
    while True:
        has_been_paid = input('\nHas this invoice been paid yet? (y/n): ')
        if has_been_paid.lower() in ('y', 'n'):
            return has_been_paid.lower() == 'y'
        else:
            print('Invalid input. Please enter y or n.')

def ask_for_invoice_id() -> int:
    while True:
        try:
            invoice_id_str = input('\nEnter the number of the invoice you would like to edit: ')
            invoice_id = int(invoice_id_str)
            if invoice_id not in invoices:
                print('Invalid number. Please enter a valid invoice number.')
                continue
            return invoice_id
        except ValueError:
            print('Invalid input. Please enter a number.')

def ask_for_edit_invoice_option() -> str:
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


def main() -> None:
    while True:
        main_menu_input = ask_for_main_menu_option()

        if main_menu_input == '1':
            event_date = ask_for_invoice_date()
            description = ask_for_invoice_description()
            amount = ask_for_invoice_amount()
            has_been_paid = ask_for_invoice_paid_status()

            add_invoice(event_date, description, amount, has_been_paid)

        elif main_menu_input == '2':
            invoice_id = ask_for_invoice_id()
            edit_invoice_input = ask_for_edit_invoice_option()
            invoice = invoices.get(invoice_id)
            if not invoice:
                print('Invoice not found.')
                continue

            if edit_invoice_input == '1':
                print(f'\nCurrent status: {invoice.get("has_been_paid")}')
                edit_invoice(invoice_id, 'has_been_paid', ask_for_invoice_paid_status())

            elif edit_invoice_input == '2':
                print(f'\nCurrent date: {invoice.get("date")}')
                edit_invoice(invoice_id, 'date', ask_for_invoice_date())

            elif edit_invoice_input == '3':
                print(f'\nCurrent description: {invoice.get("description")}')
                edit_invoice(invoice_id, 'description', ask_for_invoice_description())

            else:
                print(f'\nCurrent fee amount: {invoice.get("amount")}')
                edit_invoice(invoice_id, 'amount', ask_for_invoice_amount())

        elif main_menu_input == '3':
            view_invoices()
        else:
            print('\nGoodbye!')
            sys.exit(0)




if __name__ == '__main__':
    main()