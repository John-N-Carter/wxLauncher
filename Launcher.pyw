#!/usr/bin/env python3.10

"""

launcher.pyw only works with python 3.8, needs upgrading

"""

#version 0.9 - redundant code to be removed and move to python 3
#version 1.0 - uses Python 3

#version 2.0, split into multiple files
#version 2.01 to resolve git merge conflict
# version 2.1 some redundant code removed.

# version 3, use regularly

#version 3.1, replaced super(C, self) with super() to make single inheritance easy.

# wxpython removed using conda and reinstalled using pip to get version 4.1

# version 5. Drag and drop, paste, select/type

"""
To Do:
parse links and eliminate os.startfile

Done:
fix EditCommand

"""

"""
Testing
proc testICO(value : seq[int8]): ImageType =
    # tests: 00 00 01 00
    return if value[0] == 0 and value[1] == 0 and value[2] == 1 and value[3] == 0: ICO else: Other

how to test for icon in some strange language
https://github.com/achesak/nim-imghdr/blob/master/imghdr.nim

imghdr source
https://github.com/python/cpython/blob/main/Lib/imghdr.py


Version 3.2, add clock and list of scores

# version 4

Add cut and paste to create tools.

Lost some code

Safe keeping
        elif newExt == '.dir':
            #~ print('Working on a folder', fullName)
            newType = 'LINK'
            #~ theDefaultIcon = CONST.LINKNAME # default icon
            match = os.path.join(newPath, newName + '.*')
            theIcon = findIcon(match, theDefaultIcon)

        elif newExt == '.eml':
            #~ print('Working on a folder', fullName)
            newType = 'LINK'
            #~ theDefaultIcon = CONST.LINKNAME # default icon
            match = os.path.join(newPath, newName + '.*')
            theIcon = findIcon(match, theDefaultIcon)

        elif newExt in ['.py', '.pyw', '.pyc']:
            newType = 'PYTHON'
            #~ theDefaultIcon = CONST.LINKNAME # default icon
            match = os.path.join(newPath, newName + '.*') #Look for <name>.ico.
            theIcon = findIcon(match, theDefaultIcon)

            newIcon = swapExt(theIcon, newIcon)

New structure to run commands, so all share D&D, clipboard etc.

All button press go to one place, it calls code to run the button. This does

maintains count
checks command exists
checks on drops, paste and link, if allowed. If not ignore and just run command.
takes copy of command an extends it with parameters
runs code as per type

#######################

Links need to be processed and converted to EXEC if possible

#potential promlem with icons '__'

"""

# project imports, not in imports.py to avoid circular imports
# imports.py used  to collect external modules.

from imports import * # Modules used.

import constants as CONST
import code as CODE
from button import *
from getWindowTitles import getWindows


def test_icon(h, f):
    if h.startswith(b'\x00\x00\x01\x00'):
        return 'icon'
    return None

imghdr.tests.append(test_icon) # this runs first to register windows icons.

class DropNewButton(wx.FileDropTarget):

    def __init__(self, master, tab = None):
        self.Tab = tab
        self.Master= master
        super().__init__()
        if tab is None:
            self.Master.ErrorMessage('No tab to drop on', 'Drop error.')
            self.Master.Finish()

    def OnDropFiles(self, x, y, filenames):

        for name in filenames:
            self.Master.NewButton(None, tab = self.Tab.Name, filename = name)
        return True

class RenameDialog(wx.Dialog):
    def __init__(self, master, button):
        self.button = button
        self.Master = master
        self.newname = None
        self.oldname = self.button.Name
        t = f'New name for "{self.button.Name}" button.'
        super().__init__(None, -1, title = t, size = (500, 500))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        textlabel = wx.StaticText(self, -1, t)
        font = wx.Font(wx.FontInfo(16).Bold())
        textlabel.SetFont(font)
        vSizer.Add(textlabel,  0, wx.ALIGN_CENTER)
        hSizer  = wx.BoxSizer(wx.HORIZONTAL)
        textlabel = wx.StaticText(self, -1, 'Name', size = (100, 25))
        font = wx.Font(wx.FontInfo(12).Bold())
        textlabel.SetFont(font)
        hSizer.Add(textlabel)
        self.buttondata = wx.TextCtrl(self, -1, button.Name, size = (500, 25))
        self.buttondata.SetFocus()
        font = wx.Font(wx.FontInfo(12).Bold())
        self.buttondata.SetFont(font)
        hSizer.Add(self.buttondata)
        vSizer.Add(hSizer)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        self.button.Name = self.buttondata.GetValue()
        self.Destroy()
        self.Master.SetFocus()

    def CancelIt(self, a):
        self.Destroy()
        self.Master.SetFocus()

class EditCommandDialog(wx.Dialog):
    def __init__(self, master, button):
        self.Button = button
        self.Master = master
        t = f'New command for "{self.Button.Name}" button.'
        super().__init__(None, -1, title = t, size = (500, 500))
        #buttons
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        linesbutton = wx.Button(self, 0, 'More Lines')
        self.Bind(wx.EVT_BUTTON, self.Lines, linesbutton)
        # command type
        self.typelist = master.ValidTypes
        rbstyle = wx.RA_SPECIFY_COLS
        font = wx.Font(wx.FontInfo(12).Bold())
        textlab = f'Choose an action type for {button.Name} button.'
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, label = textlab, choices = self.typelist, majorDimension = len(self.typelist), style = rbstyle)
        self.radiobox.SetFont(font)
        self.radiobox.SetSelection(self.typelist.index(button.Type))
        textlabel = wx.StaticText(self, -1, t)
        font = wx.Font(wx.FontInfo(16).Bold())
        textlabel.SetFont(font)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(textlabel,  0, wx.ALIGN_CENTER)
        vSizer.Add(self.radiobox)
        # command strings
        self.NumStrings = int(self.Button.Lines)
        self.ButtonData = []
        cmdData = str(self.Button.Command)
        try:
            cmdData = eval(cmdData)
        except:
            sys.exit(F'cmdData {cmdData}')
        for i in range(self.NumStrings):
            hSizer  = wx.BoxSizer(wx.HORIZONTAL)
            if i == 0:
                textlabel = wx.StaticText(self, -1, 'Command', size = CONST.TEXT_TITLE)
            else:
                textlabel = wx.StaticText(self, -1, '', size = CONST.TEXT_TITLE)
            textlabel.SetFont(font)
            hSizer.Add(textlabel)
            try:
                cData = cmdData[i]
            except:
                cData = ''
            buttonData = wx.TextCtrl(self, -1, cData, size = CONST.TEXT_IN)
            buttonData.SetFocus()
            buttonData.SetFont(font)
            hSizer.Add(buttonData)
            self.ButtonData.append(buttonData)
            #~ font = wx.Font(wx.FontInfo(12).Bold())
            vSizer.Add(hSizer)
        self.TextControl = {}
        for Key in CONST.plaintextKeys:
            value = getattr(self.Button, Key, None)
            if Key in CONST.printNames:
                title = CONST.printNames[Key]
            else:
                title = Key
            textlabel = wx.StaticText(self, -1, title, size = CONST.TEXT_TITLE)
            textlabel.SetFont(font)
            buttonData = wx.TextCtrl(self, -1, str(value), size = CONST.TEXT_IN)
            buttonData.SetFocus()
            buttonData.SetFont(font)
            self.TextControl[Key] = buttonData
            tabSizer = wx.BoxSizer(wx.HORIZONTAL)
            tabSizer.Add(textlabel, flag = wx.ALIGN_CENTER)
            tabSizer.Add(buttonData, flag = wx.ALIGN_LEFT)
            vSizer.Add(tabSizer)

        # binaray flags
        self.Control = {}
        for Key in CONST.binaryKeys: # GetValue
            value = getattr(self.Button, Key, None)
            value = CODE.str2bool(value)
            #controled error here
            textlabel = wx.StaticText(self, -1, Key, size = CONST.TEXT_TITLE)
            textlabel.SetFont(font)
            radioButton = wx.CheckBox(self, style = wx.CHK_2STATE)
            radioButton.SetValue(value)
            radioButton.SetFont(font)
            self.Control[Key] = radioButton
            tabSizer = wx.BoxSizer(wx.HORIZONTAL)
            tabSizer.Add(textlabel, flag = wx.ALIGN_CENTER)
            tabSizer.Add(radioButton, flag = wx.ALIGN_LEFT)
            vSizer.Add(tabSizer)
        # count data
        self.oldcount = str(self.Button.Count)
        hSizer  = wx.BoxSizer(wx.HORIZONTAL)
        textlabel = wx.StaticText(self, -1, 'Count', size = CONST.TEXT_TITLE)
        #~ font = wx.Font(wx.FontInfo(12).Bold())
        textlabel.SetFont(font)
        hSizer.Add(textlabel)
        self.countButtonData = wx.TextCtrl(self, -1, self.oldcount, size = CONST.TEXT_IN)
        self.countButtonData.SetFocus()
        #~ font = wx.Font(wx.FontInfo(12).Bold())
        self.countButtonData.SetFont(font)
        hSizer.Add(self.countButtonData)
        vSizer.Add(hSizer)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton, 0, wx.EXPAND)
        hSizer.Add(cancelbutton, 0, wx.EXPAND)
        hSizer.AddStretchSpacer()
        hSizer.Add(linesbutton, 0, wx.EXPAND)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a): # need to read and store
        self.Master.Result = 'F'
        radioResult, commandResult, flagResult, countResult, textResult = [None] * 5
        Result = {}
        # command strings, GetValue
        commandResult = []
        for i in range(self.NumStrings):
            commandResult.append(self.ButtonData[i].GetValue())
        Result[CONST.COMMAND] = commandResult
        # type, getselection -> int, getstring
        radioResult = self.radiobox.GetSelection()
        radioResult = self.radiobox.GetString(radioResult)
        Result[CONST.TYPE] = radioResult
        # flags, self.Control[Key] = ?
        flagResult = {}
        textResult = {}
        for Key in self.Control:
            flagResult[Key] = str(self.Control[Key].GetValue())
            Result[Key] = str(self.Control[Key].GetValue())
        for Key in self.TextControl:
            textResult[Key] = str(self.TextControl[Key].GetValue())
            Result[Key] = str(self.TextControl[Key].GetValue())
        # count result
        countResult = self.countButtonData.GetValue()
        Result[CONST.COUNT] = int(self.countButtonData.GetValue())
        #
        self.Master.Result = C.deepcopy(Result)
        self.Destroy()
        self.Master.SetFocus()

    def Lines(self, a):
        lines = int(self.Button.Lines)
        lines += 1
        self.Button.Lines = str(lines)
        self.Master.Result = True
        self.Destroy()
        self.Master.SetFocus()

    def CancelIt(self, a):
        self.Master.Result = False
        self.Destroy()
        self.Master.SetFocus()

class RenameTabDialog(wx.Dialog):
    def __init__(self, master, tab):
        self.Master = master
        self.thistab = tab
        t = f'New name for "{self.thistab.Name}" tab.'
        super().__init__(None, -1, title = t, size = (500, 500))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        textlabel = wx.StaticText(self, -1, 'New Name', size = (100, 25))
        font = wx.Font(wx.FontInfo(12).Bold())
        textlabel.SetFont(font)
        self.tabdata = wx.TextCtrl(self, -1, self.thistab.Name, size = (500, 25))
        self.tabdata.SetFocus()
        font = wx.Font(wx.FontInfo(12).Bold())
        self.tabdata.SetFont(font)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer  = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(textlabel)
        hSizer.Add(self.tabdata)
        vSizer.Add(hSizer)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        self.thistab.Name = self.tabdata.GetValue()
        self.Destroy()
        self.Master.SetFocus()

    def CancelIt(self, a):
        self.Destroy()
        self.Master.SetFocus()

class TabPropDialog(wx.Dialog):
    def __init__(self, master, tab):
        self.Master = master
        self.thistab = tab
        t = f'New name for "{self.thistab.Name}" tab.'
        super().__init__(None, -1, title = t, size = (500, 500))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        self.thistab.Name = self.tabdata.GetValue()
        self.Destroy()
        self.Master.SetFocus()

    def CancelIt(self, a):
        self.Destroy()
        self.Master.SetFocus()

class MakeNewTabDialog(wx.Dialog):
    def __init__(self, master):
        self.Master = master
        t = 'New tab.'
        super().__init__(None, -1, title = t, size = (500, 500))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        textlabel = wx.StaticText(self, -1, 'New Name', size = (100, 25))
        font = wx.Font(wx.FontInfo(12).Bold())
        textlabel.SetFont(font)
        self.tabdata = wx.TextCtrl(self, -1, '', size = (500, 25))
        self.tabdata.SetFocus()
        font = wx.Font(wx.FontInfo(12).Bold())
        self.tabdata.SetFont(font)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        hSizer  = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(textlabel)
        hSizer.Add(self.tabdata)
        vSizer.Add(hSizer)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        self.Master.Result = self.tabdata.GetValue()
        self.Destroy()
        self.Master.SetFocus()

    def CancelIt(self, a):
        self.Destroy()
        self.Master.SetFocus()


class SelectTabDialog(wx.Dialog):
    def __init__(self, master, textlab = 'Chose a tab'):
        self.Master = master
        t = 'Select a tab.'
        super().__init__(None, -1, title = t, size = (-1, -1))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        self.tablist = master.ValidTabs
        rbstyle = wx.RA_SPECIFY_ROWS
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, label = textlab, choices = master.ValidTabs, majorDimension = len(master.ValidTabs), style = rbstyle)
        self.radiobox.SetSelection(0) # default to start of list
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.radiobox)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        n = self.radiobox.GetSelection()
        self.Master.treeResult = self.tablist[n]
        self.Destroy()

    def CancelIt(self, a):
        self.Destroy()

class NewTabDialog(wx.Dialog):
    def __init__(self, master, button):
        self.button = button
        self.Master = master
        t = 'New Tab.'
        super().__init__(None, -1, title = t, size = (-1, -1))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        self.tablist = master.ValidTabs
        rbstyle = wx.RA_SPECIFY_ROWS
        textlab = f'Choose a new Group for "{button.Name}" button.'
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, label = textlab, choices = self.tablist, majorDimension = len(self.tablist), style = rbstyle)
        self.radiobox.SetSelection(self.tablist.index(button.Tab))
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.radiobox)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        n = self.radiobox.GetSelection()
        self.button.Tab = self.tablist[n]
        self.Destroy()

    def CancelIt(self, a):
        self.Destroy()

class TabChoseDialog(wx.Dialog):
    def __init__(self, title, tabname, master):
        self.Master = master
        super().__init__(None, -1, title = title, size = (-1, -1))
        okbutton = wx.Button(self, wx.ID_OK, 'OK')
        self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)
        self.tablist = master.ValidTabs
        rbstyle = wx.RA_SPECIFY_ROWS
        textlab = 'Choose a Group.'
        self.radiobox = wx.RadioBox(self, wx.ID_ANY, label = textlab, choices = self.tablist, majorDimension = len(self.tablist), style = rbstyle)
        self.radiobox.SetSelection(self.tablist.index(tabname))
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.radiobox)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(okbutton)
        hSizer.Add(cancelbutton)
        vSizer.Add(hSizer)
        self.SetSizer(vSizer)
        vSizer.Fit(self)

    def DoIt(self, a):
        n = self.radiobox.GetSelection()
        self.Master.treeResult = self.tablist[n] # do this another way
        self.Destroy()

    def CancelIt(self, a):
        self.Master.treeResult = None
        self.Destroy()


class EditDialog(wx.Dialog):
    def __init__(self, button, master, edit = None): # show only
        self.Master = master
        self.Edit = edit
        super().__init__(None, -1, title = f'Show Button {button.Name}', size = (500, 500))
        font12 = wx.Font(wx.FontInfo(12).Bold())
        font15 = wx.Font(wx.FontInfo(15).Bold())
        self.Button = button
        okbutton = wx.Button(self, wx.ID_OK, 'ok')
        okbutton.Bind(wx.EVT_BUTTON, self.DoIt)
        bigSizer = wx.BoxSizer(wx.VERTICAL)
        textlabel = wx.StaticText(self, -1, button.Name.capitalize(), size = (150, 25))
        textlabel.SetFont(wx.Font(wx.FontInfo(15).Bold()))
        bigSizer.Add(textlabel, 0, wx.ALIGN_CENTER)
        tabSizer = wx.GridBagSizer()
        self.Control ={}
        row = 0
        for Key in CONST.textKeys: #GetValue
            value = getattr(self.Button, Key, None)
            value = str(value)
            if Key == 'Command':
                v = eval(value)
                try:
                    v = ' '.join(v)
                except:
                    sys.exit('Fatal Error needs work')
                value = v
            textlabel = wx.StaticText(self, -1, Key, size = (150, 25))
            textlabel.SetFont(font12)
            buttondataT = wx.TextCtrl(self, -1, value, size = (500, 25))
            self.Control[Key] = buttondataT
            buttondataT.SetFont(font12)
            tabSizer.Add((40, 12), pos = (row, 0))
            tabSizer.Add(textlabel, pos = (row , 1), flag = wx.ALIGN_CENTER)
            tabSizer.Add(buttondataT, pos = (row, 2), flag = wx.ALIGN_LEFT)
            row += 1
        for Key in CONST.binaryKeys: # GetValue
            value = CODE.str2bool(getattr(self.Button, Key, None))
            textlabel = wx.StaticText(self, -1, Key, size = (150, 25))
            textlabel.SetFont(font12)
            radioButton = wx.CheckBox(self, label = Key, style = wx.CHK_2STATE)
            radioButton.SetValue(value)
            radioButton.SetFont(font12)
            self.Control[Key] = radioButton
            tabSizer.Add((40, 12), pos = (row, 0))
            tabSizer.Add(textlabel, pos = (row , 1), flag = wx.ALIGN_CENTER)
            tabSizer.Add(radioButton, pos = (row, 2), flag = wx.ALIGN_LEFT)
            row += 1
        for Key in CONST.radioKeys: # getselection int, getstring
            value = getattr(self.Button, Key, None)
            textlabelT = wx.StaticText(self, -1, Key, size = (150, 25))
            textlabelT.SetFont(font12)
            lbList = CONST.radioKeys[Key]
            place = lbList.index(value)
            rbox = wx.RadioBox(self, label = 'Button Type', choices = lbList ,   majorDimension = 1, style = wx.RA_SPECIFY_ROWS)
            rbox.SetSelection(place)
            rbox.SetFont(font12)
            self.Control[Key] = rbox
            tabSizer.Add((40, 12), pos = (row, 0))
            tabSizer.Add(textlabelT, pos = (row, 1), flag = wx.ALIGN_CENTER)
            tabSizer.Add(rbox, pos = (row, 2), flag = wx.ALIGN_CENTER)
            row += 1
        bigSizer.Add(tabSizer)
        Sizer = wx.BoxSizer(wx.HORIZONTAL)
        Sizer.Add(okbutton)
        if self.Edit:
            Sizer.Add(cancelbutton)
        bigSizer.Add(Sizer)
        self.SetSizer(bigSizer)
        bigSizer.Fit(self)

    def DoIt(self, a):
        self.Destroy()

    def CancelIt(self, a):
        self.Destroy()

class TreeDialog(wx.Dialog):
    def __init__(self, master, title, open = None):
        self.Roots = {}
        self.Master  =master
        tabs = self.Master.AllTabs
        super().__init__(None, -1, title)
        self.edit_tree = wx.TreeCtrl(self, size = (500, 500))
        if open is not None:
            open = open.strip()
        root = self.edit_tree.AddRoot('The world')
        for i, k in enumerate(sorted(tabs)):
            child = self.edit_tree.AppendItem(root, k)
            for v in tabs[k].Buttons:
                subchild = self.edit_tree.AppendItem(child, v.Name.strip())
                self.Roots[subchild] = v
            if k == open:
                self.edit_tree.ExpandAllChildren(child)
        self.edit_tree.Expand(root)
        okbt = wx.Button(self, -1, 'Ok')
        canbt = wx.Button(self, -1, 'Cancel')
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.edit_tree)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add((50,20), 1)
        buttonSizer.Add(okbt)
        buttonSizer.Add((50,20), 1)
        buttonSizer.Add(canbt)
        buttonSizer.Add((50,20), 1)
        Sizer.Add(buttonSizer, 0, wx.EXPAND, 10)
        self.SetSizer(Sizer)
        Sizer.Fit(self)
        self.edit_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.doit)
        okbt.Bind(wx.EVT_BUTTON, self.doit)
        canbt.Bind(wx.EVT_BUTTON, self.exit)

    def exit(self,a ):
        self.Master.treeResult = None
        self.Close()

    def doit(self,a ):
        i = self.edit_tree.GetSelection()
        try:
            self.Master.treeResult = self.Roots[i]
        except:
            msg =  'Tree has no solution'
            dlg = wx.MessageDialog(None, msg, 'Nothing!', wx.OK | wx.ICON_ERROR)
            ret = dlg.ShowModal()
            self.Master.Finish()
        self.Close()

class MyMenu():
    def MenuItem(self, Name, Command, Menu = None, Enable = True):
        if Menu is None:
            Menu = self
        menuItem = wx.MenuItem(self,  wx.ID_ANY, Name)
        Menu.Append(menuItem)
        if not Enable:
            menuItem.Enable(False)
        self.Bind(wx.EVT_MENU, Command, menuItem)

class PopMenu(wx.Menu, MyMenu):
    def __init__(self, master, button):
        super().__init__()
        self.Master = master
        self.Button = button
        self.SetTitle(self.Button.Name)
        menuPaste = wx.MenuItem(self,  wx.ID_ANY, 'Paste') # Rename
        self.Append(menuPaste)
        self.Bind(wx.EVT_MENU, Command(self.Master.PasteToButton, None, button = self.Button), menuPaste )
        menuSelect = wx.MenuItem(self,  wx.ID_ANY, 'Select Argument') # Rename
        self.Append(menuSelect)
        self.Bind(wx.EVT_MENU, Command(self.Master.SelectForButton, None, button = self.Button), menuSelect )
        menuType = wx.MenuItem(self,  wx.ID_ANY, 'Type Argument') # Rename
        self.Append(menuType)
        self.Bind(wx.EVT_MENU, Command(self.Master.TypeForButton, None, button = self.Button), menuType )
        #
        activeFolders = getWindows()
        whereMenu = wx.Menu()
        for folder in activeFolders:
            self.MenuItem(folder, Command(self.Master.FastRecordRun, folder = folder), Menu = whereMenu)
        self.AppendSubMenu(whereMenu, 'Run Here')

        #
        self.AppendSeparator()
        #
        menuProp = wx.MenuItem(self,  wx.ID_ANY, f'Show {self.Button.Name}') # List all properties of button, allow edit ?
        self.Append(menuProp)
        self.Bind(wx.EVT_MENU, Command(self.Master.ShowProperty, button = self.Button, editprop = False), menuProp )
        menuRename = wx.MenuItem(self,  wx.ID_ANY, 'Rename') # Rename
        self.Append(menuRename)
        menuRename.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.RenameButton, None, button = self.Button), menuRename )
        menuIcon= wx.MenuItem(self,  wx.ID_ANY, 'New Icon') # Icon
        self.Append(menuIcon)
        menuIcon.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.NewIcon, None, button = self.Button), menuIcon )
        menuCommand = wx.MenuItem(self,  wx.ID_ANY, 'Edit Command') # Command
        self.Append(menuCommand)
        menuCommand.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.EditCommand, None, button = self.Button), menuCommand )
        #
        self.AppendSeparator()
        #
        menuDelete = wx.MenuItem(self,  wx.ID_ANY, 'Delete Current Button') # Delete
        self.Append(menuDelete)
        menuDelete.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.DeleteButton, button = self.Button), menuDelete )
        #
        menuTab = wx.MenuItem(self,  wx.ID_ANY, 'Move to New Tab') # Tab
        self.Append(menuTab)
        menuTab.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.MoveToNewTab, None, button = self.Button), menuTab )
        #
        menuTab = wx.MenuItem(self,  wx.ID_ANY, 'Copy to New Tab') # List all properties of button, allow edit ?
        self.Append(menuTab)
        menuTab.Enable(not self.Master.IsBest)
        self.Bind(wx.EVT_MENU, Command(self.Master.CopyToNewTab, None, button = self.Button), menuTab )
        #
        self.AppendSeparator()
        #
        menuExit = wx.MenuItem(self,  wx.ID_ANY, 'Exit') # Exit with choice
        self.Append(menuExit)
        self.Bind(wx.EVT_MENU, self.Master.FinishOK, menuExit)



class PopMenuTab(wx.Menu, MyMenu):
    def __init__(self, master, tab):
        super().__init__()
        self.Master = master
        self.Tab = tab
        self.tabName = self.Tab.Name
        isFrequent = (self.tabName == CONST.MOST_POPULAR)
        self.SetTitle(self.tabName)
        if not isFrequent:
            numberButtons = len(self.Tab.Buttons)
            if numberButtons > CONST.PER_ROW:
                for button in self.Tab.Buttons[CONST.PER_ROW:]:
                    self.MenuItem(button.Name, button.CommandData)
            #
                self.AppendSeparator()
            #
        self.MenuItem('Run a Button', self.Master.Run)
        if not isFrequent:
            self.MenuItem('Delete a Butten',  Command(self.Master.SelectDeleteButton, None, tab = self.tabName))
            self.MenuItem('New Button Here', Command(self.Master.SelectNewButton, None, tab = self.tabName))
            self.MenuItem('Paste Button Here', Command(self.Master.PasteButton, None, tab = self.tabName))
            #
            self.AppendSeparator()
            #
            self.MenuItem('Select a Tab', Command(self.Master.SelectATab, None))
            menuNewTab = wx.MenuItem(self,  wx.ID_ANY, 'New Tab')
            self.Append(menuNewTab)
            menuNewTab.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.MakeNewTab, None), menuNewTab)
            menuRenameTab = wx.MenuItem(self,  wx.ID_ANY, 'Rename this tab')
            self.Append(menuRenameTab)
            menuRenameTab.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.RenameTab, None, tab = self.tabName), menuRenameTab)
            self.MenuItem('Delete this Empty Tab', Command(self.Master.DeleteEmptyTab, None), Enable = len(tab.Buttons) == 0)
            #
            self.AppendSeparator()
            #
        sysMenu = wx.Menu()
        self.MenuItem('Very Fast Exit (No update .ini)', self.Master.FastFinish, Menu = sysMenu)
        self.MenuItem('Fast Exit', self.Master.Finish, Menu = sysMenu)
        self.MenuItem('Edit .ini file', self.Master.EditIni, Menu = sysMenu)
        self.MenuItem('Update', self.Master.Update, Menu = sysMenu)
        self.MenuItem('Disable Vanish' if self.Master.DoVanish else 'Enable Vanish', self.Master.SetVanish, Menu = sysMenu)
        self.MenuItem('Restart', self.Master.Restart, Menu = sysMenu)
        self.AppendSubMenu(sysMenu, 'System')
        self.MenuItem('Exit', self.Master.FinishOK)

    #~ def MenuItem(self, Name, Command, Menu = None, Enable = True):
        #~ if Menu is None:
            #~ Menu = self
        #~ menuItem = wx.MenuItem(self,  wx.ID_ANY, Name)
        #~ Menu.Append(menuItem)
        #~ if not Enable:
            #~ menuItem.Enable(False)
        #~ self.Bind(wx.EVT_MENU, Command, menuItem)

class Command:
    def __init__(self, callback, *args, **kwargs): # Use this in place of lamda
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args):
        return self.callback( *self.args, **self.kwargs) # python 3 specific


class EmptyTabPanel(wx.Panel):
    def __init__(self, parent, master, tab, size = (-1, -1)):
        super().__init__(parent, size = size)
        self.Master = master
        self.Tab = tab
        self.Bind(wx.EVT_CONTEXT_MENU, Command(self.Master.TabContextMenu, None, Tab = self.Tab.Name), self)
        self.NotebookTabSizer = wx.GridBagSizer(hgap = 10)
        IconData = self.Master.IconData
        for i in range(CONST.PER_ROW):  # buttons in tabs
            j = 0
            k = i
            box = buttons.GenBitmapButton(self, -1, IconData, style = wx.BORDER_NONE)
            text = wx.StaticText(self, -1, str(i), style = wx.BORDER_NONE | wx.ST_ELLIPSIZE_END)
            text.Wrap(20)
            text.SetForegroundColour('white')
            self.Tab.addPlaces(box, text)
            self.NotebookTabSizer.Add(box, pos = (j + 0, k), flag = wx.ALIGN_CENTER)
            self.NotebookTabSizer.Add(text, pos = (j + 1, k), flag = wx.ALIGN_CENTER)
        self.SetSizer(self.NotebookTabSizer)
        self.NotebookTabSizer.Fit(parent)
        self.NotebookTabSizer.Layout()

class MyFrame2(wx.Frame): # what do empty tabs looklike
    def __init__(self, root, master, title, pos):
        super().__init__(None, title= CONST.NAME_STRING, pos = pos, style = wx.BORDER_NONE)
        self.Master = master
        self.other = None
        self.RebuildFlag = False
        self.Bind(wx.EVT_ENTER_WINDOW, self.swap)
        box = buttons.GenButton(self, -1, 'wxLauncher', size = (CONST.myWidth, 20))
        box.SetBackgroundColour('black')
        box.SetForegroundColour('white')
        box.Bind(wx.EVT_BUTTON, self.swap)        # all fails when draging.
        box.Bind(wx.EVT_ENTER_WINDOW, self.swap)
        box.Bind(wx.EVT_MOUSE_EVENTS, self.swap)
        self.aStyle = fnb.FNB_NO_X_BUTTON # fnb.FNB_NAV_BUTTONS_WHEN_NEEDED # | fnb.FNB_TABS_BORDER_SIMPLE
        self.aStyle = self.aStyle | fnb.FNB_COLOURFUL_TABS # | fnb.FNB_DROPDOWN_TABS_LIST
        self.aStyle = self.aStyle | fnb.FNB_VC8 | fnb.FNB_NO_NAV_BUTTONS
        self.tabControl = fnb.FlatNotebook(self, -1, size = (CONST.myWidth, -1), agwStyle = self.aStyle)
        self.tabControl.SetTabAreaColour('black')
        self.tabControl.Bind(wx.EVT_ENTER_WINDOW, self.swap)
        for pageindex, t in enumerate(self.Master.AllTabs): # export labels and sort, t is key
            tabName =  self.Master.AllTabs[t].Name # long way making it clear
            if 'System' in t:
                continue
            else:
                pass
            atab = wx.Panel(self.tabControl) # Use Panel not frame
            atab.SetBackgroundColour('black')
            self.tabControl.AddPage(atab, tabName)
            self.tabControl.SetPageTextColour(pageindex, 'black')
            self.tabControl.SetPageColour(pageindex, master.TabColours[pageindex])

        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(self.tabControl)
        Sizer.Add(box)
        self.SetSizer(Sizer)
        Sizer.Fit(self)

    def swap(self, a):
        if self.RebuildFlag:
            self.Hide()
            self.other = MyFrame(self.Master, NAME_STRING, (CONST.myPosition, 0))
            self.other.other = self # ?
            self.other.Layout()
            self.other.Show()
        else:
            self.Hide()
            pa = self.tabControl.GetSelection()
            self.other.tabControl.SetSelection(pa)
            self.other.Layout()
            self.other.Show()
        self.RebuildFlag = False

class MyFrame(wx.Frame):
    def __init__(self, root, title, pos):
        global ExitFlag
        ExitFlag = False
        self.Root = root
        self.master = self # master used in external clases
        self.treeResult = None # used by treees to return results
        self.Result = None
        self.Edited = False
        self.AllButtons = []
        self.AllTabs = {}
        self.scriptPath = ''
        self.PageIndex = {}
        self.PagePanel = {}
        self.CurrentSelection = 0
        self.DoVanish = False
        self.TabColours = []
        self.DontUpdate = False
        self.IsBest = False
        self.Score = False
        super().__init__(None, title= CONST.NAME_STRING, pos = pos, style = wx.BORDER_NONE)
        self.Paths() # check all paths
        self.config = configparser.ConfigParser(interpolation = None, allow_no_value=True)
        IconData = wx.Image(CONST.QUERYNAME, wx.BITMAP_TYPE_BMP)  # should cache this
        if IconData.GetWidth() != 48:
            IconData.Rescale(48, 48, quality = wx.IMAGE_QUALITY_HIGH)
        self.IconData = IconData.ConvertToBitmap()
        self.GenerateColours()
        self.setup(None)
        self.MakePanel()

    def GenerateColours(self):
        for i in range(40):
            col = fnb.RandomColour()
            self.TabColours.append(col)

    def Message(self, msg = 'I have no idea', title= 'Warning'):
            dlg = wx.MessageDialog(None, msg, title, wx.OK | wx.ICON_ERROR)
            ret = dlg.ShowModal()

    def ErrorMessage(self, msg = 'Did you seee thr blue screen', title= 'Error'):
            dlg = wx.MessageDialog(None, msg, title, wx.OK | wx.CANCEL | wx.ICON_ERROR)
            ret = dlg.ShowModal()

    #~ @timeout(5, 'Warning timed out') # doesnt work on windows
    def WarningMessage(self, msg = 'I have no idea what the relevance is', title= 'Warning'):
            dlg = wx.MessageDialog(None, msg, title, wx.OK | wx.ICON_WARNING  | wx.CANCEL)
            ret = dlg.ShowModal()

    def InfoMessage(self, msg = 'Something you should no', title= 'Information', timeout = None): # needs timeout!
            dlg = wx.MessageDialog(None, msg, title, wx.OK | wx.CANCEL | wx.ICON_INFORMATION)
            ret = dlg.ShowModal()

    def ButtonProperties(self, a, button): # To be a one shop edit.
        pass

    def TabProperties(self, a, thisTab): # To be a setconfig  of tab or program
        tabProp = TabPropDialog(self, thisTab)
        pass

    def setup(self, notebook = None): # protect againist bad section
        fp = open(CONST.FULL_INI_PATH, 'r')
        self.config.read_file(fp)
        fp.close()
        try:
            labels = self.config.sections()
            self.ValidTabs = self.config[CONST.SETUP]['Tabs']
        except:
            self.ErrorMessage('Read failed', 'Access config file.')
            sys.exit()
        self.ValidTabs = eval(self.ValidTabs)
        self.ValidTabs.sort()
        self.ValidTabs.insert(0,  CONST.MOST_POPULAR)
        self.ValidTypes = eval(self.config[CONST.SETUP]['types'])
        for vt in self.ValidTabs:
            self.AllTabs[vt] = Tab(vt)
        deleteSection = []
        for section in labels:
            if CONST.SETUP in section or CONST.SYSTEM in section:
                continue
            items = self.config.items(section) # all values as tuple pair.
            items = [(x[0].capitalize(), x[1]) for x in items]
            allOptions = CODE.lt2d(items) # as dictionary
            allKeys = CODE.lt2l(items) # keys.
            if section == '':
                pass
            try:
                name =self.config[section][CONST.NAME]
                if name == None: # bad section so delete, does not seem to work
                    deleteSection.append(section)
                    continue
            except:
                deleteSection.append(section)
                continue
            xb = Button(self, name, section, self.config)
            self.AllButtons.append(xb)
            worst = self.config[section]['worst']
            xb.Worst =CODE.str2bool(worst)
            xb.makeIcon(CONST.ICON_PATH)
            xb.makeCommand(self)
            xb.makeContext(self)
            xb.allKeys = sorted(allKeys)
            xb.allOptions = allOptions
            xb.TabInstance = self.AllTabs[xb.Tab]
            self.AllTabs[xb.Tab].addButton(xb)
        if deleteSection: # delet and warns of any bad sections found.
            for s in deleteSection: # is invoked on empty list
                self.config.remove_section(s)
            self.Edited = True
            bad = ', '.join(deleteSection)
            self.WarningMessage(F'Bad section(s) found {bad}', 'Setup')

    def MakePanel(self):
        self.panel =wx.Panel(self, wx.ID_ANY, style = wx.BORDER_NONE)
        self.butt = wx.Button(self.panel, -1, CONST.NAME_STRING, size = ( CONST.myWidth, 20), style = wx.BORDER_NONE)
        self.butt.SetBackgroundColour('black')
        self.butt.SetForegroundColour('white')
        self.Bind(wx.EVT_BUTTON,  self.Vanish, self.butt)
        self.butt.Bind(wx.EVT_LEAVE_WINDOW, self.Vanish, self.butt)
        self.Debug = False
        self.panelSizer= wx.BoxSizer(wx.VERTICAL)
        if self.Debug:
            butExit = wx.Button(self, -1, 'Exit')
            self.Bind(wx.EVT_BUTTON,  self.Finish, butExit)
            butRecycle = wx.Button(self, -1, 'Use for testing.')
            self.Bind(wx.EVT_BUTTON,  self.Test, butRecycle)
            butEdit = wx.Button(self, -1, 'Re Sync Slowly.')
            self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.topSizer.Add((50,15), 1)
            self.topSizer.Add(butExit)
            self.topSizer.Add((50,15), 1)
            self.topSizer.Add(butRecycle)
            self.topSizer.Add((50,15), 1)
            self.topSizer.Add(butEdit)
            self.topSizer.Add((50,15), 1)
            self.panelSizer.Add(self.topSizer, 0, wx.EXPAND, 0)
        self.noteSizer = wx.BoxSizer(wx.VERTICAL)
        self.aStyle = fnb.FNB_NO_X_BUTTON | fnb.FNB_COLOURFUL_TABS | fnb.FNB_VC8 | fnb.FNB_NO_NAV_BUTTONS
        self.tabControl = fnb.FlatNotebook(self.panel, -1, size = (CONST.myWidth, CONST.myHeight), style = wx.BORDER_NONE, agwStyle = self.aStyle)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.ChangeNotebookTab, self.tabControl)
        self.SetGui()
        indexnet = self.ValidTabs.index( CONST.MOST_POPULAR)
        self.tabControl.SetSelection(indexnet) # default is 'Net'
        self.tabControl.SetTabAreaColour('black')
        self.noteSizer.Add(self.tabControl, flag = wx.ALIGN_CENTER, border = 0)
        self.noteSizer.Add(self.butt, flag = wx.ALIGN_CENTER, border = 0)
        self.SetSizer(self.noteSizer)
        self.noteSizer.Fit(self)
        self.panelSizer.Add(self.panel, 0, wx.ALL, 0)
        self.SetSizer(self.panelSizer)
        self.panelSizer.Fit(self)
        self.Layout()

    def ChangeNotebookTab(self, a):
        self.ActiveTabColour = self.tabControl.GetActiveTabColour()
        self.CurrentActiveTab = self.tabControl.GetCurrentPage()
        tab = self.CurrentActiveTab.Tab
        self.IsBest = False
        if tab.Name ==  CONST.MOST_POPULAR:
            self.IsBest = True
            self.bestButtons = sorted(self.AllButtons, key=attrgetter('Count'), reverse = True)
            self.bestButtons = [x for x in self.bestButtons if not x.Worst]
            tab.Buttons = self.bestButtons[:15]
            tab.Populate(self)

    def Test(self, a):
        for i, info in enumerate(self.tabControl._pages._pagesInfoVec):
            pass

    def SetGui(self):
        for pageindex, tab in enumerate(self.AllTabs.values()): # export labels and sort, t is an instance of  Tab
            self.MakeTab(pageindex, tab)

    def MakeTab(self, pageindex, tab):
        atab = EmptyTabPanel(self.tabControl, self, tab, size = (CONST.myWidth, CONST.myHeight)) # Use Panel not frame
        atab.SetBackgroundColour(adjust_colour(self.TabColours[pageindex], -50))
        self.PageIndex[tab] = pageindex
        self.PagePanel[tab] = atab
        self.tabControl.AddPage(atab, tab.Name) # add page number to dict with name as key.
        dr = DropNewButton(self, tab)
        atab.SetDropTarget(dr)
        tab.Hide()
        tab.Populate(self)
        tab.Show()
        self.tabControl.SetPageTextColour(pageindex, 'black')
        self.tabControl.SetPageColour(pageindex, self.TabColours[pageindex])

    def Paths(self):
        try:
            a = sys.argv[0]
        except:
            a = ''
        a = os.path.abspath(a) # update to get absolute path
        scriptPath, prog = os.path.split(a)
        if scriptPath == '':
            scriptPath = '.\\'
        self.scriptPath = scriptPath

    def Run(self, a, open = None):
        self.open = open
        self.edittree = TreeDialog(self, 'Choose Button to Run.', open = self.open)
        result = self.edittree.ShowModal()
        self.edittree.Destroy()
        if self.treeResult is not None:
            self.treeResult.CommandData(self) # explictitly calling lamnda
        else:
            self.WarningMessage('Nothing Selected to Run', 'Choose Button to run')

    def Edit(self, a, open = None): # a is a place holder for evemts.
        title = 'Chose to Button to Edit.'
        self.edittree = TreeDialog(self, title, open = open)
        temp = self.edittree.ShowModal()
        result = None
        if self.treeResult is None:
            self.WarningMessage('No Button to Edit', title)
        else:
            button = self.treeResult
            editbox = EditDialog(button, self)
            result = editbox.ShowModal()
            editbox.Destroy()
            self.EditConfig(button, button.Section)
            button.TabInstance.Populate(self)
            self.Edited = True

    def SelectDeleteButton(self, a, tab = None): # a is a place holder for evemts.
        if tab is None:
            self.ErrorMesssage(msg = 'Bad Error')
            self.FinishOK()
            return
        self.edittree = TreeDialog(self, 'Chose a Button to Deletee.', open = tab)
        result = self.edittree.ShowModal()
        if self.treeResult is None:
            self.WarningMessage('Nothing Selected to Delete',  'Delete Button')
        else:
            button = self.treeResult # dont like this, but cant think of better - use method in master
            self.DeleteButton(button = button)
            self.Edited = True

    def PasteButton(self, a, tab = None):
        # Read some text
        fileData = wx.FileDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(fileData)
            wx.TheClipboard.Close()
        if success:
            listFiles = fileData.GetFilenames()
        else:
            listFiles = [None]
        for fn in listFiles:
            self.NewButton(a, tab = tab, filename = fn)

    def  NewButton(self, a, tab = None, filename = None): # tab is object, a is event place holder, tab.Name is a name
        # Consider image file, wp files (all libre office)
        import pylnk3
        import icoextract

        def getIconFromIconsExt(iconfile, newname, default):
            iconExtract = CONST.ICONSEXT
            if iconExtract is None:
                self.WarningMessage(msg = 'Install IconsExt so Icon extraction works', title= 'Create NewButton')
                # add to launcher.ini
                return
            iconCmd = F'{iconExtract} /save {iconfile} {CONST.ICONCACHE} -icons'
            iconCmdList = iconCmd.split()
            ret = sub.run(iconCmdList) # must wait till process finishes
            match = F'{newname}*.ico'
            fullmatch = os.path.join(CONST.ICONCACHE, match)
            iconFiles = glob.glob(fullmatch)
            if iconFiles:
                iconFile = iconFiles[0]
            else:
                iconFile = theDefaultIcon
            return iconFile

        def findIcon(a, default = CONST.QUERYNAME):
            found = glob.glob(a)
            for fo in found:
                if imghdr.what(fo):
                    return fo
            return default

        def  getIconFrom(source, index, name = 'temporary.ico'):
            from icoextract import IconExtractor
            name = os.path.expandvars(name)
            if os.path.exists(name):
                os.remove(name)
            getIcon = IconExtractor(source)
            res = getIcon.export_icon(name, index) # alway take first, asume its an .ico
            theIcon = name
            return theIcon

        def swapExt(a, b): #a.ext -> b.ext
            aN, aE = os.path.splitext(a)
            bN, bE = os.path.splitext(b)
            return bN + aE

        if tab is None:
            self.ErrorMessage('Really Bad error, no Tab', 'Create New Buttton')
            self.FinishOK()
            return
        if filename is None:
            self.ErrorMessage('Really Bad error, no Name', 'Create New Buttton')
            self.FinishOK()
            return
        tempFile = os.path.expandvars(filename)
        fullName = os.path.abspath(tempFile)
        newPath, newName, newExt = CODE.getFileName(fullName)
        #
        if os.path.isdir(fullName):
            newExt = '.dir' # this forces treatment of folders
        #
        newExt = newExt.lower()
        try: # check Tab
            thisTab = self.AllTabs[tab]
        except:
            self.ErrorMessage(F'Really Bad error, unknown Tab {tab}', 'Create New Buttton')
            self.FinishOK()
            return
        newSection = f'{thisTab.Name}.{newName}'
        try: # create section, check and delete
            self.config.add_section(newSection) #Must be removed if error later
        except:
            self.WarningMessage(F'Section or command {newSection} exists', 'Create New Buttton')
            return #Return with out doing anything
        if newExt in ['.lnk', 'url']: # copy all link types
            newFileName = os.path.join(CONST.SHORTCUTPATH, newName + newExt) # thing to execute
            if os.path.exists(newFileName):
                os.remove(newFileName)
            shutil.copy(fullName, newFileName)
        else:
            newFileName  = fullName
        newCommand = f"['{newFileName}']"
        newIcon = os.path.join(CONST.ICON_PATH, F'{newName}_{thisTab.Name}.ico')
        match = os.path.join(CONST.DEFAULTICONS, newExt[1:] + '.png')
        if os.path.exists(match):
            theDefaultIcon = match
        else:
            theDefaultIcon = CONST.LINKNAME # default icon
        if newExt == '.lnk': # parse link, result is .ico
            newType = 'LINK'
            if os.path.exists(newIcon): # delete new icon if it exists
                os.remove(newIcon)
            try: # parsing link
                parseLnk = pylnk3.parse(newFileName)
                iconFile = parseLnk.icon
                iconIndex = parseLnk.icon_index
                if iconFile is None:
                    match = os.path.join(newPath, newName + '.*')
                    iconFile = findIcon(match, theDefaultIcon)
                else:
                    iconFile =getIconFrom(iconFile, iconIndex)
                #~ print(iconFile)
                if not imghdr.what(iconFile): # imghdr does not support .ico files, yet. Extension added.
                    self.WarningMessage(msg = F'{iconFile} not image', title= 'Create NewButton')
                    theIcon = theDefaultIcon # Use default icon if not image
                else:
                    theIcon = iconFile
                #~ print(iconFile, iconIndex)
            except icoextract.NoIconsAvailableError as inst: # get icons with iconsExtract
                theIcon = getIconFromIconsExt(iconFile, newName, theDefaultIcon)
            except Exception as inst:
                et, ef, el = CODE.decodeException()
                s = str(inst)
                summary = F'{s} in {ef}:{el}'
                self.WarningMessage(msg = summary, title= 'Create NewButton')
                # use default icon if error
                match = os.path.join(newPath, newName + '.*')
                theIcon = findIcon(match, theDefaultIcon)

        elif newExt == '.url': # parse url link
            newType = 'LINK'
            try: # get files from .URL file, assume exception if not there.
                urlParser = configparser.ConfigParser(interpolation = None)
                with open(newFileName, 'r') as urlFile:
                    urlParser.read_file(urlFile)
                url = urlParser['InternetShortcut']['url']
                iconIndex =  urlParser['InternetShortcut']['IconIndex']
                newIconFile =  urlParser['InternetShortcut']['IconFile'].lower()
            except:
                newIconFile = theDefaultIcon
                iconIndex = 0
                self.config.remove_section(newSection)
                self.WarningMessage(F'Icon informatio Not Found in {newFileName}', 'Create New Buttton')

            if imghdr.what(newIconFile):                                           # imghdr does not support .ico files, yet, fixed
                theIcon = newIconFile
            else:                                                                       #  not imghdr.what(newIconFile):
                try:
                    theIcon =getIconFrom(newIconFile, iconIndex)
                except icoextract.NoIconsAvailableError as inst:    # get icons with iconsExtract
                    summary = str(inst)
                    theIcon = getIconFromIconsExt(newIconFile, newName, theDefaultIcon)
                except Exception as inst:
                    summary = str(inst)
                    self.WarningMessage(msg = summary, title= 'Create NewButton')
                    match = os.path.join(newPath, newName + '.*')
                    theIcon = findIcon(match, theDefaultIcon)

        elif newExt in ['.bat', '.dir', '.eml', '.py', '.pyw', '.pyc']:  #ignore .bat, eventually look for NAME.ico in same place
            newType = 'LINK'
            match = os.path.join(newPath, newName + '.*')
            theIcon = findIcon(match, theDefaultIcon)

        elif newExt in ['.exe']:
            newType = 'EXEC'
            try:
                iconIndex = 0
                theIcon =getIconFrom(newFileName, iconIndex)
            except icoextract.NoIconsAvailableError as inst:    # get icons with iconsExtract
                summary = str(inst)
                theIcon = getIconFromIconsExt(newFileName, newName, theDefaultIcon)
            except Exception as inst:
                summary = str(inst)
                self.WarningMessage(msg = summary, title= 'Create NewButton')
                match = os.path.join(newPath, newName + '.*')
                theIcon = findIcon(match, theDefaultIcon)

        elif 'http:' or 'https:' in newFileName:
            newType = 'LINK'
            match = os.path.join(newPath, newName + '.*') #Look for <name>.ico.
            theIcon = findIcon(match, theDefaultIcon)

        else:
            self.WarningMessage(f'Dont Understand dropped extension - {newFileName}', 'Create New Button')
            self.config.remove_section(newSection)
            return

        newIcon = swapExt(theIcon, newIcon)

        if os.path.exists(newIcon):
            os.remove(newIcon)
        shutil.copy(theIcon, newIcon)
        theIcon = newIcon
        newGroup = thisTab.Name
        self.config.set(newSection, 'name', newName)
        self.config.set(newSection, 'tab', newGroup)
        b = Button(self, newName, newSection, self.config)
        self.AllButtons.append(b) # used to count button access.
        b.Tab = thisTab.Name
        b.TabInstance = thisTab
        b.Icon = theIcon
        b.makeIcon()
        b.Type = newType
        b.Command = newCommand
        b.makeCommand(self)
        b.makeContext(self)
        items = self.config.items(newSection) # all values as tuple pair.
        items = [(x[0].capitalize(), x[1]) for x in items]
        b.allOptions = CODE.lt2d(items) # as dictionary
        b.allKeys = CODE.lt2l(items) # keys.
        thisTab.addButton(b)
        thisTab.Hide()
        thisTab.Populate(self)
        thisTab.Show()
        self.tabControl.SetSelection(self.PageIndex[thisTab]) # causes a slight blip
        self.EditConfig(b, b.Section)
        self.Edited = True
        self.Refresh()

    def SelectNewButton(self, a, tab = None): # a is a place holder for evemts, tab is a name
        if tab is None:
            self.WarningMessage('No tab Selected', 'Select New Button')
            return
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        with wx.FileDialog(self, 'Open Bitmap File', style = style, defaultDir = CONST.LOCALPATH) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.WarningMessage('Nothing Selected', 'Select button')
                return
            command = fileDialog.GetPath()

        self.NewButton(None, tab = tab, filename = command) # need to get a file name

    def DeleteEmptyTab(self, a): # a is event place holder
        tabid = self.tabControl.GetSelection()
        oldname = self.tabControl.GetPageText(tabid)
        thistab = self.AllTabs[oldname]
        legalname = thistab.LegalName
        if len(thistab.Buttons) != 0:
            self.WarningMessage('This tab still has buttons.', 'Delete Tab')
            return
        self.AllTabs.pop(oldname) # delete entry from allTabs
        self.ValidTabs.remove(oldname) #delete name from ValidTabs and update SETUP
        self.config[CONST.SETUP]['Tabs'] = str(self.ValidTabs)
        self.config.remove_option(CONST.SETUP, legalname)
        self.Edited = True
        self.tabControl.DeletePage(tabid)  #delete tab from self.tabControl
        self.tabControl.SendSizeEvent()
        self.Refresh()

    def RenameTab(self, a, tab = None): # a is a place holder for evemts, tab is a name, rename this tab
        tabid = self.tabControl.GetSelection()
        oldname = self.tabControl.GetPageText(tabid)
        thistab = self.AllTabs[oldname]
        dlg = RenameTabDialog(self, thistab)
        dlg.ShowModal()
        if thistab.Name == oldname:
            return
        newname = thistab.Name
        self.tabControl.SetPageText(tabid, newname)
        self.ValidTabs.remove(oldname)
        self.ValidTabs.append(newname)
        self.config[CONST.SETUP]['Tabs'] = str(self.ValidTabs)
        for b in thistab.Buttons:
            b.Tab = newname
            self.config[b.Section][CONST.TAB] = b.Tab
        self.Edited = True

    def MakeNewTab(self, a): # a is a place holder for evemts, new tab
        #does not work properly, fails to redraw screen.
        dlg = MakeNewTabDialog(self)
        dlg.ShowModal()
        self.Freeze()
        newname = self.Result
        tab = Tab(newname)
        pageindex = len(self.ValidTabs) # will be the last one
        self.ValidTabs.append(tab.Name)
        self.config[CONST.SETUP]['Tabs'] = str(self.ValidTabs)
        self.config[CONST.SETUP][tab.LegalName] = f'{tab.Format}'
        atab = EmptyTabPanel(self, self, tab, size = (CONST.myWidth, CONST.myHeight)) # Use Panel not frame
        atab.SetBackgroundColour(adjust_colour(self.TabColours[pageindex], -50))
        self.tabControl.AddPage(atab, tab.Name) # add page number to dict with name as key.
        self.tabControl.SetPageTextColour(pageindex, 'red')
        self.tabControl.SetPageColour(pageindex, self.TabColours[pageindex])
        self.PageIndex[tab] = pageindex
        self.PagePanel[tab] = atab
        dt = DropNewButton(self, tab)
        atab.SetDropTarget(dt)
        tab.Hide()
        tab.Populate(self)
        tab.Show()
        self.AllTabs[tab.Name] = tab
        self.tabControl.SendSizeEvent()
        self.panelSizer.Fit(self)
        self.Layout()
        self.Edited = True
        self.Thaw()

    def NewIcon(self, a, button = None): # a is placeholder for event stuff
        # change how icons are named
        wc = 'Bitmap files (.bmp)|.bmp|PNG Files (.png)|.png' # format problem
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        with wx.FileDialog(self, 'Open Bitmap File', style = style, defaultDir = './icons') as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            icon = fileDialog.GetPath()
            junk, exc = os.path.splitext(icon)
            newname = f'{button.Section}__{button.Name}{exc}' # remove '__', need to fix .ini file and icon file
            newpath = os.path.join(CONST.ICONPATH, newname)
            if not os.path.exists(newpath):
                shutil.copy(icon, newpath)
            button.Icon = newname
            button.makeIcon(CONST.ICONPATH)
        t = button.TabInstance
        t.Hide()
        t.Populate(self)
        t.Show()
        self.EditConfig(button, button.Section)
        self.Edited = True

    def SelectATab(self, a): # need to set selection on notebook
        box = SelectTabDialog(self, 'Chose a Tab')
        result = box.ShowModal()
        choice = self.treeResult
        ind = self.ValidTabs.index(choice)
        self.tabControl.SetSelection(ind)
        self.tabControl.EnsureVisible(ind)

    def MoveToNewTab(self, a, button = None): # a is placeholder for event stuff, delete button from current group and redraw
        oldTabName = button.Tab
        box =NewTabDialog(self, button)
        result = box.ShowModal()
        currentTab = self.AllTabs[oldTabName]
        currentTab.Buttons.remove(button)
        currentTab.Hide()
        currentTab.Populate(self)
        currentTab.Show()
        newTab = self.AllTabs[button.Tab]
        newTab.addButton(button)
        newTab.Hide()
        newTab.Populate(self)
        newTab.Show()
        self.EditConfig(button, button.Section) # section name does not reflect new tab
        self.Edited = True

    def CopyToNewTab(self, a, button = None): # a is placeholder for event stuff
        oldTabName = button.Tab
        box =NewTabDialog(self, button)
        result = box.ShowModal()
        button.Section = CODE.get_random_string(5) + '.' + button.Name
        newTab = self.AllTabs[button.Tab]
        newTab.addButton(button)
        newTab.Hide()
        newTab.Populate(self)
        newTab.Show()
        self.config[button.Section] = {}
        self.config[button.Section]['name'] = button.Name
        self.EditConfig(button, button.Section) # section name does not reflect new tab
        self.Edited = True

    def EditCommand(self, a, button = None): # a is placeholder for event stuff
        Button = button
        self.Result = None
        commandbox = EditCommandDialog(self, Button)
        result = commandbox.ShowModal()
        while True:
            if self.Result is True: # rerun dialog with more line
                continue
            elif self.Result is False: # cancel, so return
                return
            else:
                break
        #
        for Key in self.Result:
            setattr(Button, Key, self.Result[Key])
        #
        Button.makeCommand(self)
        Button.dump(' ----------- After Commmand Edit -----------')
        Tab = Button.TabInstance
        self.Bind(wx.EVT_BUTTON, Button.CommandData, Tab.iconImage[Button.Position])
        self.Bind(wx.EVT_CONTEXT_MENU, Button.ButtonContextData, Tab.iconImage[Button.Position])
        self.EditConfig(Button, Button.Section)
        self.Edited = True

    def EditCount(self, a, button = None, text = None): # a is placeholder for event stuff
        countbox = CountDialog(self, button)
        result = countbox.ShowModal()
        t = button.TabInstance
        t.Populate(self) # number of buttons does not change, so no need to do hide and show
        self.EditConfig(button, button.Section)
        self.Edited = True

    def RenameButton(self, a, button = None, text = None): # a is placeholder for event stuff
        renamebox = RenameDialog(self, button)
        result = renamebox.ShowModal()
        button.TabInstance.Populate(self)
        self.EditConfig(button, button.Section)
        self.Edited = True

    def Temporary(self, a, button = None): # a is placeholder for event stuff
        pass

    def DeleteButton(self, button = None):
        if button is None:
            self.WarningMesssage('Nothing to delete', 'Delete Button')
            return
        if button not in self.AllButtons:
            self.WarningMesssage(F'Buton {button.Name} may already have been deleted', 'Delete Button')
            return
        msg = f'Delete {button.Name} from {button.Tab}'
        dlg = wx.MessageDialog(None, msg, F'Delete this button {button.Name}', wx.YES_NO)
        ret = dlg.ShowModal()
        if ret != wx.ID_YES:
            return
        self.AllButtons.remove(button)
        tab = button.TabInstance
        tab.deleteButton(button)
        tab.Hide()
        tab.Populate(self)
        tab.Show()
        ret = self.config.remove_section(button.Section) # Use section name here
        self.Edited = True # This is crucial

    def ShowProperty(self, button = None, editprop = None):
        editbox = EditDialog(button, self, edit = editprop)
        result = editbox.ShowModal()
        editbox.Destroy()
        self.Edited = False

    def EditProperty(self, button = None, editprop = None):
        editbox = EditDialog(button, self, edit = editprop)
        result = editbox.ShowModal()
        editbox.Destroy()
        self.Edited = False
        if self.Result is not None:
            for k, v in self.Result.items():
                setattr(button, k, v)
            button.Count = int(button.Count)
            self.Edited = True
        t = button.TabInstance
        t.Hide()
        t.Populate(self)
        t.Show()
        self.EditConfig(button, button.Section)

    def EditConfig(self, button, section):
        print(F'======== Button Name: {button.Name} ========')
        for k in button.allOptions:
            v = getattr(button, k)
            #~ print(k, v)
            self.config.set(section, k.lower(), str(v))

    def Update(self, a):
        #~ print('Updating')
        if self.DontUpdate:
            self.DontUpdate = False
            self.Edited = False
            return
        filename = os.path.join(self.scriptPath, CONST.INIFILE)
        backupfile = filename.replace('.ini', '.ini.backup')
        shutil.copy(filename, backupfile)
        with open(filename, 'w') as configfile:
            self.config.write(configfile)
        self.Edited = False

    def Restart(self, a):
        global ExitFlag
        ExitFlag = True
        self.Finish(None)

    def FastFinish(self, a): #No configuration update
        self.other.Close() # must close spare frame first.
        self.Close()

    def Finish(self, a):
        if self.Edited:
            self.Update(None)
        self.other.Close() # must close spare frame first.
        self.Close()

    def FinishOK(self, a): #a is event rubbish, ignore
        dlg = wx.MessageDialog(None, 'Exit YES or NO', 'Confirm Exit', wx.YES_NO)
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            self.Finish(None)
        else:
            return

    def SetVanish(self, a): # a is event rubish
        if self.DoVanish:
            self.DoVanish = False
        else:
            self.DoVanish = True

    def Vanish(self, a):
        if self.DoVanish:
            self.Hide()
            self.CurrentSelection = self.tabControl.GetSelection()
            self.other.Layout()
            self.other.tabControl.SetSelection(self.CurrentSelection)
            self.other.Show()

    def UpdateConfigFile(self):
        self.Update(None)

    def ButtonContextMenu(self, *a, **b):
        button = b[CONST.BUTTON] # Name of button
        self.popmenu = PopMenu(self, button)
        self.PopupMenu(self.popmenu)

    def TabContextMenu(self, *a, **b):
        tabname = b[CONST.TAB] # Name of tab
        tab = self.AllTabs[tabname]
        self.popmenutab = PopMenuTab(self, tab)
        self.PopupMenu(self.popmenutab)

    def EditIni(self, a, tab = None):
        edit = ['C:\\Programs\\wscite\\SciTE.exe', CONST.FULL_INI_PATH] # put in configuration file
        try:
            pid = sub.Popen(edit).pid
        except:
            self.WarningMessage('sub.Popen failed', 'Edit .Ini Command')
        self.Vanish(None)

    def FastRecordRun(self, folder = None):
        #~ print(folder)
        return

    def AllCommand(self, *a, **b): # b is a dictionary, b[CONST.PROG] should be a list, a is some event data
        prog = copy.deepcopy( b[CONST.PROG])
        button = b[CONST.BUTTON]
        self.RunAllCom(button, prog)

    def RunAllCom(self,  button, prog, parameters = []):
        #
        # use cwd = 'h:\' to set working directory
        #
        button.dump('Running')
        pid = None
        button.Count += 1 # update count in file
        self.config.set(button.Section, 'count', str(button.Count))
        self.Edited = True
        if parameters:
            #~ print(F'Parameters {parameters}')
            prog.extend(parameters)
        else:
            if button.Defaultargument:
                #~ print(F'use default argument {button.Defaultargument}')
                prog.append(button.Defaultargument)
        if button.Type == 'EXEC':
            if CODE.str2bool(button.Elevation):
                c = prog[0]
                ret =ctypes.windll.shell32.ShellExecuteW(None, "runas", c, '', None, 1)
            else:
                try:
                    pid = sub.Popen(prog).pid
                except OSError:
                    self.WarningMessage(f'Needs elevation  {prog}! (Probably.)', f'Run .exe Command')
                except:
                    self.WarningMessage(f'sub.Popen failed  {prog}', f'Run .exe Command')
            self.Vanish(None)
        elif button.Type == 'LINK':
            cmd = prog[0] # ban parameters to link
            try:
                os.startfile(cmd)
            except Exception as inst:
                if not os.path.exists(cmd): # not all exist
                    self.WarningMessage(F'No command Found: {cmd}', 'Run Link Command')
                else:
                    self.WarningMessage(f'Exception {inst} running link - {cmd}', 'Run Link Command')
        elif button.Type == 'PYTHON':
            prog.insert(0, 'C:/programs/Apps/pyw.exe')
            startinfo = sub.STARTUPINFO()
            startinfo.dwFlags |= sub.STARTF_USESHOWWINDOW
            try:
                pid = sub.Popen(prog, startupinfo = startinfo).pid
            except:
                self.ErrorMessage(f'sub.Popen failed  {prog}', f'Run Python Command')
                self.Finish(None)
        else:
            self.ErrorMessage(F'Unknown Commmand: {button.Type}', 'Run Command')
            self.Finish(None)
        self.Vanish(None)

    def SelectForButton(self, a, button = None, text = None):
        wc = '*.*' # format problem
        style=wx.FD_OPEN
        with wx.FileDialog(self, 'Select or Name File', style = style, defaultDir = 'H:/') as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            afile = fileDialog.GetPath()
        files =[afile]
        prog = copy.deepcopy( button.Command)
        self.RunAllCom(button, prog, parameters = files)

    def DropOnButton(self, a, button = None, files = []):
        prog = copy.deepcopy( button.Command)
        self.RunAllCom(button, prog, parameters = files)

    def TypeForButton(self, a, button = None):
        prog = copy.deepcopy(button.Command)
        oneLine = wx.TextEntryDialog(self,  F'Please type a parameter for {button.Name}')
        oneLine.ShowModal()
        param = oneLine.GetValue()
        if param != '':
            self.RunAllCom(button, prog, parameters = [param])

    def PasteToButton(self, a, button = None, text = None):
        fileData = wx.FileDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(fileData)
            wx.TheClipboard.Close()
        if success:
            listFiles = fileData.GetFilenames()
        else:
            listFiles = []
        prog = copy.deepcopy( button.Command)
        self.RunAllCom(button, prog, parameters = listFiles)


def gogui():
    version = ' (Ver 4.00)'
    title='Launcher'
    wx.InitAllImageHandlers()
    app = wx.App()
    frm1 = MyFrame(app, CONST.NAME_STRING, (CONST.myPosition, 0)) # main gui
    frm1.Layout()
    frm2 = MyFrame2(app, frm1, 'Spare', (CONST.myPosition, 0)) # dummy gui
    frm2.Layout()
    frm1.other = frm2
    frm2.other = frm1
    frm1.Show()
    app.MainLoop()

if __name__ == '__main__': # tidy this up
    name = sys.argv[0]
    name = os.path.abspath(name)
    localpath, name = os.path.split(name)
    #
    # over write constants with local path
    #
    CONST.LOCALPATH = localpath
    CONST.ICON_PATH = CONST.ICONPATH = os.path.join(localpath, CONST.ICONPATH) # 'H:\\Computers\\PythonTools\\Launcher\\icons'
    CONST.FULL_INI_PATH = os.path.join(localpath, CONST.INIFILE) #'H:\\Computers\\PythonTools\\Launcher\\' + INI_FILE
    CONST.PICLKEFILE = CONST.FULL_INI_PATH.replace('.ini', '.pickle')
    CONST.ICONCACHE  = os.path.join(localpath, CONST.ICONCACHE)
    #
    # Delete everything in ICONCACHE
    #
    if not os.path.exists(CONST.ICONCACHE):
        os.makedirs(CONST.ICONCACHE)
    match = os.path.join(CONST.ICONCACHE, '*.*')
    found = glob.glob(match)
    for f in found:
        p =os.path.abspath(f)
        os.remove(p)
    #
    CONST.DEFAULTICONS = os.path.join(localpath, CONST.DEFAULTICONS) # default icon path
    CONST.QUERYNAME = os.path.join(CONST.DEFAULTICONS, CONST.QUERYNAME) # default icon
    CONST.LINKNAME = os.path.join(localpath, CONST.DEFAULTICONS, CONST.LINKNAME) # default icon
    CONST.SHORTCUTPATH = os.path.join(localpath, CONST.SHORTCUTPATH)
    if 'PythonTools' in CONST.FULL_INI_PATH: # may require more general test
        CONST.NAME_STRING = 'wxLauncher - Development'
    else:
        CONST.NAME_STRING = CONST.NAME_STRING
    ExitFlag = None
    gogui()
    if ExitFlag:
        os.execl(sys.executable, sys.executable, *sys.argv) # This works as required, taken from internet





