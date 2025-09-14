"""Invoice Tracker"""

import sys
from datetime import date

invoices = []
last_id = 0

def add_invoice(event_date: date, description: str, amount: float, has_been_paid: bool) -> None:
    """Add new invoice to invoices list"""
    global last_id
    last_id += 1

    invoice = {
        'id': last_id,
        'date': event_date,
        'description': description,
        'amount': amount,
        'paid': has_been_paid
    }
    invoices.append(invoice)

def edit_invoice() -> None:
    pass

def view_invoices() -> None:
    print()
    for invoice in invoices:
        print(f'INVOICE {invoice["id"]}:')
        print(f'{invoice["date"]} | {invoice["description"]}')
        print(f'£{invoice["amount"]:.2f} {"received" if invoice["paid"] else "awaiting"}')
        print()


def main() -> None:
    while True:
        while True:
            print('\nChoose one of the following options by entering the corresponding number:')
            print('  (1) Add an invoice')
            print('  (2) Edit an invoice / Mark invoice as paid')
            print('  (3) View all invoices')
            print('  (4) Exit')
            main_menu_input = input()
            if main_menu_input in ('1', '2', '3', '4'):
                break
            else:
                print('Invalid choice. Please enter a number between 1 and 4.')

        if main_menu_input == '1':
            while True:
                date_str = input('\nEnter the date of the event (YYYY-MM-DD): ')
                try:
                    event_date = date.fromisoformat(date_str)
                    break
                except ValueError:
                    print('Invalid date. Please use valid date in YYYY-MM-DD format.')

            description = input('\nEnter a description of the event: ')

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

                    break
                except ValueError:
                    print('Invalid input. Please enter a number.')
                
            while True:
                has_been_paid = input('\nHas this invoice been paid yet? (y/n): ')
                if has_been_paid.lower() in ('y', 'n'):
                    has_been_paid = has_been_paid.lower() == 'y'
                    break
                else:
                    print('Invalid input. Please enter y or n.')

            add_invoice(event_date, description, amount, has_been_paid)




        elif main_menu_input == '2':
            edit_invoice()
        elif main_menu_input == '3':
            view_invoices()
        else:
            sys.exit(0)




if __name__ == '__main__':
    main()