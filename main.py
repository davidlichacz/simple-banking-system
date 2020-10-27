from random import randint
import sqlite3

conn = sqlite3.connect('card.s3db')

create_cards_table = '''CREATE TABLE IF NOT EXISTS card(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            number TEXT,
                            pin TEXT,
                            balance INTEGER DEFAULT 0
                        )'''

cur = conn.cursor()
cur.execute(create_cards_table)
conn.commit()

intro_message = ['1. Create an account', '2. Log into account', '0. Exit']
options_message = ['1. Balance', '2. Add income', '3. Do transfer', '4. Close account', '5. Log out', '0. Exit']

IIN = '400000'


def luhn(num):
    """
    Calculates a checksum digit using the Luhn algorithm.
    :rtype: str
    :param num: any positive integer passed as a string
    :return: a string representing the checksum digit calculated with the Luhn algorithm.
    """
    num_list = list(num)
    step_one = [2 * int(num_list[n]) if n % 2 == 0 else int(num_list[n]) for n in range(len(num_list))]
    step_two = [step_one[n] - 9 if step_one[n] > 9 else step_one[n] for n in range(len(step_one))]
    if sum(step_two) % 10 == 0:
        return '0'
    else:
        return str(10 - (sum(step_two) % 10))


def get_balance(card_number):
    balance_sql = f'SELECT balance FROM card WHERE number = {card_number}'
    cur.execute(balance_sql)
    balance_list = cur.fetchall()
    if balance_list:
        return balance_list[0][0]
    else:
        return None


class Account:
    def __init__(self):
        self.balance = 0
        self.card_number = None
        self.PIN = None

    def get_card_number(self):
        account_number = '%09d' % randint(0, 999999999)
        checksum = luhn(IIN + account_number)
        self.card_number = IIN + account_number + checksum

    def get_pin(self):
        self.PIN = '%04d' % randint(0, 9999)


continue_session = True

while continue_session:
    print(*intro_message, sep='\n')
    main_menu_choice = input()
    if main_menu_choice == '1':
        new_account = Account()
        new_account.get_card_number()
        new_account.get_pin()

        print('Your card has been created')
        print('Your card number:')
        print(new_account.card_number)
        print('Your card PIN:')
        print(new_account.PIN)

        insert_card = f'INSERT INTO card(number, pin) VALUES ("{new_account.card_number}", "{new_account.PIN}")'

        cur.execute(insert_card)
        conn.commit()

        continue

    elif main_menu_choice == '2':
        print('Enter your card number:')
        entered_card = input()
        print('Enter your PIN:')
        entered_PIN = input()

        cur.execute('SELECT number FROM card')
        numbers_result = cur.fetchall()
        numbers = [number[0] for number in numbers_result]

        pin_sql = f'SELECT pin FROM card WHERE number = {entered_card}'
        cur.execute(pin_sql)
        pin_result = cur.fetchall()

        if entered_card not in numbers:
            print('Wrong card number or PIN!')
            continue
        elif pin_result[0][0] != entered_PIN:
            print('Wrong card number or PIN!')
            continue
        else:
            print('You have successfully logged in!')

        while True:
            print(*options_message, sep='\n')
            sub_menu_choice = input()
            balance = get_balance(entered_card)

            if sub_menu_choice == '1':
                print('Balance: ', balance)
                continue
            elif sub_menu_choice == '2':
                print('Enter income:')
                income = int(input())
                income_sql = f'UPDATE card SET balance = {balance + income} WHERE number = {entered_card}'
                cur.execute(income_sql)
                conn.commit()
                print('Income was added!')
                continue
            elif sub_menu_choice == '3':
                print('Transfer')
                print('Enter card number:')
                destination = input()

                last_digit = destination[-1]
                first_digits = destination[:len(destination) - 1]

                if destination == entered_card:
                    print("You can't transfer money to the same account!")
                elif last_digit != luhn(first_digits):
                    print('Probably you made a mistake in the card number. Please try again!')
                elif destination not in numbers:
                    print('Such a card does not exist.')
                else:
                    print('Enter how much money you want to transfer:')
                    transfer = int(input())
                    if transfer > balance:
                        print('Not enough money!')
                    else:
                        balance_destination = get_balance(destination)
                        source_sql = f'UPDATE card SET balance = {balance - transfer} WHERE number = {entered_card}'
                        destination_sql = f'UPDATE card SET balance = {balance_destination + transfer} WHERE ' \
                                          f'number = {destination} '
                        cur.execute(source_sql)
                        cur.execute(destination_sql)
                        conn.commit()
                        print('Success!')
                continue
            elif sub_menu_choice == '4':
                close_sql = f'DELETE FROM card WHERE number = {entered_card}'
                cur.execute(close_sql)
                conn.commit()
                print('The account has been closed!')
                break
            elif sub_menu_choice == '5':
                print('You have successfully logged out!')
                break
            elif sub_menu_choice == '0':
                continue_session = False
                print('Bye!')
                break

    elif main_menu_choice == '0':
        print('Bye')
        break

    else:
        continue
