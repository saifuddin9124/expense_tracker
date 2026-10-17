from datetime import datetime
import json

def validate_edit_choice(prompt):
    while True:
        try:
            edit_choice = int(input(prompt))
            
            if 1<=edit_choice<= len(dict_expense):
                return edit_choice
            
            print("invalid number! please enter a valid number")
            
        except ValueError:
            print(f"enter a valid number between 1 and {len(dict_expense)} ")
            
def validate_expenses_input(prompt):
    while True:
        try:
            expense_number = int(input(prompt))
            
            if 1<=expense_number<= len(expenses):
                return expense_number
                    
            print("invalid number! please enter a valid number")

        except ValueError:
            print(f"enter a valid number between 1 and {len(expenses)} ")
    
def validate_user_input(prompt):
    while True:
        user_response = input(prompt)

        if user_response.strip() == "":
            print("enter a valid string")
            continue

        return user_response
def validate_amount(prompt):
    while True:
        try:
            user_response = float(input(prompt))
            if user_response <=0:
                print("amount cant be smaller than 0")
                continue
            return user_response
        except ValueError:
            print("Enter a valid number")
def validate_date(prompt):
    while True:
        try:
            user_response = input(prompt)
            if len(user_response) == 6 and user_response.isdigit():
                datetime.strptime(user_response, "%d%m%y")
                return user_response
            else:
                print("enter a valid date")
        except ValueError:
            print("please enter a valid date in DDMMYY format")
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)
try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = []
except json.JSONDecodeError:
    expenses = []
           
exit = False

while not exit:
    choice = input('''PERSONAL EXPENSE TRACKER
    1----add expense
    2----view expenses
    3----get total expenses
    4----exit
    5----delete expense
    6----edit expenses
    \n''')
         
    if choice == '1':
        ex = validate_amount("enter an amount")
        des = validate_user_input("enter a description")
        loc = validate_user_input("enter a location")
        cat = validate_user_input("enter a category")
        dat = validate_date("enter a date")
                
        expense = {
            "amount": ex,
            "description": des,
            "location": loc,
            "category": cat,
            "date": dat
            }
        expenses.append(expense)
        save_expenses()
    elif choice == '2':
        if not expenses:
            print('No recorded expenses')
            
        else:
            print('Recorded expense:')

            for expense in expenses:
                print('Amount:', expense['amount'])
                print('Description:', expense['description'])
                print('Location:', expense['location'])
                print('Category:', expense['category'])
                print('Date:', expense['date'])
                print('=================================')
    elif choice == '3':
            total_expenses = sum(expense['amount'] for expense in expenses)
            print('Total expenses:', total_expenses)
    elif choice == '4':
        exit = True
    elif choice == '5':
        if not expenses:
            print("no recorded expenses")
        else:
            
            for number, expense in enumerate(expenses):
                print(f"{number + 1} ---> {expense['category']}(${expense['amount']})")

            remove_num = validate_expenses_input("enter a value to remove")
            expenses.pop(remove_num-1)
            save_expenses()
            
    elif choice== '6':
        if not expenses:
            print("no recorded expenses")
        else:
            for number, expense in enumerate(expenses):
                print(f"{number + 1} ---> {expense['category']}(${expense['amount']})")
            edit_num = validate_expenses_input("enter an expense to edit")-1
            dict_expense = {
                1 : 'amount',
                2 : 'description',
                3 : 'location',
                4 : 'category',
                5 : 'date'
            }
            print(f"""{expenses[edit_num].items()}
    1---> amount
    2---> description
    3---> location
    4---> category
    5---> date""")
            edit_expense = validate_edit_choice("what do u wish to edit")
            
            if edit_expense == 1:
                new_value = validate_amount('enter the new amount')
                expenses[edit_num][dict_expense[edit_expense]]= new_value
            elif edit_expense == 2:
                new_value = validate_user_input('enter the new description')
                expenses[edit_num][dict_expense[edit_expense]]= new_value
            elif edit_expense == 3:
                new_value = validate_user_input('enter the new location')
                expenses[edit_num][dict_expense[edit_expense]]= new_value
            elif edit_expense == 4:
                new_value = validate_user_input("enter the new category")
                expenses[edit_num][dict_expense[edit_expense]]= new_value
            else:
                new_value = validate_date('enter the new date')
                expenses[edit_num][dict_expense[edit_expense]]= new_value
            save_expenses()
            
            
            

            
    else :
        print('Enter a valid number between 1-6')