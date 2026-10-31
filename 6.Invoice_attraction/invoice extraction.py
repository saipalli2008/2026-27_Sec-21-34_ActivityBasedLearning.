# =====================================================================
# CS32 : Text-Based Invoice Data Extraction
# Syllabus used : variables, data types, operators, conditionals,
#                 loops, strings (slicing, split, find, count,
#                 isdigit, isalpha, isupper), lists, tuples, unpacking
# =====================================================================

print("=" * 72)
print("           TEXT-BASED INVOICE DATA EXTRACTION")
print("=" * 72)
print("Record format : INV-YYYY-NNN|PRD:AA999|QTY:n|AMT:0000.00")

text = input("Number of invoice records : ")
while not text.isdigit() or int(text) == 0:
    text = input("  Enter a positive whole number : ")
n = int(text)

valid_records = []     # tuples: (invoice, product, qty, amount)
error_log = []         # tuples: (record_no, text, [errors])
seen_invoices = []
codes = []             # product-wise totals kept in parallel lists
code_qty = []
code_amt = []

for i in range(n):
    rec = input("Record " + str(i + 1) + " : ").strip()
    errors = []

    if rec.count("|") != 3:
        errors.append("Expected 4 fields separated by 3 '|' symbols (found " +
                      str(rec.count("|") + 1) + " field(s))")
    else:
        inv, prd, qty, amt = rec.split("|")        # tuple-style unpacking
        inv = inv.strip()
        prd = prd.strip()
        qty = qty.strip()
        amt = amt.strip()
        code = ""
        q = 0
        a = 0.0

        # ---- invoice number : INV-YYYY-NNN ----
        if (len(inv) != 12 or inv[0:4] != "INV-" or inv[8] != "-"
                or not inv[4:8].isdigit() or not inv[9:12].isdigit()):
            errors.append("Invoice number '" + inv + "' must look like INV-2026-014")
        elif inv in seen_invoices:
            errors.append("Duplicate invoice number " + inv)

        # ---- product code : PRD:AA999 ----
        if prd[0:4] != "PRD:":
            errors.append("Product field must start with 'PRD:'")
        else:
            code = prd[4:]
            if (len(code) != 5 or not code[0:2].isalpha() or not code[0:2].isupper()
                    or not code[2:5].isdigit()):
                errors.append("Product code '" + code + "' must be 2 capital letters + 3 digits")
                code = ""

        # ---- quantity : QTY:1..999 ----
        if qty[0:4] != "QTY:":
            errors.append("Quantity field must start with 'QTY:'")
        else:
            qt = qty[4:]
            if not qt.isdigit():
                errors.append("Quantity '" + qt + "' is not a whole number")
            elif int(qt) < 1 or int(qt) > 999:
                errors.append("Quantity " + qt + " is outside the range 1-999")
            else:
                q = int(qt)

        # ---- amount : AMT:digits.dd ----
        if amt[0:4] != "AMT:":
            errors.append("Amount field must start with 'AMT:'")
        else:
            at = amt[4:]
            pieces = at.split(".")
            if (len(pieces) != 2 or not pieces[0].isdigit() or not pieces[1].isdigit()
                    or len(pieces[1]) != 2):
                errors.append("Amount '" + at + "' must have exactly two decimal places")
            else:
                a = float(at)
                if a <= 0:
                    errors.append("Amount must be greater than zero")

        if len(errors) == 0:
            seen_invoices.append(inv)
            valid_records.append((inv, code, q, a))
            pos = -1
            for k in range(len(codes)):
                if codes[k] == code:
                    pos = k
            if pos == -1:
                codes.append(code)
                code_qty.append(q)
                code_amt.append(a)
            else:
                code_qty[pos] += q
                code_amt[pos] += a

    if len(errors) > 0:
        error_log.append((i + 1, rec, errors))

# ---------------- Report ----------------
print("\n" + "=" * 72)
print("EXTRACTED VALID RECORDS")
print("=" * 72)
if len(valid_records) == 0:
    print("No valid records found.")
else:
    print(f"{'Invoice':<14}{'Product':<10}{'Qty':>6}{'Amount':>12}")
    print("-" * 42)
    total_qty = 0
    total_amt = 0.0
    for rec in valid_records:
        inv, code, q, a = rec
        total_qty += q
        total_amt += a
        print(f"{inv:<14}{code:<10}{q:>6}{a:>12.2f}")
    print("-" * 42)
    print(f"{'TOTAL':<24}{total_qty:>6}{total_amt:>12.2f}")

    print("\nPRODUCT-WISE TOTALS")
    print("-" * 42)
    best = 0
    for k in range(len(codes)):
        print(f"{codes[k]:<14}{'':<10}{code_qty[k]:>6}{code_amt[k]:>12.2f}")
        if code_amt[k] > code_amt[best]:
            best = k
    print("Highest-value product : " + codes[best] + " (Rs. " + f"{code_amt[best]:.2f}" + ")")

print("\n" + "=" * 72)
print("MALFORMED RECORDS FLAGGED")
print("=" * 72)
if len(error_log) == 0:
    print("None")
else:
    for item in error_log:
        number, original, problems = item
        shown = original
        if shown == "":
            shown = "(empty line)"
        print("Record " + str(number) + " : " + shown)
        for p in problems:
            print("   - " + p)

print("\nSUMMARY : records = " + str(n) + ", valid = " + str(len(valid_records)) +
      ", malformed = " + str(len(error_log)))

