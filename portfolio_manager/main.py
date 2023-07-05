import re
import os
import sys
import fidelity_csv_parser
from .utils import format_cents
from .objects.account import Account
from .objects.portfolio import Portfolio
from constants import ACCOUNTS, TASKS
from .objects.account_details import AccountDetails

# Colors
blues = [u"\u001b[38;5;32m", u"\u001b[38;5;39m"]
greens = [u"\u001b[38;5;34m", u"\u001b[38;5;76m"]
purple = u"\033[0;35m"
orange = u"\u001b[38;5;172m"
default = u"\u001b[0m"
warning = u'\033[93m'
bold = u'\033[1m'

# -------------------------------------------------------------------------
# Prints a message in blue font
# -------------------------------------------------------------------------
def printBlue(message):
    print(f'{blues[1]}{message}{default}')

# -------------------------------------------------------------------------
# Prints cash-related error text to output
# -------------------------------------------------------------------------
def showCashErrorMessage():
    print(f'\n{warning}Oops! The value must be a number.{default}\n')

# -------------------------------------------------------------------------
# Prints file-related error text to output
# -------------------------------------------------------------------------
def showFileErrorMessage():
    print(f'\n{warning}Oops! The file could not be found.{default}\n')

# -------------------------------------------------------------------------
# Prints comma-separated list of integers -related error text to output
# -------------------------------------------------------------------------
def showIntListErrorMessage():
    print(f'\n{warning}Oops! Please provide a comma-separated list of integers.{default}\n')

# -------------------------------------------------------------------------
# Prints empty account list error text to output
# -------------------------------------------------------------------------
def showNoAccountsRequestedErrorMessage():
    print(f'\n{warning}You must choose at least 1 account.{default}\n')

# -------------------------------------------------------------------------
# Prints non-int error text to output
# -------------------------------------------------------------------------
def showNonIntErrorMessage():
    print(f'\n{warning}You must enter a single integer from the list above.{default}\n')

# -------------------------------------------------------------------------
# Prints help text to output
# -------------------------------------------------------------------------
def outputHelpText():
    print("""\nbrokerage_rebalance.py [options]
            
        -h, --help      Show simple help text
        -c, --cash      Provide investment amount to include in calculations
        -f, --file      Provide Fidelity CSV file path to include in calculations\n""")

# -------------------------------------------------------------------------
# Handles operation when user provides the 'help' option
# -------------------------------------------------------------------------
def helpOption():
    outputHelpText()
    sys.exit()

# -------------------------------------------------------------------------
# This method gets a valid cash value from the user. This method is useful
# when no cash amount is provided by the user or the value provided is
# invalid.
# -------------------------------------------------------------------------
def getCashAmountFromUser():
    while True:
        try:
            dollars = float(input(f'\nEnter the amount of cash you are investing: {greens[1]}${default}'))
            cents = dollars * 100
            return cents
        except ValueError:
            showCashErrorMessage()

# -------------------------------------------------------------------------
# Strips the quotations from the end of a string
# -------------------------------------------------------------------------
def stripQuotations(val):
    return re.sub(r'[\'\"]', '', val)

# -------------------------------------------------------------------------
# This method gets a valid file path from the user. This method is useful
# when no file path is provided by the user or the path provided is
# invalid.
# -------------------------------------------------------------------------
def getFileFromUser():
    try:
        dir_path = 'text_files'
        db_file_path = os.path.join(dir_path, 'csv_name.txt')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        csv_file_path = input(f'\n{blues[1]}Enter the Fidelity CSV file path ("f" to use last-used file): {greens[1]}${default}')
        if csv_file_path == 'f':
            with open(db_file_path, 'r') as db_file:
                csv_file_path = db_file.readline()
        else:
            with open(db_file_path, 'w') as db_file:
                db_file.write(csv_file_path)
        return open(stripQuotations(csv_file_path))
    except FileNotFoundError:
        showFileErrorMessage()
        return getFileFromUser()

# -------------------------------------------------------------------------
# Handles operation when user provides the 'cash' option and arg
# Converts dollar int to cent int
# -------------------------------------------------------------------------
def cashOption(cash_input):
    try:
        return float(cash_input) * 100
    except ValueError:
        showCashErrorMessage()
        return getCashAmountFromUser()

# -------------------------------------------------------------------------
# Shows the opening message to the user.
# -------------------------------------------------------------------------
def showOpeningMessage():
    print('************************************')
    print(f'* {bold}Welcome! It\'s {greens[1]}money{default}{bold} timmmeeeeeee{default} *')
    print('************************************\n')

# -------------------------------------------------------------------------
# Ask which accounts the user wants to work with
# -------------------------------------------------------------------------
def getAccountsOfInterest():
    printBlue("Which accounts would you like to manage? (comma-separated list)\n")
    for index, account in ACCOUNTS.items():
        print(f'{index}) {account.name}')
    
    print()
    while True:
        try:
            intList = [ACCOUNTS[val] for val in re.split(r'\D+', input('> ')) if int(val) > 0 and int(val) <= len(ACCOUNTS)]
            if intList == []:
                showNoAccountsRequestedErrorMessage()
            else:
                return intList
        except:
            showIntListErrorMessage()

# -------------------------------------------------------------------------
# Get desired task for each account
# -------------------------------------------------------------------------
def getTasksForAccounts(account_details_list: list[AccountDetails]):
    inputTasks = []
    for account_details in account_details_list:
        printBlue(f'\nWhat would you like to do with your {account_details.name} account? (enter number)\n')
        for index, task in enumerate(TASKS, start=1):
            print(f'{index}) {task}')
        while True:
            try:
                inputTasks.append(int(input('\n> ')))
                break
            except ValueError:
                showNonIntErrorMessage()
    return inputTasks

# -------------------------------------------------------------------------
# Get desired task for portfolio accounts
# -------------------------------------------------------------------------
def getTasksForPortfolioAccounts(portfolio: Portfolio):
    inputTasks = []
    for account in portfolio.accounts:
        printBlue(f'\nWhat would you like to do with your {account.name} account? (enter number)\n')
        for index, task in enumerate(TASKS, start=1):
            print(f'{index}) {task}')
        while True:
            try:
                inputTasks.append(int(input('\n> ')))
                break
            except ValueError:
                showNonIntErrorMessage()
    return inputTasks

# -------------------------------------------------------------------------
# Ask the user if they want to consider additional cash besides what is
# already in the account.
# -------------------------------------------------------------------------
def getAdditionalCash(account_details_list: list[AccountDetails]):
    additionalCash = []
    for account_details in account_details_list:
        printBlue(f'\nWould you like to consider additional cash for your {account_details.name} account? (y/n)\n')
        answer = input('> ').lower()
        if answer == 'y':
            additionalCash.append(getCashAmountFromUser())
        else:
            additionalCash.append(0)
    return additionalCash

# -------------------------------------------------------------------------
# Ask the user if they want to consider additional cash besides what is
# already in the Portfolio accounts.
# -------------------------------------------------------------------------
def getAdditionalCash2(portfolio: Portfolio):
    additionalCash = []
    for account in portfolio.accounts:
        printBlue(f'\nWould you like to consider additional cash for your {account.name} account? (y/n)\n')
        answer = input('> ').lower()
        if answer == 'y':
            additionalCash.append(getCashAmountFromUser())
        else:
            additionalCash.append(0)
    return additionalCash

def investBalancedBinance(account_balances):
    print('Investing in Binance.US account')
    # account_details_list = [AccountDetails('binance', 'Binance.US')]
    # assets = binance_parser
    
def manage_kraken(portfolio: Portfolio):
    print("Managing kraken")
    # Ask user for task (e.g. invest, rebalance)
    tasks = getTasksForPortfolioAccounts(portfolio)
    # Get other info (e.g. how much $ to invest)
    additionalCash = getAdditionalCash(portfolio)
    # Do actual stuff
    print(f'Portfolio:\n{portfolio}')
    for index, account in enumerate(portfolio.accounts):
        id = account.get_id()
        if tasks[index] == 1:   # Invest cash
            print(f'\n{greens[0]}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Investment summary for account: {account.get_name()} ({id}){default}')
            amount_invested = portfolio.invest_balanced(id, additionalCash[index])
            portfolio.print_categories(id)
            portfolio.print_assets(id)
            print(f'\nInvestment total: {format_cents(amount_invested)}')
            print(f'\n{greens[0]}{bold}\\\\**************************************************************************//{default}')
        elif tasks[index] == 2: # Rebalance
            print(f'\n{orange}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Rebalance summary for account: {account.get_name()} ({id}){default}')
            print(f'\n{orange}{bold}\\\\**************************************************************************//{default}')
        elif tasks[index] == 3: # Get summary
            print(f'\n{purple}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Account summary for account: {account.get_name()} ({id}){default}')
            print(f'\n{purple}{bold}\\\\**************************************************************************//{default}')

# -------------------------------------------------------------------------
# The beginning. Does 5 things:
#      1. Asks user which accounts to manage
#      2. Asks user to provide Fidelity CSV file
#      3. Asks user what task to run on each account
#      4. Asks user if they want to include additional cash
#      5. Displays output
# -------------------------------------------------------------------------
def manage_fidelity():
    # Welcome message
    showOpeningMessage()
    # Get information from user
    account_details_list = getAccountsOfInterest()
    tasks = getTasksForAccounts(account_details_list)
    additionalCash = getAdditionalCash(account_details_list)
    csvFile = getFileFromUser()
    # Prepare portfolio
    assets = fidelity_csv_parser.parse(csvFile)
    csvFile.close()
    portfolio = Portfolio(assets, list(ACCOUNTS.values()))
    # Do tasks and display results
    for index, account_details in enumerate(account_details_list):
        if tasks[index] == 1:   # Invest cash
            print(f'\n{greens[0]}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Investment summary for account: {account_details.name} ({account_details.id}){default}')
            amount_invested = portfolio.invest_balanced(account_details, additionalCash[index])
            portfolio.print_categories(account_details)
            portfolio.print_assets(account_details)
            print(f'\nInvestment total: {format_cents(amount_invested)}')
            print(f'\n{greens[0]}{bold}\\\\**************************************************************************//{default}')
        elif tasks[index] == 2: # Rebalance
            print(f'\n{orange}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Rebalance summary for account: {account_details.name} ({account_details.id}){default}')
            print(f'\n{orange}{bold}\\\\**************************************************************************//{default}')
        elif tasks[index] == 3: # Get summary
            print(f'\n{purple}{bold}//**************************************************************************\\\\\n')
            print(f'{blues[1]}Account summary for account: {account_details.name} ({account_details.id}){default}')
            print(f'\n{purple}{bold}\\\\**************************************************************************//{default}')
            
def main(argv=None):
    manage_fidelity()

if __name__ == '__main__':
    main(sys.argv[1:])
