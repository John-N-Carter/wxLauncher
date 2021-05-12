#! python3
from imports import *

SETUP = 'SETUP'
SYSTEM = 'SYSTEM'
TAB = 'Tab'
NAME = 'Name'
ICON = 'Icon'
COMMAND = 'Command'
TYPE = 'Type'
COUNT = 'Count'
PROG = 'program'
LABEL = 'Label'
BUTTON = 'Button'
COLOUR = 'Colour'
DROP = 'Drop'
ELEVATION = 'Elevation'
LINES = 'Lines'
#
MOST_POPULAR = 'Frequent'
#
INI_FILE = INIFILE = 'launcher.ini'
ICONPATH = 'icons'
#
SHORTCUTPATH = 'Shortcuts'
#
#
#
NAME_STRING = 'wxLauncher'
EXPLORER = None
FIREFOX = None
#
myPosition = 1690
myWidth =1650
myHeight = 104
#
SQUARE_500 = (500, 500)
S_100_25 = (100, 25)
S_500_25 = (700, 25)
#
PER_ROW = 25
#
STATS = True
#
textKeys = set([# string commands
    'Command',
    'Icon',
    'Tab',
    'Name',
    'Count'])
binaryKeys = set([ # Binary Commands
    'Drop',
    'Elevation'])
otherKeys =set([ # others
    'Worst',
    'Colour',
    'IconData'])
lbList = ['EXEC', 'LINK', 'INTERNAL', 'PYTHON'] # options for radio button type
radioKeys = {
    'Type':lbList
    }



if __name__ == '__main__':
    print('Constants and CONST namespace for Luncher')
    print(sys.argv)
    print(os.path.abspath(sys.argv[0]))
