#!/usr/bin/env python3

import sys
import math

def round_to_nearest_100(number):
    return math.floor(number / 100 + 0.5) * 100

def calculate_xp(cr):
    return round_to_nearest_100(-0.00423870517390708 * cr**6 + 0.34063676404399 * cr**5 - 9.61698619982549 * cr**4 + 122.059894737395 * cr**3 - 656.533146529477 * cr**2 + 1732.02671196015 * cr - 1052.47597995511)

def print_usage_and_exit():
    print("Usage: {} -n -c <integer>".format(sys.argv[0]))
    print("If executed without any arguments, the script will run interactively.")
    sys.exit(1)

if "-n" in sys.argv:
    cr_index = sys.argv.index("-c") if "-c" in sys.argv else None
    if cr_index is None or cr_index + 1 >= len(sys.argv):
        print_usage_and_exit()

    try:
        cr = int(sys.argv[cr_index + 1])
    except ValueError:
        print("Invalid value for Challenge Rating. Please provide an integer.")
        sys.exit(1)

    xp = calculate_xp(cr)
    # Print XP value instead of using sys.exit()
    print(xp)
else:
    if len(sys.argv) > 1:
        print_usage_and_exit()

    try:
        cr = int(input("\nEnter A Challenge Rating.\n"))
    except ValueError:
        print("Invalid value for Challenge Rating. Please provide an integer.")
        sys.exit(1)

    xp = calculate_xp(cr)
    print("\nXP =", xp)

