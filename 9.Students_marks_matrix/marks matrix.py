# =====================================================================
# CS42 : Student Marks Matrix Analysis
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings, lists, nested lists
# =====================================================================

print("=" * 76)
print("                STUDENT MARKS MATRIX ANALYSIS")
print("=" * 76)

PASS_MARK = 40       # minimum marks to pass a subject
LOW_AVG = 50         # subject average below this is flagged LOW
TOP_RANKS = 3        # report students up to this rank

# ---------------- Matrix size ----------------
text = input("Number of students (1-30) : ")
while not text.isdigit() or int(text) < 1 or int(text) > 30:
    text = input("  Enter a number between 1 and 30 : ")
n = int(text)

text = input("Number of subjects (1-8) : ")
while not text.isdigit() or int(text) < 1 or int(text) > 8:
    text = input("  Enter a number between 1 and 8 : ")
m = int(text)

subjects = input("Subject names (space-separated) : ").split()
while len(subjects) != m:
    subjects = input("  Enter exactly " + str(m) + " names : ").split()

# ---------------- Build the nested list (matrix) ----------------
names = []
marks = []        # nested list: marks[student][subject]
for i in range(n):
    ok = False
    while not ok:
        line = input("Student " + str(i + 1) + " (Name + " + str(m) + " marks) : ")
        parts = line.split()
        ok = False
        if len(parts) == m + 1:
            ok = True
            for t in parts[1:]:
                if not t.isdigit() or int(t) > 100:
                    ok = False
        if not ok:
            print("  Invalid record: need a name and " + str(m) + " marks between 0 and 100.")
    names.append(parts[0])
    row = []
    for t in parts[1:]:
        row.append(int(t))
    marks.append(row)

# ---------------- Row-wise statistics ----------------
totals = []
for i in range(n):
    s = 0
    for j in range(m):
        s += marks[i][j]
    totals.append(s)

# ---------------- Print the matrix ----------------
print("\nMARKS MATRIX")
print("=" * 76)
head = f"{'Student':<10}"
for j in range(m):
    head += f"{subjects[j][0:8]:>9}"
head += f"{'Total':>8}{'Avg':>8}"
print(head)
print("-" * len(head))
for i in range(n):
    line = f"{names[i]:<10}"
    for j in range(m):
        line += f"{marks[i][j]:>9}"
    line += f"{totals[i]:>8}{totals[i] / m:>8.1f}"
    print(line)
print("-" * len(head))

# ---------------- Column-wise statistics ----------------
print("\nSUBJECT-WISE ANALYSIS")
print("=" * 76)
print(f"{'Subject':<12}{'Average':>8}{'Highest':>9}{'Lowest':>8}{'Pass%':>8}  Topper(s)")
print("-" * 76)
low_subjects = []
col_avgs = []
for j in range(m):
    col_sum = 0
    high = marks[0][j]
    low = marks[0][j]
    passed = 0
    for i in range(n):
        v = marks[i][j]
        col_sum += v
        if v > high:
            high = v
        if v < low:
            low = v
        if v >= PASS_MARK:
            passed += 1
    avg = col_sum / n
    col_avgs.append(avg)
    toppers = []
    for i in range(n):
        if marks[i][j] == high:
            toppers.append(names[i])
    note = ""
    if avg < LOW_AVG:
        note = "  << LOW AVERAGE"
        low_subjects.append(subjects[j])
    print(f"{subjects[j]:<12}{avg:>8.1f}{high:>9}{low:>8}{passed * 100 / n:>8.1f}  "
          f"{', '.join(toppers)}{note}")

# ---------------- Ranking (bubble sort on totals, ties share a rank) ----------------
order = []
for i in range(n):
    order.append(i)
for a in range(n - 1):
    for b in range(n - 1 - a):
        if totals[order[b]] < totals[order[b + 1]]:
            order[b], order[b + 1] = order[b + 1], order[b]

rank = [0] * n
for pos in range(n):
    if pos > 0 and totals[order[pos]] == totals[order[pos - 1]]:
        rank[order[pos]] = rank[order[pos - 1]]
    else:
        rank[order[pos]] = pos + 1

print("\nSTUDENT RANKING AND RESULT")
print("=" * 76)
print(f"{'Rank':<6}{'Student':<10}{'Total':>7}{'Percent':>9}  {'Grade':<6}Result")
print("-" * 76)
fail_count = 0
for pos in range(n):
    i = order[pos]
    pct = totals[i] / m
    failed = []
    for j in range(m):
        if marks[i][j] < PASS_MARK:
            failed.append(subjects[j])
    if len(failed) > 0:
        grade = "F"
        result = "FAIL in " + ", ".join(failed)
        fail_count += 1
    else:
        if pct >= 90:
            grade = "O"
        elif pct >= 80:
            grade = "A+"
        elif pct >= 70:
            grade = "A"
        elif pct >= 60:
            grade = "B"
        elif pct >= 50:
            grade = "C"
        else:
            grade = "D"
        result = "PASS"
    print(f"{rank[i]:<6}{names[i]:<10}{totals[i]:>7}{pct:>9.1f}  {grade:<6}{result}")

# ---------------- Highlights ----------------
print("\nHIGHLIGHTS")
print("=" * 76)
top_names = []
for pos in range(n):
    i = order[pos]
    if rank[i] <= TOP_RANKS:
        top_names.append(names[i] + " (rank " + str(rank[i]) + ")")
print("Top performers       : " + ", ".join(top_names))

hard = 0
easy = 0
for j in range(m):
    if col_avgs[j] < col_avgs[hard]:
        hard = j
    if col_avgs[j] > col_avgs[easy]:
        easy = j
print("Toughest subject     : " + subjects[hard] + " (average " + f"{col_avgs[hard]:.1f}" + ")")
print("Best-scoring subject : " + subjects[easy] + " (average " + f"{col_avgs[easy]:.1f}" + ")")
if len(low_subjects) == 0:
    print("Low-average subjects : None (all averages are " + str(LOW_AVG) + " or more)")
else:
    print("Low-average subjects : " + ", ".join(low_subjects))
print("Students failing     : " + str(fail_count) + " of " + str(n))
