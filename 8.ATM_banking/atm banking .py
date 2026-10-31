# =====================================================================
# CS38 : ATM Menu-Driven Banking Simulation
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings, lists, tuples, unpacking, slicing
# =====================================================================

print("=" * 60)
print("              SMART ATM BANKING SIMULATOR")
print("=" * 60)

# ---------------- Account rules (constants) ----------------
PIN = "4321"
ATTEMPTS = 3
OPENING_BALANCE = 25000
DAILY_LIMIT = 25000        # maximum total withdrawals in a day
TXN_LIMIT = 10000          # maximum per withdrawal
MIN_BALANCE = 1000         # balance that must remain in the account
MAX_DEPOSIT = 50000        # maximum per deposit
MAX_WITHDRAWALS = 4        # maximum withdrawals in a day
UNIT = 100                 # amounts must be multiples of this

balance = OPENING_BALANCE
withdrawn_today = 0
withdraw_count = 0
txns = []      # tuples: (no, type, amount, status, reason, balance_after)

# ---------------- PIN verification ----------------
authenticated = False
tries = 0
while tries < ATTEMPTS and not authenticated:
    entered = input("Enter 4-digit PIN : ")
    if entered == PIN:
        authenticated = True
    else:
        tries += 1
        print("Incorrect PIN. Attempts left : " + str(ATTEMPTS - tries))

if not authenticated:
    print("\nCard BLOCKED after " + str(ATTEMPTS) + " wrong attempts. Please contact your bank.")
else:
    print("PIN accepted. Welcome!")
    running = True
    while running:
        print("\n------------ MENU ------------")
        print(" 1. Deposit")
        print(" 2. Withdraw")
        print(" 3. Balance enquiry")
        print(" 4. Mini statement (last 5)")
        print(" 5. Transaction summary")
        print(" 0. Exit")
        choice = input("Select option : ").strip()

        # ================= 1. DEPOSIT =================
        if choice == "1":
            text = input("Deposit amount : ").strip()
            reason = "-"
            amount = 0
            if not text.isdigit():
                reason = "Invalid amount (digits only)"
            else:
                amount = int(text)
                if amount == 0:
                    reason = "Amount must be greater than zero"
                elif amount % UNIT != 0:
                    reason = "Amount must be a multiple of " + str(UNIT)
                elif amount > MAX_DEPOSIT:
                    reason = "Exceeds deposit limit of Rs." + str(MAX_DEPOSIT)
            if reason == "-":
                balance += amount
                txns.append((len(txns) + 1, "DEPOSIT", amount, "SUCCESS", "-", balance))
                print("Deposited Rs." + str(amount) + ". New balance : Rs." + str(balance))
            else:
                txns.append((len(txns) + 1, "DEPOSIT", amount, "REJECTED", reason, balance))
                print("Deposit rejected : " + reason)

        # ================= 2. WITHDRAW =================
        elif choice == "2":
            text = input("Withdrawal amount : ").strip()
            reason = "-"
            amount = 0
            if not text.isdigit():
                reason = "Invalid amount (digits only)"
            else:
                amount = int(text)
                if amount == 0:
                    reason = "Amount must be greater than zero"
                elif amount % UNIT != 0:
                    reason = "Amount must be a multiple of " + str(UNIT)
                elif amount > TXN_LIMIT:
                    reason = "Exceeds per-transaction limit of Rs." + str(TXN_LIMIT)
                elif withdraw_count >= MAX_WITHDRAWALS:
                    reason = "Daily limit of " + str(MAX_WITHDRAWALS) + " withdrawals reached"
                elif withdrawn_today + amount > DAILY_LIMIT:
                    reason = "Exceeds daily limit of Rs." + str(DAILY_LIMIT)
                elif balance - amount < MIN_BALANCE:
                    reason = "Insufficient balance (minimum Rs." + str(MIN_BALANCE) + " must remain)"
            if reason == "-":
                balance -= amount
                withdrawn_today += amount
                withdraw_count += 1
                txns.append((len(txns) + 1, "WITHDRAW", amount, "SUCCESS", "-", balance))
                print("Please collect Rs." + str(amount) + ". New balance : Rs." + str(balance))
            else:
                txns.append((len(txns) + 1, "WITHDRAW", amount, "REJECTED", reason, balance))
                print("Withdrawal rejected : " + reason)

        # ================= 3. BALANCE ENQUIRY =================
        elif choice == "3":
            txns.append((len(txns) + 1, "BALANCE", 0, "SUCCESS", "-", balance))
            print("Available balance : Rs." + str(balance))

        # ================= 4. MINI STATEMENT =================
        elif choice == "4":
            if len(txns) == 0:
                print("No transactions yet.")
            else:
                last = txns[-5:]       # slicing: the five most recent records
                print(f"{'No':<4}{'Type':<10}{'Amount':>8}  {'Status':<9}{'Balance':>9}")
                print("-" * 44)
                for t in last:
                    no, kind, amt, status, why, bal = t
                    print(f"{no:<4}{kind:<10}{amt:>8}  {status:<9}{bal:>9}")

        # ================= 5. TRANSACTION SUMMARY =================
        elif choice == "5":
            dep_total = 0
            wd_total = 0
            dep_n = 0
            wd_n = 0
            bal_n = 0
            rej_n = 0
            for t in txns:
                no, kind, amt, status, why, bal = t
                if status == "REJECTED":
                    rej_n += 1
                elif kind == "DEPOSIT":
                    dep_n += 1
                    dep_total += amt
                elif kind == "WITHDRAW":
                    wd_n += 1
                    wd_total += amt
                else:
                    bal_n += 1
            print("\n----------- TRANSACTION SUMMARY -----------")
            print("Opening balance       : Rs." + str(OPENING_BALANCE))
            print("Deposits  (" + str(dep_n) + ")         : Rs." + str(dep_total))
            print("Withdrawals (" + str(wd_n) + ")       : Rs." + str(wd_total))
            print("Balance enquiries     : " + str(bal_n))
            print("Rejected transactions : " + str(rej_n))
            print("Closing balance       : Rs." + str(balance))
            print("Withdrawn today       : Rs." + str(withdrawn_today) + " of Rs." + str(DAILY_LIMIT))
            if rej_n > 0:
                print("Rejection details:")
                for t in txns:
                    if t[3] == "REJECTED":
                        print("  #" + str(t[0]) + " " + t[1] + " " + str(t[2]) + " -> " + t[4])

        # ================= 0. EXIT =================
        elif choice == "0":
            print("\nThank you for banking with us. Final balance : Rs." + str(balance))
            running = False

        else:
            print("Invalid option. Please choose 0-5.")
