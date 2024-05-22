#!/usr/bin/env python3

# Future feature: export to ODS with nice formatting
#import pandas
# Future feature: detect and offer to rename existing files
import sys
import signal
import math
from colorama import Fore, Back, Style
import platform


# Make colorama work on Windows
if platform.system() == "Windows":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Define signal handler for CTRL+C on Mac/Linux; Windows handles this with default prompt.
def sigint_handler(signal, frame):
    print ("\nCTRL+C Received.  Exiting.")
    sys.exit(0)

# Execute cigint_handler when CTRL+C is pressed on Mac/Linux
signal.signal(signal.SIGINT, sigint_handler)
    
# Make rounding work the way we learned in elementary school
def roundhalf(val):
    if (float(val) % 1) >= 0.5:
        return math.ceil(val)
    else:
        return round(val)

# Display program name and version
version = 0.1
print ("Welcome to 5e Monster Generator version ", version, ".", sep='')

# Provide basic instructions and link to source material
print (Fore.YELLOW + "\nTHIS GENERATOR IS FOR LEVELS 1 AND ABOVE.\n" + Style.RESET_ALL)
print ("Refer to \"5e Monster Manual on a Business Card\" for instructions on")
print ("how to use these statistics and monster statistics for lower levels.")
print (Fore.CYAN + "https://www.blogofholding.com/?p=7338\n" + Style.RESET_ALL)

# Clarify how save/skill bonuses work
print (Fore.YELLOW + "A NOTE ABOUT SAVE/SKILL BONUSES:" + Style.RESET_ALL)
print ("-\"Good Save/Skill Bonus\" is the best save/skill bonus the monster has.")
print ("-\"Average Save/Skill Bonus\" is a very rough estimate of most other saves/skills\nfor the monster.")
print ("-Most monsters have one or more \"Bad\" saves/skills.  How many they have and how\nbad they are is completely arbitrary.  In general, lower-CR monsters have a lot\nof bad saves/skills while higher-CR monsters have one or two.  This generator\nwill not attempt to calculate \"Bad\" saves/skills.\n")

# TODO: Ask user whether to output to stdout, text file, or spreadsheet file (ods)
# TODO: If user chooses output to file, ask for location (default ./)
# TODO: Detect existing file and ask user whether to move them or overwrite

# Get desired monster generation range
try:
    low_cr = int(input(Fore.GREEN + "Enter the lowest challenge rating (CR) you want to generate statistics for:\n" + Style.RESET_ALL))
except ValueError:
    print (Fore.RED + "Challenge ratings must be whole numbers. Exiting.\n" + Style.RESET_ALL)
    exit(1)

try:
    high_cr = int(input(Fore.GREEN + "Enter the highest challenge rating you want to generate statistics for:\n" + Style.RESET_ALL))
except ValueError:
    print (Fore.RED + "Challenge ratings must be whole numbers. Exiting.\n" + Style.RESET_ALL)
    exit(1)

# Sanity checks for monster generation range
if high_cr < 1 or low_cr < 1:
    print (Fore.RED + "\nChallenge ratings to generate must be at least 1." + Style.RESET_ALL)
    print ("Exiting.")
    exit(1)

if (high_cr - low_cr) < 0:
    print (Fore.RED + "\nPlease enter the lowest CR followed by the highest CR to generate." + Style.RESET_ALL)
    print ("Exiting.")
    exit(1)

cr_range = (high_cr - low_cr + 1)

if cr_range < 1:
    print (Fore.RED + "\nPlease choose at least one challenge rating to generate monster statistics for." + Style.RESET_ALL)
    exit(1)

if cr_range > 20:
    print ("\nThat would generate more than 20 challenge ratings of monster statistics.")
    sure = input("Are you sure? (y/N)\n")
    if sure in ['y', 'Y', 'yes', 'Yes', 'YES']:
        print("Proceeding.\n")
    else:
        print ("\nExiting.\n")
        exit(1)

def map_ability(ability_int):
    global ability
    if ability_int == 1:
        ability = "Strength"
    if ability_int == 2:
        ability = "Dexterity"
    if ability_int == 3:
        ability = "Constitution"
    if ability_int == 4:
        ability = "Intelligence"
    if ability_int == 5:
        ability = "Wisdom"
    if ability_int == 6:
        ability = "Charisma"

# TODO: Make questions about primary/secondary/worst ability scores a loop function
# TODO: Figure out how to use the results of these questions to do different math on those scores.

print (Fore.GREEN + "\nEnter the number for the monster's PRIMARY ability score:")
print ("1. Strength")
print ("2. Dexterity")
print ("3. Constitution")
print ("4. Intelligence")
print ("5. Wisdom")
print ("6. Charisma" + Style.RESET_ALL)

try:
    ability_int = int(input("Primary Ability Score: "))
except ValueError:
    print (Fore.RED + "Please enter a number between 1 and 6." + Style.RESET_ALL)
    print ("Exiting.")
    exit(1)

map_ability(ability_int)
primary_ability = ability

print ("Primary ability score is", primary_ability)

print (Fore.GREEN + "\nEnter the number for the monster's SECONDARY ability score:")
print ("1. Strength")
print ("2. Dexterity")
print ("3. Constitution")
print ("4. Intelligence")
print ("5. Wisdom")
print ("6. Charisma" + Style.RESET_ALL)

try:
    ability_int = int(input("Secondary Ability Score: "))
except ValueError:
    print (Fore.RED + "Please enter a number between 1 and 6." + Style.RESET_ALL)
    print ("Exiting.")
    exit(1)

map_ability(ability_int)
secondary_ability = ability

print ("Secondary Ability Score is", secondary_ability)

print (Fore.GREEN + "\nEnter the number for the monster's WORST ability score:")
print ("1. Strength")
print ("2. Dexterity")
print ("3. Constitution")
print ("4. Intelligence")
print ("5. Wisdom")
print ("6. Charisma" + Style.RESET_ALL)

try:
    ability_int = int(input("Worst Ability Score: "))
except ValueError:
    print (Fore.RED + "Please enter a number between 1 and 6." + Style.RESET_ALL)
    print ("Exiting.")
    exit(1)

map_ability(ability_int)
worst_ability = ability

print ("Worst Ability Score is", worst_ability)


# TODO: separate variable creation from printing; use loops on function calls instead.  

# Define variables, print results
def print_stats():
    current_cr = low_cr
    print("\nGenerating...")
    print("\n----------------------------------------\n")
    while current_cr <= high_cr:
        print("Challenge Rating " + str(current_cr))
        if current_cr == 1:
            CR = current_cr
            AC = 13
            HP = 30
            Proficiency = 2
            Attack = 4
            Damage = 10
            DC = 11
            Save = 3
            AverageSave = 0
        elif 2 <= current_cr <= 7:
            CR = current_cr
            AC = 13 + 1 / 3 * CR
            HP = 15 * CR + 15
            Proficiency = 1 + int(math.ceil(.25 * CR))
            Attack = 4 + 1 / 2 * CR
            Damage = 5 * CR + 5
            DC = 11 + 1 / 2 * CR
            Save = 3 + 1 / 2 * CR
            AverageSave = 1 / 2 * CR - 1
        elif current_cr > 7:
            CR = current_cr
            AC = 13 + 1 / 3 * CR
            HP = 15 * CR
            Proficiency = 1 + int(math.ceil(.25 * CR))
            Attack = 4 + 1 / 2 * CR
            Damage = 5 * CR
            DC = 11 + 1 / 2 * CR
            Save = 3 + 1 / 2 * CR
            AverageSave = 1 / 2 * CR - 1

        print ("\nAC =", roundhalf(AC), "(+/-) 3")
        print ("HP =", roundhalf(HP), "(+/-)", roundhalf(.5 * HP))
        print ("Proficiency Bonus =", Proficiency)
        print ("Attack Bonus =", roundhalf(Attack), "(+/-) 2")
        print ("Damage Per Round =", roundhalf(Damage), "(+/-)", roundhalf(.5 * Damage))
        print ("Save DC =", roundhalf(DC), "(+/-) 2")
        print ("Good Save/Skill Bonus =", roundhalf(Save), "(+/-) 1")
        print ("Average Save/Skill Bonus =", roundhalf(AverageSave), "(+/-) 1")
        print ("\n----------------------------------------\n")

        current_cr += 1

# Call generation functions
print_stats()
print ("Done.  Press ENTER to Exit.\n")
input()
exit(0)

# TODO: after separting variable creation from printing, use variables to output to files at afore-specified path, moving files if requested

