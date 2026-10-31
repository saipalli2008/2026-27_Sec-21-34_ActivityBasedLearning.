 =====================================================================
# CS01 : University Scholarship Allocation
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, lists, tuples,
#                 tuple comparison and unpacking
# =====================================================================

print("=" * 70)
print("            UNIVERSITY SCHOLARSHIP ALLOCATION SYSTEM")
print("=" * 70)

# ---------------- Scholarship policy (constants) ----------------
MIN_PERCENT = 75.0      # minimum aggregate percentage
MIN_SUBJECT = 50        # minimum marks required in EVERY subject
MIN_ATTENDANCE = 80     # minimum attendance percentage
MAX_INCOME = 600000     # maximum annual family income (Rs.)
SUBJECTS = 5            # number of subjects per applicant
FULL_MARKS = 100        # maximum marks per subject

# ---------------- Read number of applicants and quota ----------------
text = input("Number of applicants : ")
while not text.isdigit() or int(text) == 0:
    text = input("  Enter a positive whole number : ")
n = int(text)

text = input("Scholarships available (quota) : ")
while not text.isdigit() or int(text) == 0:
    text = input("  Enter a positive whole number : ")
quota = int(text)

print("\nRecord format : ID,Name,m1 m2 m3 m4 m5,Attendance,Income")

eligible = []   # tuples: (key, id, name, marks, total, attendance, income)
rejected = []   # tuples: (id, [reasons])
seen_ids = []

# ---------------- Read and evaluate every applicant ----------------
for i in range(n):
    line = input("Applicant " + str(i + 1) + " : ")
    parts = line.split(",")
    if len(parts) != 5:
        rejected.append(("Record " + str(i + 1),
                         ["Malformed record: 5 comma-separated fields required"]))
    else:
        sid = parts[0].strip()
        name = parts[1].strip()
        mark_text = parts[2].split()
        att_text = parts[3].strip()
        inc_text = parts[4].strip()

        valid = True
        marks = []
        if len(mark_text) != SUBJECTS:
            valid = False
        else:
            for t in mark_text:
                if t.isdigit() and int(t) <= FULL_MARKS:
                    marks.append(int(t))
                else:
                    valid = False
        if not att_text.isdigit() or int(att_text) > 100:
            valid = False
        if not inc_text.isdigit():
            valid = False
        if sid == "" or name == "":
            valid = False

        if not valid:
            label = sid
            if label == "":
                label = "Record " + str(i + 1)
            rejected.append((label, ["Invalid or missing data in the record"]))
        elif sid in seen_ids:
            rejected.append((sid, ["Duplicate application ID"]))
        else:
            seen_ids.append(sid)
            attendance = int(att_text)
            income = int(inc_text)

            total = 0
            for m in marks:
                total += m
            percent = total * 100 / (SUBJECTS * FULL_MARKS)

            reasons = []
            if percent < MIN_PERCENT:
                reasons.append("Aggregate " + str(round(percent, 2)) +
                               "% is below " + str(MIN_PERCENT) + "%")
            for s in range(SUBJECTS):
                if marks[s] < MIN_SUBJECT:
                    reasons.append("Subject " + str(s + 1) + " marks " +
                                   str(marks[s]) + " are below " + str(MIN_SUBJECT))
            if attendance < MIN_ATTENDANCE:
                reasons.append("Attendance " + str(attendance) +
                               "% is below " + str(MIN_ATTENDANCE) + "%")
            if income > MAX_INCOME:
                reasons.append("Income Rs." + str(income) +
                               " exceeds Rs." + str(MAX_INCOME))

            if len(reasons) == 0:
                # ranking key: higher total, higher Subject-1 marks,
                # higher attendance, LOWER income (negated so bigger = better)
                key = (total, marks[0], attendance, 0 - income)
                eligible.append((key, sid, name, marks, total, attendance, income))
            else:
                rejected.append((sid, reasons))

# ---------------- Rank eligible students (bubble sort on tuple keys) ----------------
count = len(eligible)
for i in range(count - 1):
    for j in range(count - 1 - i):
        k1 = eligible[j][0]
        k2 = eligible[j + 1][0]
        # tuples compare element by element; final tie-break: smaller ID first
        if k1 < k2 or (k1 == k2 and eligible[j][1] > eligible[j + 1][1]):
            eligible[j], eligible[j + 1] = eligible[j + 1], eligible[j]

# ---------------- Report ----------------
print("\n" + "=" * 70)
print("RANKED LIST OF ELIGIBLE STUDENTS   (quota = " + str(quota) + ")")
print("=" * 70)
if count == 0:
    print("No applicant satisfies all scholarship conditions.")
else:
    print(f"{'Rank':<5}{'ID':<7}{'Name':<15}{'Total':>6}{'%':>7}{'Att':>5}"
          f"{'Income':>9}  {'Result':<9}Tie-break")
    print("-" * 70)
    for r in range(count):
        key, sid, name, marks, total, att, inc = eligible[r]
        percent = total * 100 / (SUBJECTS * FULL_MARKS)
        tie = "-"
        if r > 0:
            pkey, psid, pname, pmarks, ptotal, patt, pinc = eligible[r - 1]
            if total == ptotal:
                if marks[0] != pmarks[0]:
                    tie = "Subject-1 marks"
                elif att != patt:
                    tie = "Attendance"
                elif inc != pinc:
                    tie = "Lower income"
                else:
                    tie = "Smaller ID"
        if r < quota:
            result = "AWARDED"
        else:
            result = "WAITLIST"
        print(f"{r + 1:<5}{sid:<7}{name:<15}{total:>6}{percent:>7.1f}{att:>5}"
              f"{inc:>9}  {result:<9}{tie}")

print("\n" + "=" * 70)
print("REJECTED APPLICATIONS")
print("=" * 70)
if len(rejected) == 0:
    print("None")
else:
    for item in rejected:
        rid, why = item
        print(rid + " :")
        for w in why:
            print("   - " + w)

awarded = count
if count > quota:
    awarded = quota
print("\nSUMMARY : applicants = " + str(n) + ", eligible = " + str(count) +
      ", rejected = " + str(len(rejected)) + ", scholarships awarded = " + str(awarded))
