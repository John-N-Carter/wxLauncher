#!/usr/bin/env python3.10
#
# Remove circular inputs
#
import sys, os, binascii
import random as r, math as m, copy as C
import ctypes
#
import glob, string, math, time, getopt, shutil, configparser
import subprocess as sub
#
from operator import itemgetter, attrgetter
import imghdr, copy
#
import wx
import wx.lib.buttons as buttons
import flatnotebook as fnb # import my version, hacked to manage colours
from wx.lib.colourutils import AdjustColour as adjust_colour
from wx.lib.colourutils import AdjustColour as adjust_colour
import pylnk3
import icoextract
from icoextract import IconExtractor

#
if __name__ == '__main__':
    print('External Imports for Launcher, not project code imports')
    print('Python', sys.version)
    print('wxPython', wx.version())
