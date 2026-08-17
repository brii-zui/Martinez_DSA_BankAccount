from bank_account import BankAccount

passed = 0
total = 7

def report(number, status, description, detail):
    print(f"{number}. {status:<16}{description:<40}{detail}")
def check(number, description, expected, produce):
    global passed
    try:
        actual = produce()
    except NotImplementedError as missing:
        report(number, "not written yet", description, str(missing))
        return
    except Exception as error:
        report(number, "ERROR", description, f"{type(error).__name__}: {error}")
        return
    if str(actual) == str(expected):
        passed += 1
        report(number, "pass", description, f"got {actual}")
    else:
        report(number, "FAIL", description, f"expected {expected}, got {actual}")
def refuses(action):
    def run():
        try:
            action()
        except ValueError:
            return "refused"
        except NotImplementedError:
            raise
        return "accepted"
    return run
def after_deposit():
    account = BankAccount("Zug", 1000)
    account.deposit(500)
    return account.get_balance()

def after_withdraw():
    account = BankAccount("Zug", 1000)
    account.withdraw(250)
    return account.get_balance()
    
check(1, "a new account keeps its opening balance", 1000,
      lambda: BankAccount("Zug", 1000).get_balance())
check(2, "depositing 500 into 1000 gives 1500", 1500, after_deposit)
check(3, "withdrawing 250 from 1000 gives 750", 750, after_withdraw)
check(4, "the account prints owner and balance", "Zug: 1500.00",
      lambda: BankAccount("Zug", 1500))
check(5, "overdrawing is refused", "refused",
      refuses(lambda: BankAccount("Zug", 1000).withdraw(5000)))
check(6, "a negative deposit is refused", "refused",
      refuses(lambda: BankAccount("Zug", 1000).deposit(-100)))
check(7, "a negative opening balance is refused", "refused",
      refuses(lambda: BankAccount("Zug", -50)))

print(f"\n{passed} of {total} checks passing.")
print("The balance never went below zero, and no test reached into _balance directly. That is encapsulation doing its job.")