# =====================================================================
# CS06 : Railway Fare and Reservation Calculator (with cancellation)
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings, lists, tuples, unpacking
# =====================================================================

print("=" * 72)
print("          RAILWAY FARE, RESERVATION AND CANCELLATION SYSTEM")
print("=" * 72)

# ---------------- Fare tables (parallel lists, same index = same class) ----------------
CODES = ["SL", "3A", "2A", "1A"]
NAMES = ["Sleeper", "AC 3-Tier", "AC 2-Tier", "AC First"]
RATE = [0.55, 1.35, 1.95, 3.30]         # Rs per km (base)
MIN_FARE = [120, 330, 480, 800]         # minimum basic fare (Rs.)
RESERVE = [20, 40, 50, 60]              # reservation fee per passenger (Rs.)
CLEARANCE = [120, 180, 200, 240]        # cancellation clearance charge (Rs.)
GST = [0.0, 0.05, 0.05, 0.05]           # GST on basic fare
SLABS = [(200, 1.0), (500, 0.9), (1000, 0.8)]   # (upper km, weight of each km)
LONG_WEIGHT = 0.7                       # weight for km beyond 1000
MAX_PASSENGERS = 6

# ---------------- Journey details ----------------
train = input("Train name : ").strip()

text = input("Distance in km (1-3500) : ")
while not text.isdigit() or int(text) < 1 or int(text) > 3500:
    text = input("  Invalid distance. Enter 1-3500 : ")
distance = int(text)

idx = -1
while idx == -1:
    code = input("Travel class (SL / 3A / 2A / 1A) : ").strip().upper()
    for k in range(len(CODES)):
        if CODES[k] == code:
            idx = k
    if idx == -1:
        print("  Invalid class. Choose from SL, 3A, 2A, 1A.")

text = input("Number of passengers (1-" + str(MAX_PASSENGERS) + ") : ")
while not text.isdigit() or int(text) < 1 or int(text) > MAX_PASSENGERS:
    text = input("  Enter a number between 1 and " + str(MAX_PASSENGERS) + " : ")
count = int(text)

# ---------------- Passenger details ----------------
people = []     # tuples: (name, age, gender, category, concession_percent)
for p in range(count):
    ok = False
    while not ok:
        line = input("Passenger " + str(p + 1) + " (name,age,M/F) : ")
        parts = line.split(",")
        if len(parts) == 3:
            pname = parts[0].strip()
            page = parts[1].strip()
            pg = parts[2].strip().upper()
            if pname != "" and page.isdigit() and int(page) <= 120 and (pg == "M" or pg == "F"):
                ok = True
        if not ok:
            print("  Invalid passenger details. Please re-enter.")
    age = int(page)
    if age < 5:
        category = "Infant"
        concession = 100
    elif age <= 11:
        category = "Child"
        concession = 50
    elif pg == "M" and age >= 60:
        category = "Senior"
        concession = 40
    elif pg == "F" and age >= 58:
        category = "Senior"
        concession = 50
    else:
        category = "Adult"
        concession = 0
    people.append((pname, age, pg, category, concession))

# ---------------- Infants cannot travel alone ----------------
has_ticketed = False
for person in people:
    if person[3] != "Infant":
        has_ticketed = True

if not has_ticketed:
    print("\nBOOKING REJECTED : infants (below 5 years) cannot travel without an")
    print("accompanying passenger who holds a ticket.")
else:
    # ---------------- Basic fare using distance slabs ----------------
    eff = 0.0
    lower = 0
    for upper, weight in SLABS:
        if distance > lower:
            if distance < upper:
                seg = distance - lower
            else:
                seg = upper - lower
            eff += seg * weight
        lower = upper
    if distance > lower:
        eff += (distance - lower) * LONG_WEIGHT

    base = eff * RATE[idx]
    if base < MIN_FARE[idx]:
        base = MIN_FARE[idx]
    base = round(base, 2)

    # ---------------- Ticket ----------------
    print("\n" + "=" * 72)
    print("TICKET : " + train + "   |   " + str(distance) + " km   |   " + NAMES[idx])
    print("Full basic fare for one adult : Rs. " + f"{base:.2f}")
    print("=" * 72)
    print(f"{'Passenger':<12}{'Age':>4} {'Category':<8}{'Concn':>6}{'Fare':>9}"
          f"{'Reserve':>9}{'GST':>7}{'Total':>10}")
    print("-" * 72)

    tickets = []    # tuples: (name, category, fare, reserve, gst, total)
    grand = 0.0
    for person in people:
        pname, age, pg, category, concession = person
        fare = round(base * (100 - concession) / 100, 2)
        if category == "Infant":
            reserve = 0
        else:
            reserve = RESERVE[idx]
        gst = round(fare * GST[idx], 2)
        total = fare + reserve + gst
        grand += total
        tickets.append((pname, category, fare, reserve, gst, total))
        print(f"{pname:<12}{age:>4} {category:<8}{str(concession) + '%':>6}{fare:>9.2f}"
              f"{reserve:>9.2f}{gst:>7.2f}{total:>10.2f}")
    print("-" * 72)
    print(f"{'TOTAL AMOUNT PAYABLE':<48}{'Rs.':>6}{grand:>18.2f}")

    # ---------------- Cancellation ----------------
    choice = input("\nCancel this ticket? (y/n) : ").strip().lower()
    if choice == "y":
        text = input("Hours remaining before departure : ")
        while not text.isdigit():
            text = input("  Enter a whole number of hours : ")
        hours = int(text)

        if hours > 48:
            rule = "More than 48 h : flat clearance charge"
        elif hours > 12:
            rule = "12-48 h : 25% of fare (minimum clearance charge)"
        elif hours > 4:
            rule = "4-12 h : 50% of fare (minimum clearance charge)"
        else:
            rule = "Less than 4 h : NO refund"
        print("\nCANCELLATION RULE APPLIED : " + rule)
        print("-" * 72)
        print(f"{'Passenger':<12}{'Fare paid':>11}{'Deduction':>12}{'Refund':>10}")

        refund_total = 0.0
        for t in tickets:
            tname, tcat, fare, reserve, gst, total = t
            if tcat == "Infant":
                ded = 0.0
            elif hours > 48:
                ded = CLEARANCE[idx]
            elif hours > 12:
                ded = fare * 0.25
                if ded < CLEARANCE[idx]:
                    ded = CLEARANCE[idx]
            elif hours > 4:
                ded = fare * 0.50
                if ded < CLEARANCE[idx]:
                    ded = CLEARANCE[idx]
            else:
                ded = fare
            if ded > fare:
                ded = fare
            refund = fare - ded
            refund_total += refund
            print(f"{tname:<12}{fare:>11.2f}{ded:>12.2f}{refund:>10.2f}")
        print("-" * 72)
        print("Reservation fee and GST are non-refundable.")
        print("TOTAL REFUND : Rs. " + f"{refund_total:.2f}")
        print("AMOUNT RETAINED : Rs. " + f"{grand - refund_total:.2f}")
    else:
        print("Ticket confirmed. Have a safe journey!")
