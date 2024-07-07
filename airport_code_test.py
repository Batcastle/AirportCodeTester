#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  airport_code_test.py
#
#  Copyright 2024 Thomas Castleman <batcastle@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""Simple program to for someone to use to help them learn Airport codes"""
# Import needed libraries
import json
import subprocess as subproc
import random as rand

# Set global variables
CODES_FILE = "airport_codes.json"
SETTINGS_FILE = "settings.json"
GREEN = "\033[92m"
RED = "\033[91m"
CLEAR = "\033[0m"
YELLOW = "\033[93m"
BLUE = '\033[94m'

WARNING = YELLOW + "WARNING: "
ERROR = RED + "ERROR: "
STATUS = BLUE
CORRECT = GREEN + "CORRECT! " + CLEAR
INCORRECT = RED + "INCORRECT! " + CLEAR

# Load settings
with open(CODES_FILE, "r") as file:
    CODES = json.load(file)

with open(SETTINGS_FILE, "r") as file:
    SETTINGS = json.load(file)

# Generate other data
INV_CODES = {v: k for k, v in CODES.items()}


def test(codes: dict, inv_codes: dict, ask) -> dict:
    """Test the user on airport codes"""
    while True:
        print("""\nShould this test be:
 1) Airport code -> City
 2) City -> Airport Code
 3) Both
 4) Exit
""")
        ans = input("Choice: ")
        if ans in ("1", "2", "3"):
            break
        if ans == "4":
            print("Exiting...")
            exit()
        print("\nInput not recognized. Please try again...\n")
    score_sheet = {}

    # Time for actual test!
    print("Starting Test...")
    click_to_continue()
    clear_screen()
    if ans == "1":
        while len(score_sheet) < len(codes):
            selection = rand.sample(list(codes.keys()), 1)[0]
            if selection in score_sheet:
                continue
            print(f"QUESTION { len(score_sheet) + 1} / { len(codes) }")
            while True:
                options = rand.sample(list(inv_codes.keys()),
                                      (SETTINGS["multiple_choice_answer_count"] * 2))
                if codes[selection] not in options:
                    break
            score_sheet[selection] = ask(selection, options,
                                         SETTINGS["multiple_choice_answer_count"], codes[selection])
            click_to_continue()
            clear_screen()
    if ans == "2":
        while len(score_sheet) < len(inv_codes):
            selection = rand.sample(list(inv_codes.keys()), 1)[0]
            if selection in score_sheet:
                continue
            print(f"QUESTION { len(score_sheet) + 1} / { len(inv_codes) }")
            while True:
                options = rand.sample(list(codes.keys()),
                                      (SETTINGS["multiple_choice_answer_count"] * 2))
                if inv_codes[selection] not in options:
                    break
            score_sheet[selection] = ask(selection, options,
                                         SETTINGS["multiple_choice_answer_count"],
                                         inv_codes[selection])
            click_to_continue()
            clear_screen()
    if ans == "3":
        while len(score_sheet) < len(codes):
            flipper = rand.randint(1, 1000)
            if (flipper % 2) == 1:
                selection = rand.sample(list(inv_codes.keys()), 1)[0]
                if (selection in score_sheet) or (inv_codes[selection] in score_sheet):
                    continue
                print(f"QUESTION { len(score_sheet) + 1} / { len(inv_codes) }")
                while True:
                    options = rand.sample(list(codes.keys()),
                                          (SETTINGS["multiple_choice_answer_count"] * 2))
                    if inv_codes[selection] not in options:
                        if selection not in options:
                            break
                score_sheet[selection] = ask(selection, options,
                                             SETTINGS["multiple_choice_answer_count"],
                                             inv_codes[selection])
                click_to_continue()
                clear_screen()
            else:
                selection = rand.sample(list(codes.keys()), 1)[0]
                if (selection in score_sheet) or (codes[selection] in score_sheet):
                    continue
                print(f"QUESTION { len(score_sheet) + 1} / { len(codes) }")
                while True:
                    options = rand.sample(list(inv_codes.keys()),
                                          (SETTINGS["multiple_choice_answer_count"] * 2))
                    if codes[selection] not in options:
                        if selection not in options:
                            break
                score_sheet[selection] = ask(selection, options,
                                             SETTINGS["multiple_choice_answer_count"],
                                             codes[selection])
                click_to_continue()
                clear_screen()
    return score_sheet


def ask_multiple_choice(query: str, possible_options: list, count: int, answer: str) -> bool:
    """Ask the user a multiple choice question.

        query - The code or location to ask about.
        possible_options - list of possible answers that this function can choose from to display.
        count - the number of possible answers to display.
        answer - the correct answer to the question.

    Returns True if answered correctly, False if incorrectly.
    """
    options = rand.sample(possible_options, count - 1)
    options.append(answer)
    rand.shuffle(options)
    while True:
        if len(query) == 3:
            print(f"What is the location for airport code \"{query}\"?")
        else:
            print(f"What is the airport code for {query}?")
        displayed = 1
        for each in options:
            print(f"{displayed}) {each}")
            displayed += 1
        try:
            user_answer = int(input(f"Answer [1-{displayed - 1}]: "))
        except ValueError:
            print("Not a valid answer. Please try again.")
            click_to_continue()
            clear_screen()
        valid = False
        for each in range(1, displayed + 1):
            if user_answer == each:
                valid = True
                break
        if not valid:
            print("Not a valid answer. Please try again.")
            click_to_continue()
            clear_screen()
            continue
        break
    # Options indexes are offset by +1 for user experience.
    # Need to undo this for future usage of the entry.
    user_answer -= 1
    selected = options[user_answer]
    if selected == answer:
        correct(query, answer)
        return True
    incorrect(query, selected, answer)
    return False


def ask_open_ended(query: str, possible_options: list, count: int, answer: str) -> bool:
    """Ask the user an open-ended question.

        query - The code or location to ask about.
        answer - the correct answer to the question.
        leniency - integer, specifies how lenient we should be on the answer.
            <=0 - Zero leniency. Must have correct spelling, punctuation, etc.
            1 - (default) Case insensitive. Otherwise, same as 0.
            >=2 - Case insensitive, must at least have city/airport name
                    spelled and punctuated correctly.

    Returns True if answered correctly, False if incorrectly.
    """
    del possible_options, count
    try:
        leniency = SETTINGS["leniency"]
    except KeyError:
        leniency = 1
    if len(query) == 3:
        print(f"What is the location for airport code \"{query}\"?")
    else:
        print(f"What is the airport code for {query}?")
    user_answer = input("Answer: ")
    if leniency <= 0:
        if answer == user_answer:
            correct(query, answer)
            return True
    if leniency == 1:
        if answer.lower() == user_answer.lower():
            correct(query, answer)
            return True
    if leniency >= 2:
        if answer.lower() == user_answer.lower():
            correct(query, answer)
            return True
        if len(query) > 3:
            user_city = user_answer.lower().split(",")[0]
            correct_city = answer.lower().split(",")[0]
            if user_city == correct_city:
                correct(query, answer)
                return True
    incorrect(query, user_answer, answer)
    return False


def clear_screen():
    """Clear the screen"""
    subproc.check_call(["clear"])


def click_to_continue():
    """Simple "wait until enter is pressed" function"""
    input("Press Enter to Continue...")


def incorrect(query: str, user_answer: str, correct_answer: str) -> None:
    """Notify the user of an incorrect answer"""
    print(f""""
{INCORRECT}
\"{query}\" is:     {GREEN}{correct_answer}{CLEAR}
Your answer:  {RED}{user_answer}{CLEAR}
""")


def correct(query: str, answer: str) -> None:
    """Notify the user of a correct answer"""
    print(f"\n{CORRECT}\n\"{query}\" is:    {GREEN}{answer}{CLEAR}\n")


def main():
    """Entry Point"""
    print("Would you like a multiple-choice, or fill-in-the-blank quiz?")
    while True:
        ans = input("1) multiple choice, 2) fill in the blank, 3) Exit: ")
        if ans == "1":
            score_sheet = test(CODES, INV_CODES, ask_multiple_choice)
            break
        if ans == "2":
            score_sheet = test(CODES, INV_CODES, ask_open_ended)
            break
        if ans == "3":
            print("Exiting...")
            exit()
        print("\nInput not recognized. Please try again...\n")
    right = 0
    for each in score_sheet:
        if score_sheet[each]:
            right += 1
    wrong = 0
    for each in score_sheet:
        if not score_sheet[each]:
            wrong += 1
    score = (right / len(CODES)) * 100
    if score >= SETTINGS["passing_score"]:
        score = f"{GREEN}{score:.2f}%{CLEAR}"
    else:
        score = f"{RED}{score:.2f}%{CLEAR}"
    print(f"""
{ "#" * 5 } SUMMARY { "#" * 5 }
{GREEN} CORRECT {CLEAR}         - {right}
{RED} INCORRECT {CLEAR}       - {wrong}
{BLUE} TOTAL QUESTIONS {CLEAR} - {len(CODES)}
{BLUE} SCORE {CLEAR}           - {score}
""")
    print("Would you like to view your score sheet or export it to a file?")
    while True:
        ans = input("1) View, 2) Export, 3) Exit: ")
        if ans == "1":
            for each in score_sheet:
                if score_sheet[each]:
                    if len(each) == 3:
                        print(f"{each} - {CODES[each]} - {GREEN}CORRECT{CLEAR}")
                    else:
                        print(f"{INV_CODES[each]} - {each} - {GREEN}CORRECT{CLEAR}")
                else:
                    if len(each) == 3:
                        print(f"{each} - {CODES[each]} - {RED}INCORRECT{CLEAR}")
                    else:
                        print(f"{INV_CODES[each]} - {each} - {RED}INCORRECT{CLEAR}")
            break
        if ans == "2":
            while True:
                print("What would you like the file name to be?")
                ans = input("*.json file name: ")
                try:
                    with open(f"{ans}.json", "w+") as file:
                        json.dump(score_sheet, file, indent=2)
                    break
                except (PermissionError, IOError, OSError):
                    print("\nFile name/location not allowed, please try again.\n")
            break
        if ans == "3":
            print("Exiting...")
            exit()
        print("\nInput not recognized. Please try again...\n")


if __name__ == "__main__":
    main()
