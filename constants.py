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
INIFILE = 'launcher.ini'
ICONPATH = 'icons'
#
ICON_PATH = 'H:\\Computers\\PythonTools\\Launcher\\icons'
SHORTCUTPATH = 'Shortcuts'
INI_FILE = 'launcher.ini'
#
FULL_INI_PATH = 'H:\\Computers\\PythonTools\\Launcher\\' + INI_FILE
#
PICLKEFILE = INIFILE.replace('.ini', '.pickle')
#
NAME_STRING = 'wxLauncher'
EXPLORER = None
FIREFOX = None
#
#~ myWidth =1400
#~ myPosition = 1900 # debug of right screen
#~ myPosition = 25 # run on left screen
myPosition = 1690
myWidth =1650
myHeight = 104
#
SQUARE_500 = (500, 500)
S_100_25 = (100, 25)
S_500_25 = (700, 25)
#
#~ PerRow = 16L
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
    print('Constants for Luncher')
