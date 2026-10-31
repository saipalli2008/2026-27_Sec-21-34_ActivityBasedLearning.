# =====================================================================
# CS37 : Nested Loop Calendar Generator
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, nested loops, strings, lists, pattern generation
# =====================================================================

print("=" * 50)
print("          MONTHLY CALENDAR GENERATOR")
print("=" * 50)

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DAYS_IN = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ---------------- Input with validation ----------------
text = input("Year (1900-2100) : ").strip()
while not text.isdigit() or int(text) < 1900 or int(text) > 2100:
    text = input("  Invalid year. Enter a year between 1900 and 2100 : ").strip()
year = int(text)

text = input("Month number (1-12) : ").strip()
while not text.isdigit() or int(text) < 1 or int(text) > 12:
    text = input("  Invalid month. Enter 1-12 : ").strip()
month = int(text)

start = -1
while start == -1:
    wd = input("Weekday of the 1st (Mon/Tue/Wed/Thu/Fri/Sat/Sun) : ").strip().capitalize()[0:3]
    for k in range(7):
        if WEEKDAYS[k] == wd:
            start = k
    if start == -1:
        print("  Invalid weekday. Use names such as Mon, Tue, Wed ...")

# ---------------- Month length with leap-year rule ----------------
leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
days = DAYS_IN[month - 1]
if month == 2 and leap:
    days = 29

# ---------------- Optional holiday dates ----------------
raw = input("Holiday dates, comma-separated (blank for none) : ")
holidays = []
if raw.strip() != "":
    for token in raw.split(","):
        t = token.strip()
        if t.isdigit() and 1 <= int(t) <= days:
            if int(t) not in holidays:
                holidays.append(int(t))
        else:
            print("  Ignored invalid holiday date '" + t + "'")

# ---------------- Print the calendar ----------------
title = MONTHS[month - 1] + " " + str(year)
print()
print(title.center(28))
print("-" * 28)
header = ""
for name in WEEKDAYS:
    header += f"{name:<4}"
print(header.rstrip())

day = 1 - start           # number in the first cell (zero/negative = blank cell)
weeks = 0
while day <= days:        # one pass of the while loop = one week row
    line = ""
    for col in range(7):  # nested loop = seven columns of the week
        if day < 1 or day > days:
            line += "    "
        else:
            mark = " "
            if day in holidays:
                mark = "*"
            line += f"{day:>2}{mark} "
        day += 1
    print(line.rstrip())
    weeks += 1
print("-" * 28)
if len(holidays) > 0:
    print("* = holiday")

# ---------------- Summary ----------------
weekend = 0
for d in range(1, days + 1):
    if (start + d - 1) % 7 >= 5:
        weekend += 1
holiday_on_weekday = 0
for h in holidays:
    if (start + h - 1) % 7 < 5:
        holiday_on_weekday += 1
working = days - weekend - holiday_on_weekday

leap_note = ""
if month == 2 and leap:
    leap_note = " (leap year)"
print("\nDays in month        : " + str(days) + leap_note)
print("Weeks shown          : " + str(weeks))
print("Month ends on        : " + WEEKDAYS[(start + days - 1) % 7])
print("Weekend days (Sat/Sun): " + str(weekend))
print("Holidays on weekdays : " + str(holiday_on_weekday))
print("Working days         : " + str(working))
