#!/usr/bin/env python3

# Future feature: export to text file
# Future feature: detect and offer to rename existing files

# Future feature: export to ODS with nice formatting
#import pandas

import sys
import signal
import math
from colorama import Fore, Back, Style
import platform
import logging
import re
import os
import subprocess

# Make colorama work on Windows
if platform.system() == "Windows":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Define signal handler for CTRL+C on Mac/Linux; Windows handles this with default prompt.
def sigint_handler(signal, frame):
    print("\nCTRL+C Received.  Exiting.")
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
print("Welcome to 5e Monster Generator version ", version, ".", sep='')

# Provide basic instructions and link to source material
print(Fore.YELLOW + "\nTHIS GENERATOR IS FOR LEVELS 1 AND ABOVE.\n" + Style.RESET_ALL)
print("Refer to \"5e Monster Manual on a Business Card\" for instructions on")
print("how to use these statistics and monster statistics for lower levels.")
print(Fore.CYAN + "https://www.blogofholding.com/?p=7338\n" + Style.RESET_ALL)

# Clarify how save/skill bonuses work
print(Fore.YELLOW + "A NOTE ABOUT SAVE/SKILL BONUSES:" + Style.RESET_ALL)
print("-\"Good Save/Skill Bonus\" is the best save/skill bonus the monster has.")
print("-\"Average Save/Skill Bonus\" is a very rough estimate of most other saves/skills\nfor the monster.")
print("-Most monsters have one or more \"Bad\" saves/skills.  How many they have and how\nbad they are is completely arbitrary.  In general, lower-CR monsters have a lot\nof bad saves/skills while higher-CR monsters have one or two.  This generator\nwill calculate approximate \"Bad\" saves/skills.")
print("-To determine a skill's total bonus, simply add the Proficiency bonus to the \nassociated Ability Score.\n")

# Clarify how XP works
print(Fore.YELLOW + "A NOTE ABOUT XP:" + Style.RESET_ALL)
print("XP is calculated based on a formula that approximates the values in official.")
print("books.  Since official monster XP is somewhat arbitrary, the formula won't")
print("always match official monsters at a given CR.  Arguably, this is more")
print("consistent and therefore better than the official XP values, but if you don't")
print("like that, feel free to ignore the provided XP value.\n")

# TODO: Implement spreadsheet (.odt/.xls/.xlsx) output.

# Get desired monster generation range
# TODO: implement CR 0, 1/8, 1/4, and 1/2

try:
    low_cr = int(input(Fore.GREEN + "Enter the lowest challenge rating (CR) you want to generate statistics for:\n" + Style.RESET_ALL))
except ValueError:
    print(Fore.RED + "Challenge ratings must be whole numbers. Exiting.\n" + Style.RESET_ALL)
    exit(1)

try:
    high_cr = int(input(Fore.GREEN + "Enter the highest challenge rating you want to generate statistics for:\n" + Style.RESET_ALL))
except ValueError:
    print(Fore.RED + "Challenge ratings must be whole numbers. Exiting.\n" + Style.RESET_ALL)
    exit(1)

# Sanity checks for monster generation range
if high_cr < 1 or low_cr < 1:
    print(Fore.RED + "\nChallenge ratings to generate must be at least 1." + Style.RESET_ALL)
    print("Exiting.")
    exit(1)

if (high_cr - low_cr) < 0:
    print(Fore.RED + "\nPlease enter the lowest CR followed by the highest CR to generate." + Style.RESET_ALL)
    print("Exiting.")
    exit(1)

cr_range = (high_cr - low_cr + 1)

if cr_range < 1:
    print(Fore.RED + "\nPlease choose at least one challenge rating to generate monster statistics for." + Style.RESET_ALL)
    exit(1)

if cr_range > 20:
    print("\nThat would generate more than 20 challenge ratings of monster statistics.")
    sure = input("Are you sure? (y/N)\n")
    if sure in ['y', 'Y', 'yes', 'Yes', 'YES']:
        print("Proceeding.\n")
    else:
        print("\nExiting.\n")
        exit(1)

# Let user specify good/average/bad ability scores
def assign_ability_scores(ability):
    print(Fore.GREEN + "\nChoose whether", ability, "will be bad, average, or good." + Style.RESET_ALL)
    print("1. Bad")
    print("2. Average")
    print("3. Good")
    try:
        goodness = int(input(Fore.GREEN + "Your choice (1-3): " + Style.RESET_ALL))
    except ValueError:
        print(Fore.RED + "\nPlease choose a number 1, 2, or 3." + Style.RESET_ALL)
        print("Exiting.")
        exit(1)
    if goodness < 1 or goodness > 3:
        print(Fore.RED + "\nPlease choose a number 1, 2, or 3." + Style.RESET_ALL)
        print("Exiting.")
        exit(1)
    if goodness == 1:
        print(ability, "will be Bad.\n")
    if goodness == 2:
        print(ability, "will be Average.\n")
    if goodness == 3:
        print(ability, "will be Good.\n")
    return goodness

Strength_goodness = assign_ability_scores("Strength")
Dexterity_goodness = assign_ability_scores("Dexterity")
Constitution_goodness = assign_ability_scores("Constitution")
Intelligence_goodness = assign_ability_scores("Intelligence")
Wisdom_goodness = assign_ability_scores("Wisdom")
Charisma_goodness = assign_ability_scores("Charisma")

# Ask whether each ability score has saving throw proficiency.
def proficiency(ability):
    prof = str(input(Fore.GREEN + "\nWill " + ability + " have saving throw proficiency? (Y/N) " + Style.RESET_ALL))
    if not prof.lower() in ["y", "n"]:
        print(Fore.RED + "\nPlease choose \"Y\" or \"N\"." + Style.RESET_ALL)
        print("Exiting.")
        exit(1)        
    return prof.lower()

Strength_prof = proficiency("Strength")
Dexterity_prof = proficiency("Dexterity")
Constitution_prof = proficiency("Constitution")
Intelligence_prof = proficiency("Intelligence")
Wisdom_prof = proficiency("Wisdom")
Charisma_prof = proficiency("Charisma")

# Function to strip color codes
def strip_color_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Ask the user if they want logging and set up the logger if they do
log_to_file = input(Fore.GREEN + "\nDo you want to log the output to a file? (Y/N) " + Style.RESET_ALL).lower()
if not log_to_file.lower() in ["y", "n"]:
    print(Fore.RED + "\nPlease choose \"Y\" or \"N\"." + Style.RESET_ALL)
    print("Exiting.")
    exit(1)
if log_to_file == 'y':
    log_file = input(Fore.GREEN + "Enter the log file name (default: monsters.txt): " + Style.RESET_ALL) or 'monsters.txt'
    log_file = os.path.expandvars(os.path.expanduser(log_file))  # expand ~ and $HOME
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(message)s')
else:
    logging.basicConfig(level=logging.CRITICAL)  # Prevent logging if not desired

# Function to call xp_by_cr.py and get the value of "xp"
def get_xp(cr):
    try:
        # Run xp_by_cr.py with -n -c <cr> flags and capture the exit code
        #xp = subprocess.check_output(["./xp_by_cr.py", "-n", "-c", str(CR)], stderr=subprocess.STDOUT)
        xp = subprocess.check_output([sys.executable, "xp_by_cr.py", "-n", "-c", str(cr)], stderr=subprocess.STDOUT)
        # Convert the exit code (bytes) to integer
        xp = int(xp)
        return xp
    except subprocess.CalledProcessError as e:
        # Print the exit status
        print("Subprocess returned non-zero exit status:", e.returncode)
        # Handle subprocess error
        print("Subprocess error:", e)
        return None

# TODO: separate variable creation from printing; use loops on function calls instead.  

# Define variables, print results
print("\nGenerating...")
print("\n----------------------------------------\n")

def print_stats():
    current_cr = low_cr
    while current_cr <= high_cr:
        if current_cr == 1:
            CR = current_cr
            AC = 13
            HP = 30
            Proficiency = 2
            Attack = 4
            Damage = 10
            DC = 11
            GoodSave = 3
            AverageSave = 0
        elif 2 <= current_cr <= 7:
            CR = current_cr
            AC = 13 + 1 / 3 * CR
            HP = 15 * CR + 15
            Proficiency = 1 + int(math.ceil(.25 * CR))
            Attack = 4 + 1 / 2 * CR
            Damage = 5 * CR + 5
            DC = 11 + 1 / 2 * CR
            GoodSave = 3 + 1 / 2 * CR
            AverageSave = 1 / 2 * CR - 1
        elif current_cr > 7:
            CR = current_cr
            AC = 13 + 1 / 3 * CR
            HP = 15 * CR
            Proficiency = 1 + int(math.ceil(.25 * CR))
            Attack = 4 + 1 / 2 * CR
            Damage = 5 * CR
            DC = 11 + 1 / 2 * CR
            GoodSave = 3 + 1 / 2 * CR
            AverageSave = 1 / 2 * CR - 1
        # Generate Bad abilility scores
        if Strength_goodness == 1:
            Strength = roundhalf(.48 * CR + 3.52)
        if Dexterity_goodness == 1:
            Dexterity = roundhalf(.48 * CR + 3.52)
        if Constitution_goodness == 1:
            Constitution = roundhalf(.48 * CR + 3.52)
        if Intelligence_goodness == 1:
            Intelligence = roundhalf(.48 * CR + 3.52)
        if Wisdom_goodness == 1:
            Wisdom = roundhalf(.48 * CR + 3.52)
        if Charisma_goodness == 1:
            Charisma = roundhalf(.48 * CR + 3.52)
        # Define Average Ability Scores
        if Strength_goodness == 2:
            Strength = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        if Dexterity_goodness == 2:
            Dexterity = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        if Constitution_goodness == 2:
            Constitution = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        if Intelligence_goodness == 2:
            Intelligence = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        if Wisdom_goodness == 2:
            Wisdom = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        if Charisma_goodness == 2:
            Charisma = (roundhalf(AverageSave) - roundhalf(Proficiency)) * 2 + 10
        # Define Good Ability Scores 
        if Strength_goodness == 3:
            Strength = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        if Dexterity_goodness == 3:
            Dexterity = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        if Constitution_goodness == 3:
            Constitution = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        if Intelligence_goodness == 3:
            Intelligence = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        if Wisdom_goodness == 3:
            Wisdom = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        if Charisma_goodness == 3:
            Charisma = (roundhalf(GoodSave) - roundhalf(Proficiency)) * 2 + 10
        # Define Ability Score Modifiers
        Strength_mod = math.floor((Strength - 10) / 2)
        Dexterity_mod = math.floor((Dexterity - 10) / 2)
        Constitution_mod = math.floor((Constitution - 10) / 2)
        Intelligence_mod = math.floor((Intelligence - 10) / 2)
        Wisdom_mod = math.floor((Wisdom - 10) / 2)
        Charisma_mod = math.floor((Charisma - 10) / 2)
        # Generate saving throws
        if Strength_prof.lower() == "y":
            Strength_save = roundhalf(Strength_mod + Proficiency)
        else:
            Strength_save = roundhalf(Strength_mod)
        if Dexterity_prof.lower() == "y":
            Dexterity_save = roundhalf(Dexterity_mod + Proficiency)
        else:
            Dexterity_save = roundhalf(Dexterity_mod)
        if Constitution_prof.lower() == "y":
            Constitution_save = roundhalf(Constitution_mod + Proficiency)
        else:
            Constitution_save = roundhalf(Constitution_mod)        
        if Intelligence_prof.lower() == "y":
            Intelligence_save = roundhalf(Intelligence_mod + Proficiency)
        else:
            Intelligence_save = roundhalf(Intelligence_mod)        
        if Wisdom_prof.lower() == "y":
            Wisdom_save = roundhalf(Wisdom_mod + Proficiency)
        else:
            Wisdom_save = roundhalf(Wisdom_mod)        
        if Charisma_prof.lower() == "y":
            Charisma_save = roundhalf(Charisma_mod + Proficiency)
        else:
            Charisma_save = roundhalf(Charisma_mod)

        # Store output in a variable
        output = (
            f"{Back.BLUE + Fore.RED}Challenge Rating {str(current_cr)} ({get_xp(CR)} XP){Style.RESET_ALL}\n"
            f"{Fore.GREEN}\nGeneral Statistics:{Style.RESET_ALL}\n"
            f"AC = {roundhalf(AC)} (+/-) 3\n"
            f"HP = {roundhalf(HP)} (+/-) {roundhalf(.5 * HP)}\n"
            f"Proficiency Bonus = {Proficiency}\n"
            f"Attack Bonus = {roundhalf(Attack)} (+/-) 2\n"
            f"Damage Per Round (one attack or multiattack total) = {roundhalf(Damage)} (+/-) {roundhalf(.5 * Damage)}\n"
            f"Multi-Target Attack (one attack or multiattack total) = {roundhalf(.5 * Damage)} (+/-) {roundhalf(.25 * Damage)}\n"
            f"Single-Target Limited-Use Attack = {roundhalf(2 * Damage)} (+/-) {roundhalf(Damage)}\n"
            f"Multi-Target Limited-Use Attack = {roundhalf(Damage)} (+/-) {roundhalf(.5 * Damage)}\n"
            f"Save DC = {roundhalf(DC)} (+/-) 2\n"
            f"\n"
            f"{Fore.GREEN}Saving Throws (+/-) 1:{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}Bad saving throws are arbitrary. This is only a suggestion.{Style.RESET_ALL}\n"
            f"Strength = {roundhalf(Strength_save)}\n"
            f"Dexterity = {roundhalf(Dexterity_save)}\n"
            f"Constitution = {roundhalf(Constitution_save)}\n"
            f"Intelligence = {roundhalf(Intelligence_save)}\n"
            f"Wisdom = {roundhalf(Wisdom_save)}\n"
            f"Charisma = {roundhalf(Charisma_save)}\n"
            f"\n"
            f"{Fore.GREEN}Ability Scores (+/-) 2 (1):{Style.RESET_ALL}\n"
            f"{Fore.YELLOW}Bad ability scores are arbitrary. This is only a suggestion.{Style.RESET_ALL}\n"
            f"Strength = {Strength} ({Strength_mod})\n"
            f"Dexterity = {Dexterity} ({Dexterity_mod})\n"
            f"Constitution = {Constitution} ({Constitution_mod})\n"
            f"Intelligence = {Intelligence} ({Intelligence_mod})\n"
            f"Wisdom = {Wisdom} ({Wisdom_mod})\n"
            f"Charisma = {Charisma} ({Charisma_mod})\n"
            f"\n----------------------------------------\n"
        )

        print(output)  # Print the stored output

        if log_to_file == 'y':  # Log the output if logging is enabled
            logging.info(strip_color_codes(output))
            print("New monster stats have been appended to the output file.")

        current_cr += 1

print_stats()

print(input("Press ENTER to exit."))
