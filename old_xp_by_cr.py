#!/usr/bin/env python3

import sys
import math

def round_to_nearest_100(number):
    return math.floor(number / 100 + 0.5) * 100

cr = int(input( "\nEnter A Challenge Rating.\n"))

xp = round_to_nearest_100(-0.00423870517390708 * cr**6 + 0.34063676404399 * cr**5 - 9.61698619982549 * cr**4 + 122.059894737395 * cr**3 - 656.533146529477 * cr**2 + 1732.02671196015 * cr - 1052.47597995511)

print("\nXP = ", xp)
