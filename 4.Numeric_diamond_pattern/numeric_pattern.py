# =====================================================================
# CS27 : Advanced Numeric Pattern Generator (hollow / filled diamond)
# Syllabus used : variables, operators, conditionals, loops,
#                 nested loops, strings, pattern generation
# =====================================================================

print("=" * 50)
print("       NUMERIC DIAMOND PATTERN GENERATOR")
print("=" * 50)

MIN_SIZE = 3
MAX_SIZE = 19

running = True
while running:
    text = input("\nEnter diamond size (odd, " + str(MIN_SIZE) + "-" + str(MAX_SIZE) +
                 "), or 0 to quit : ").strip()

    # ---------------- Validation ----------------
    if text == "0":
        print("Thank you. Goodbye!")
        running = False
    elif not text.isdigit():
        print("Invalid input: please enter digits only (no letters, signs or decimals).")
    else:
        n = int(text)
        if n < MIN_SIZE or n > MAX_SIZE:
            print("Invalid size: must be between " + str(MIN_SIZE) + " and " + str(MAX_SIZE) + ".")
        elif n % 2 == 0:
            print("Invalid size: " + str(n) + " is even. A symmetric diamond needs an odd size.")
        else:
            style = input("Style  1 = Hollow diamond   2 = Filled palindromic diamond : ").strip()
            if style != "1" and style != "2":
                print("Invalid style: choose 1 or 2.")
            else:
                mid = n // 2
                print()
                # ---------------- Pattern generation ----------------
                for row in range(n):
                    if row < mid:
                        d = mid - row          # distance of this row from the centre row
                    else:
                        d = row - mid
                    k = mid - d + 1            # width index of this row (1 at the tips)
                    line = ""

                    if style == "1":
                        # hollow: only the two border columns carry a digit
                        for col in range(n):
                            if col == d or col == n - 1 - d:
                                line += str(k % 10)
                            else:
                                line += " "
                    else:
                        # filled: digits climb 1..k then fall k-1..1 (palindrome)
                        line = " " * d
                        up = 1
                        while up <= k:
                            line += str(up % 10)
                            up += 1
                        down = k - 1
                        while down >= 1:
                            line += str(down % 10)
                            down -= 1

                    print(line.rstrip())
