# =====================================================================
# CS02 : Progressive Electricity Billing with Anomaly Detection
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings, lists, nested lists, tuples, unpacking
# =====================================================================

print("=" * 80)
print("         PROGRESSIVE ELECTRICITY BILLING AND ANOMALY DETECTION")
print("=" * 80)

# ---------------- Tariff (constants) ----------------
SLABS = [(100, 3.50), (200, 5.00), (400, 6.50)]   # (upper limit in units, Rs/unit)
TOP_RATE = 8.00             # Rs/unit above the last slab limit
SLAB_LABELS = ["1-100", "101-200", "201-400", "Above 400"]
SLAB_RATES = [3.50, 5.00, 6.50, 8.00]
FIXED = 120.00              # fixed monthly charge (Rs.)
DUTY_RATE = 0.05            # electricity duty on energy charge
SURCHARGE_LIMIT = 300       # surcharge applies above this many units
SURCHARGE_RATE = 0.10       # surcharge on energy charge
LIFELINE_LIMIT = 100        # small consumers: units <= this get rebate
LIFELINE_REBATE = 0.10      # 10% rebate on energy charge
ONLINE_REBATE = 25.00       # flat rebate for online payment
UNUSUAL_RISE = 30.0         # bill increase (%) treated as unusual

# ---------------- Input ----------------
consumer = input("Consumer name : ").strip()
text = input("Number of months to analyse (2-12) : ")
while not text.isdigit() or int(text) < 2 or int(text) > 12:
    text = input("  Enter a number between 2 and 12 : ")
months = int(text)
pay = input("Pay online? (y/n) : ").strip().lower()
online = (pay == "y")

month_names = []
units_list = []
bills = []
rows = []        # tuples: (month, units, energy, duty, surcharge, rebate, bill)
details = []     # nested list: units used in each of the 4 slabs, per month

for i in range(months):
    ok = False
    while not ok:
        line = input("Month " + str(i + 1) + " (e.g. Jan 240) : ")
        parts = line.split()
        if len(parts) == 2 and parts[0].isalpha() and parts[1].isdigit():
            ok = True
        else:
            print("  Invalid entry. Use the format: MonthName Units")
    mname = parts[0].capitalize()[0:3]
    units = int(parts[1])

    # ---- progressive slab calculation ----
    used = [0, 0, 0, 0]
    energy = 0.0
    lower = 0
    slab_no = 0
    for upper, rate in SLABS:
        if units > lower:
            if units < upper:
                part = units - lower
            else:
                part = upper - lower
            used[slab_no] = part
            energy += part * rate
        lower = upper
        slab_no += 1
    if units > lower:
        used[3] = units - lower
        energy += used[3] * TOP_RATE

    duty = energy * DUTY_RATE
    surcharge = 0.0
    if units > SURCHARGE_LIMIT:
        surcharge = energy * SURCHARGE_RATE
    rebate = 0.0
    if units <= LIFELINE_LIMIT:
        rebate += energy * LIFELINE_REBATE
    if online:
        rebate += ONLINE_REBATE
    bill = energy + FIXED + duty + surcharge - rebate

    month_names.append(mname)
    units_list.append(units)
    bills.append(bill)
    details.append(used)
    rows.append((mname, units, energy, duty, surcharge, rebate, bill))

# ---------------- Month-wise bill statement ----------------
print("\nCONSUMER : " + consumer)
print("=" * 80)
print(f"{'Month':<6}{'Units':>6}{'Energy':>10}{'Duty':>8}{'Surchg':>9}{'Rebate':>8}"
      f"{'Bill':>10}{'Units%':>8}{'Bill%':>8}  Flag")
print("-" * 80)
unusual_months = []
for i in range(months):
    mname, units, energy, duty, surcharge, rebate, bill = rows[i]
    units_chg = "-"
    bill_chg = "-"
    flag = ""
    if i > 0:
        prev_units = rows[i - 1][1]
        prev_bill = rows[i - 1][6]
        if prev_units > 0:
            units_chg = f"{(units - prev_units) * 100 / prev_units:+.1f}"
        change = (bill - prev_bill) * 100 / prev_bill
        bill_chg = f"{change:+.1f}"
        if change > UNUSUAL_RISE:
            flag = "<< UNUSUAL INCREASE"
            unusual_months.append(mname)
    print(f"{mname:<6}{units:>6}{energy:>10.2f}{duty:>8.2f}{surcharge:>9.2f}"
          f"{rebate:>8.2f}{bill:>10.2f}{units_chg:>8}{bill_chg:>8}  {flag}")
print("-" * 80)

# ---------------- Statistics ----------------
total_bill = 0.0
total_units = 0
high = 0
low = 0
for i in range(months):
    total_bill += bills[i]
    total_units += units_list[i]
    if bills[i] > bills[high]:
        high = i
    if bills[i] < bills[low]:
        low = i

print("Total units consumed : " + str(total_units))
print("Total amount payable : Rs. " + f"{total_bill:.2f}")
print("Average monthly bill : Rs. " + f"{total_bill / months:.2f}")
print("Highest bill         : " + month_names[high] + "  Rs. " + f"{bills[high]:.2f}")
print("Lowest bill          : " + month_names[low] + "  Rs. " + f"{bills[low]:.2f}")

if len(unusual_months) == 0:
    print("Unusual increases    : None (no month rose by more than "
          + str(int(UNUSUAL_RISE)) + "%)")
else:
    print("Unusual increases    : " + ", ".join(unusual_months) +
          " (bill rose by more than " + str(int(UNUSUAL_RISE)) + "%)")

# ---------------- Slab breakdown of the highest bill ----------------
print("\nSLAB BREAKDOWN OF HIGHEST BILL (" + month_names[high] + ")")
print("-" * 50)
for s in range(4):
    u = details[high][s]
    print(f"{SLAB_LABELS[s]:<12}{u:>5} units x Rs.{SLAB_RATES[s]:.2f} = Rs.{u * SLAB_RATES[s]:>9.2f}")
