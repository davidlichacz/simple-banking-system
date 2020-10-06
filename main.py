from random import randint

intro_message = ['1. Create an account', '2. Log into account', '0. Exit']
options_message = ['1. Balance', '2. Log out', '0. Exit']

IIN = '400000'

session_accounts = {}

def luhn(num):
    """
    Calculates a checksum digit using the Luhn algorithm.
    :param num: any positive integer passed as a string
    :return: the checksum digit calculated with the Luhn algorithm.
    """
    num_list = list(num)
    step_one = [2 * int(num_list[n]) if n % 2 == 0 else int(num_list[n]) for n in range(len(num_list))]
    step_two = [step_one[n] - 9 if step_one[n] > 9 else step_one[n] for n in range(len(step_one))]
    if sum(step_two) % 10 == 0:
        return '0'
    else:
        return str(10 - (sum(step_two) % 10))


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

        session_accounts[new_account.card_number] = new_account

        print('Your card has been created')
        print('Your card number:')
        print(new_account.card_number)
        print('Your card PIN:')
        print(new_account.PIN)

        continue

    elif main_menu_choice == '2':
        print('Enter your card number:')
        entered_card = input()
        print('Enter your PIN:')
        entered_PIN = input()

        if entered_card not in session_accounts:
            print('Wrong card number or PIN!')
            continue
        elif session_accounts[entered_card].PIN != entered_PIN:
            print('Wrong card number or PIN!')
            continue
        else:
            print('You have successfully logged in!')

        while True:
            print(*options_message, sep='\n')
            sub_menu_choice = input()

            if sub_menu_choice == '1':
                print('Balance: ', session_accounts[entered_card].balance)
                continue
            elif sub_menu_choice == '2':
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
