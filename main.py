import random
ROWS=3
COLS=3
#these are the global constants decleared to use in functions in entire program
MAX_LINES=3
MAX_BET=1000
MIN_BET=10
symbol_count={
    "A" : 2,
    "B" : 4,
    "C" : 6,
    "D" : 8   
}
symbol_value={
    "A" : 5,
    "B" : 4,
    "C" : 3,
    "D" : 2
}

def check_winnings(columns, lines, bet, values):
    winnings=0
    winning_lines=[]
    for line in range(lines):
        symbol=columns[0][line]
        for column in columns:
            symbol_to_check=column[line]
            if symbol != symbol_to_check:
                break
        else :
            winnings+=values[symbol] * bet
            winning_lines.append(line+1)
    return winnings, winning_lines
def get_slot_machine_spin(rows,cols,symbols):
    all_symbols=[]
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
    columns=[]
    for _ in range(cols):
        column = []
        current_symbols=all_symbols[:]
        
        for _ in range(rows):
            value=random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i !=len(columns)-1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="") 
        print()
#the user have to deposit amount if want to play
def deposit():
    while True :
        #amount have to be number and greater than 0 otherwise user cant play
        amount=input("HOW MUCH WOULD YOU LIKE TO DEPOSIT? $")
        if amount.isdigit():
            amount=int(amount)
            if amount > 0 :
                break
            else :
                print("AMOUNT HAVE TO BE GREATER THAN 0.")
        else :
            print("PLEASE ENTER A NUMBER")
    return amount
def get_no_of_lines():
    #we can change the max lines in the top accordingly 
    while True :
        lines=input("ENTER THE NUMBER OF LINES TO BET ON (1-"+ str(MAX_LINES)+")?")
        if lines.isdigit():
            lines=int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else :
                print("ENTER A VALID NUMBER OF LINES")
        else :
            print("PLEASE ENTER A NUMBER")
    return lines
def get_bet():
    #we can change the max bet and min bet in the top accordingly 
    #we have to get the amount how much we want to bet , otherwise we will get an error
    while True :
        amount=input("WHAT WOULD LIKE TO BET ON EACH LINE ? $")
        if amount.isdigit():
            amount=int(amount)
            if MIN_BET <=amount<= MAX_BET :
                break
            else :
                print(f"AMOUNT MUST BE BETWEEN ${MIN_BET} - ${MAX_BET}")
        else :
            print("")
    return amount
def spin(balance):
    lines=get_no_of_lines()
    while True :
        bet=get_bet()
        total_bet = bet * lines
        if total_bet > balance :
            print(f"you do not have enough amount to bet on, your current balance is ${balance}")
        else:
            break
    print(f"you are betting ${bet} on {lines} lines. total bet is equal to : ${total_bet}")
    
    slots=get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines=check_winnings(slots, lines, bet, symbol_value)
    print(f"you won ${winnings}")
    print(f"you won on lines :", *winning_lines)
    if winning_lines == 0 :
        return 0
    return winnings - total_bet

def main():
    balance=deposit()
    while True:
        print(f"current balance is ${balance}")
        answer=input("press enter to play (q to quit)")
        if answer == "q":
            break
        balance +=spin(balance)
    print(f"you left with ${balance}")      
    
if __name__ == "__main__":
    main()
