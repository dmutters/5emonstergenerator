#!/usr/bin/env python3

import sys
import math

def round_to_nearest_25(number):
    return math.floor(number / 25 + 0.5) * 25

level = int(input( "\nEnter character level.\n"))

print("\nDifficulty:")
print("1. Easy")
print("2. Medium")
print("3. Hard")
print("4. Deadly")

difficulty = int(input( "\nChoose a difficulty (1-4).\n"))

if difficulty < 1:
    print("Please choose 1, 2, 3, or 4.  Exiting.\n")
    exit(1)
    
if difficulty > 4:
    print("Please choose 1, 2, 3, or 4.  Exiting.\n")
    exit(1)

if difficulty == 4:
    xp = round_to_nearest_25(0.002639991924 * level**6 - 0.156332727599 * level**5 + 3.587332301342 * level**4 - 39.39869782426 * level**3 + 232.2350714543 * level**2 - 399.1710092921 * level + 305.379256966)

if difficulty == 3:
    xp = round_to_nearest_25(0.001810098563 * level**6 - 0.106130255306 * level**5 + 2.407142242863 * level**4 - 26.12149867229 * level**3 + 152.8841343337 * level**2 - 263.2470862551 * level + 210.379256966)
    
if difficulty == 2:
    xp = round_to_nearest_25(0.001013950584 * level**6 - 0.0598255148742 * level**5 + 1.379104597598 * level**4 - 15.29230898466 * level**3 + 92.31269003982 * level**2 - 155.9860166649 * level + 127.4496904025)

if difficulty == 1:
    xp = round_to_nearest_25(0.000482437445 * level**6 - 0.029131051734 * level**5 + 0.682155890579 * level**4 - 7.613087353211 * level**3 + 45.97326941683 * level**2 - 78.02385527443 * level + 64.43111455111)

print("\nXP Per Party Member = ", xp)
