# =====================================================================
# CS29 : Password Policy Validation Engine
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings (indexing, slicing, methods), lists
# =====================================================================

print("=" * 66)
print("            PASSWORD POLICY VALIDATION ENGINE")
print("=" * 66)

# ---------------- Policy (constants) ----------------
MIN_LEN = 10
MAX_LEN = 32
SPECIALS = "!@#$%^&*()-_+="
PROHIBITED = ["password", "admin", "qwerty", "welcome", "college", "letmein"]
RULE_TITLES = ["Length", "Uppercase letter", "Lowercase letter", "Digit",
               "Special character", "No spaces", "No repeated characters",
               "No ascending sequence", "No prohibited words", "No username"]

username = input("Username (password must not contain it) : ").strip().lower()
text = input("How many passwords to test : ")
while not text.isdigit() or int(text) == 0:
    text = input("  Enter a positive whole number : ")
n = int(text)

accepted = 0
weak = 0
rejected = 0
rule_fail_count = [0] * 10     # how many passwords failed each rule

for i in range(n):
    pw = input("\nPassword " + str(i + 1) + " : ")
    lw = pw.lower()
    size = len(pw)
    failures = []              # explanation of every failed rule
    failed_rules = []          # rule numbers that failed

    # R1 : length
    if size < MIN_LEN:
        failures.append("R1 Length is " + str(size) + "; at least " + str(MIN_LEN) +
                        " characters are required")
        failed_rules.append(0)
    elif size > MAX_LEN:
        failures.append("R1 Length is " + str(size) + "; at most " + str(MAX_LEN) +
                        " characters are allowed")
        failed_rules.append(0)

    # R2-R6 : character categories
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    has_space = False
    for ch in pw:
        if ch.isupper():
            has_upper = True
        elif ch.islower():
            has_lower = True
        elif ch.isdigit():
            has_digit = True
        elif ch == " ":
            has_space = True
        elif ch in SPECIALS:
            has_special = True
    if not has_upper:
        failures.append("R2 No uppercase letter (A-Z) found")
        failed_rules.append(1)
    if not has_lower:
        failures.append("R3 No lowercase letter (a-z) found")
        failed_rules.append(2)
    if not has_digit:
        failures.append("R4 No digit (0-9) found")
        failed_rules.append(3)
    if not has_special:
        failures.append("R5 No special character from " + SPECIALS + " found")
        failed_rules.append(4)
    if has_space:
        failures.append("R6 Password must not contain spaces")
        failed_rules.append(5)

    # R7 : same character three or more times in a row / R8 : ascending run of 4+
    run = 1
    arun = 1
    repeated = ""
    sequence = ""
    for k in range(1, size):
        if pw[k] == pw[k - 1]:
            run += 1
        else:
            run = 1
        if run >= 3 and repeated == "":
            repeated = pw[k] * 3

        if lw[k].isalnum() and lw[k - 1].isalnum() and ord(lw[k]) == ord(lw[k - 1]) + 1:
            arun += 1
        else:
            arun = 1
        if arun >= 4 and sequence == "":
            sequence = lw[k - 3:k + 1]
    if repeated != "":
        failures.append("R7 Same character repeated 3+ times in a row ('" + repeated + "')")
        failed_rules.append(6)
    if sequence != "":
        failures.append("R8 Ascending sequence of 4+ characters found ('" + sequence + "')")
        failed_rules.append(7)

    # R9 : prohibited words
    found = []
    for word in PROHIBITED:
        if word in lw:
            found.append(word)
    if len(found) > 0:
        failures.append("R9 Contains prohibited word(s): " + ", ".join(found))
        failed_rules.append(8)

    # R10 : username
    if len(username) >= 3 and username in lw:
        failures.append("R10 Password contains the username '" + username + "'")
        failed_rules.append(9)

    # ---------------- Verdict ----------------
    bad = len(failures)
    score = (10 - bad) * 10
    if bad == 0:
        verdict = "ACCEPTED (Strong)"
        accepted += 1
    elif bad <= 2:
        verdict = "WEAK - fix the listed problems"
        weak += 1
    else:
        verdict = "REJECTED (Very weak)"
        rejected += 1

    print("  Score   : " + str(score) + "/100   (" + str(10 - bad) + " of 10 rules passed)")
    print("  Verdict : " + verdict)
    for f in failures:
        print("    [FAIL] " + f)
    for r in failed_rules:
        rule_fail_count[r] += 1

# ---------------- Summary ----------------
print("\n" + "=" * 66)
print("SUMMARY : tested = " + str(n) + ", accepted = " + str(accepted) +
      ", weak = " + str(weak) + ", rejected = " + str(rejected))
worst = 0
for r in range(10):
    if rule_fail_count[r] > rule_fail_count[worst]:
        worst = r
if rule_fail_count[worst] == 0:
    print("Every password satisfied every rule.")
else:
    print("Most frequently failed rule : R" + str(worst + 1) + " " + RULE_TITLES[worst] +
          " (" + str(rule_fail_count[worst]) + " password(s))")
