#!/usr/bin/env python3.10
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
WORKING = 'Working'
DEFAULTARGUMENT = 'Defaultargument'
#
MOST_POPULAR = 'Frequent'
#
INI_FILE = INIFILE = 'launcher.ini'
ICONPATH = 'icons'
ICONCACHE = 'iconcache'
#
DEFAULTICONS = 'DefaultIcons'
#
SHORTCUTPATH = 'Shortcuts'
#
QUERYNAME = 'query.bmp'
#
LINKNAME = 'query.ico'
#
ICONSEXT = os.path.join(R'C:\Programs\iconsext', 'iconsext.exe') # edit path as appropriate
if not os.path.exists(ICONSEXT):
    ICONSEXT = None
#
name = sys.argv[0]
name = os.path.abspath(name)
localpath, name = os.path.split(name)
#
# over write constants with local path
#
ICON_PATH = ICONPATH = os.path.join(localpath, ICONPATH) # 'H:\\Computers\\PythonTools\\Launcher\\icons'
#
FULL_INI_PATH = os.path.join(localpath, INIFILE) #'H:\\Computers\\PythonTools\\Launcher\\' + INI_FILE
#
PICLKEFILE = FULL_INI_PATH.replace('.ini', '.pickle')
#
#~ QUERYNAME = os.path.join(ICON_PATH, QUERYNAME) # default icon
#
#~ SHORTCUTPATH = os.path.join(localpath, SHORTCUTPATH)
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
TEXT_TITLE = (200, 25)
S_100_25 = (100, 25)
S_500_25 = (500, 25)
S_700_25 = (700, 25)
TEXT_IN = (600, 25)
#
PER_ROW = 25
#
STATS = True
#
textKeys = {
    'Command',
    'Icon',
    'Tab',
    'Name',
    'Defaultargument',
    'Working',
    'Count',
}

plaintextKeys = {'Defaultargument', 'Working'}
binaryKeys = {'Drop', 'Elevation'}
otherKeys = {'Worst', 'Colour', 'IconData'}
lbList = ['EXEC', 'LINK', 'INTERNAL', 'PYTHON'] # options for radio button type
radioKeys = {
    'Type':lbList
    }

printNames = { # maping to be used to print names formatted
    'Defaultargument':'Default Argument'
    }



if __name__ == '__main__':
    print('Constants and CONST namespace for Luncher')
    print(sys.argv)
    print(os.path.abspath(sys.argv[0]))
