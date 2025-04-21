from pathlib import Path
import re

# Paths
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / 'files'
WINDOW_ICON_PATH = FILES_DIR / 'icon.png'

# Colors
PRIMARY_COLOR = '#1e81b0'
DARKER_PRIMARY_COLOR = '#16658a'
DARKEST_PRIMARY_COLOR = '#115270'

# Fonts
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 10
MINIMUN_WIDTH = 500

# Verify
NUM_OR_DOT_REGEX = re.compile('[0-9.]')

def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))

def isValidNumber(string):
    try:
        float(string)
        return True
    except:
        return False

def isEmpty(string: str):
    return len(string) == 0


def isValidOperator(operator):
    if operator in ['^', '/', '*', '-', '+']:
        return True
    return False

def convertToNumber(string):
    number = float(string)

    if number.is_integer():
        number = int(number)

    return number






    




