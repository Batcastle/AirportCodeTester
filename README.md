# AirportCodeTester
Simple script to help someone learn Airport Codes

## About
AirportCodeTester is a simple script to help you learn airport codes. It provides a total of 6 possible testing modes, with varying degrees of difficulty. It should run out-of-the-box on Linux, and likely MacOS too. Windows users will need Python 3 installed on their computers already. But that should be the only dependency. This script runs on the command line to help cut down on dependencies and prevent platform lock-in.

## Usage
Simply run `airport_code_test.py` in your command line!

## Configuration
### Airport codes
In order to add, remove, or edit the airport codes known AirportCodeTester, simply edit `airport_codes.json`

By default, AirportCodeTester comes with `airport_codes.json` pre-populated with the 60 most commonly traveled airports in the American Airlines system. Feel free to open a PR to add more airports.

### Settings
To configure settings, edit `settings.json`

To make the tests more lenient for new uers, you can change the `leniency` field to >=2. By default, it is set to 1 to provide a challenge, but not be overly unfair. You can set this to 0 for a greater challenge (this enables case-sensitivity), or set it to >=2 to make it easier (this makes it where the tester just pays attention to the city name). `leniency` has no effect on multiple choice quizes.

`multiple_choice_answer_count` allows you to control the difficulty of the multiple choice quizes by adding more or less options to chose from. By default this is set to 4 to mirror many standard tests.

`test_length` is not used yet, but will allow you to set how many questions to ask when tested. This can be useful when doing a quick review vs. a full blow quiz.

`passing_score` largely just sets what color the minimum is to change the score from red to green, marking that you passed the test.
