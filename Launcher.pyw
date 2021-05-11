#! python3

#version 0.9 - redundant code to be removed and move to python 3
#version 1.0 - uses Python 3

#version 2.0, split into multiple files
#version 2.01 to resolve git merge conflict
# version 2.1 some redundant code removed.

# version 3, use regularly

#version 3.1, replaced super(C, self) with super() to make single inheritance easy.

# wxpython removed using conda and reinstalled using pip to get version 4.1

""" Version 3.2, add clock and list of scores """

# version 4

from imports import *

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
        
#~ class DummyFileDrop(wx.FileDropTarget):

    #~ def __init__(self, master):
        #~ self.Master= master
        #~ super().__init__()

    #~ def OnDropFiles(self, x, y, filenames):
        #~ return True

#~ class CountDialog(wx.Dialog):
    #~ def __init__(self, master, button):
        #~ self.button = button
        #~ self.newname = None
        #~ self.Master = master
        #~ self.oldcount = str(self.button.Count)
        #~ t = f'New count for"{self.button.Name}" button.'
        #~ super().__init__(None, -1, title = t, size = (500, 500))
        #~ okbutton = wx.Button(self, wx.ID_OK, 'OK')
        #~ self.Bind(wx.EVT_BUTTON, self.DoIt, okbutton)
        #~ cancelbutton = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        #~ self.Bind(wx.EVT_BUTTON, self.CancelIt, cancelbutton)

        #~ vSizer = wx.BoxSizer(wx.VERTICAL)
        #~ textlabel = wx.StaticText(self, -1, t)
        #~ font = wx.Font(wx.FontInfo(16).Bold())
        #~ textlabel.SetFont(font)
        #~ vSizer.Add(textlabel,  0, wx.ALIGN_CENTER)
        
        #~ hSizer  = wx.BoxSizer(wx.HORIZONTAL)
        
        #~ textlabel = wx.StaticText(self, -1, 'Count', size = CONST.S_100_25)
        #~ font = wx.Font(wx.FontInfo(12).Bold())
        #~ textlabel.SetFont(font)
        #~ hSizer.Add(textlabel)
        
        #~ self.buttondata = wx.TextCtrl(self, -1, self.oldcount, size = CONST.S_500_25)
        #~ self.buttondata.SetFocus()
        #~ font = wx.Font(wx.FontInfo(12).Bold())
        #~ self.buttondata.SetFont(font)
        #~ hSizer.Add(self.buttondata)
        
        #~ vSizer.Add(hSizer)
        
        #~ hSizer = wx.BoxSizer(wx.HORIZONTAL)
        #~ hSizer.Add(okbutton)
        #~ hSizer.Add(cancelbutton)
        
        #~ vSizer.Add(hSizer)
        
        #~ self.SetSizer(vSizer)
        #~ vSizer.Fit(self)

        
    #~ def DoIt(self, a):
        #~ temp  = self.buttondata.GetValue()
        #~ self.button.Count = int(temp)
        #~ self.Destroy()
        #~ self.Master.SetFocus()
        
    #~ def CancelIt(self, a):
        #~ self.Destroy()
        
class RenameDialog(wx.Dialog):
    def __init__(self, master, button):
        self.button = button
        self.newname = None
        self.Master = master
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

class CommandDialog(wx.Dialog):
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
        cmdData = button.Command
        cmdData = eval(cmdData)
        for i in range(self.NumStrings): 
            hSizer  = wx.BoxSizer(wx.HORIZONTAL)
            if i == 0:
                textlabel = wx.StaticText(self, -1, 'Command', size = (100, 25))
            else:
                textlabel = wx.StaticText(self, -1, '', size = (100, 25))
            textlabel.SetFont(font)
            hSizer.Add(textlabel)
            try:
                cData = cmdData[i]
            except:
                cData = ''
            buttonData = wx.TextCtrl(self, -1, cData, size = (700, 25))
            buttonData.SetFocus()
            buttonData.SetFont(font)
            hSizer.Add(buttonData)
            self.ButtonData.append(buttonData)
            #~ font = wx.Font(wx.FontInfo(12).Bold())
            vSizer.Add(hSizer)
        # binarty flags
        self.Control = {}
        for Key in CONST.binaryKeys: # GetValue
            #~ value = self.Button.allOptions[Key]
            value = getattr(self.Button, Key, None)
            value = CODE.str2bool(value)
            #controled error here
            print('@@@ binary', Key, value)
            textlabel = wx.StaticText(self, -1, Key, size = (150, 25))
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
        
        textlabel = wx.StaticText(self, -1, 'Count', size = CONST.S_100_25)
        #~ font = wx.Font(wx.FontInfo(12).Bold())
        textlabel.SetFont(font)
        hSizer.Add(textlabel)
        
        self.countButtonData = wx.TextCtrl(self, -1, self.oldcount, size = CONST.S_500_25)
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
        radioResult, commandResult, flagResult, countResult = [None] * 4
        # command strings, GetValue
        commandResult = []
        for i in range(self.NumStrings):
            commandResult.append(self.ButtonData[i].GetValue())
        # type, getselection -> int, getstring
        radioResult = self.radiobox.GetSelection()
        radioResult = self.radiobox.GetString(radioResult)
        # flags, self.Control[Key] = ?
        flagResult = {}
        for Key in self.Control:
            flagResult[Key] = str(self.Control[Key].GetValue())
        # count result
        countResult = self.countButtonData.GetValue()
        #
        self.Master.Result = (radioResult, commandResult, flagResult, countResult)
        self.Destroy()
        self.Master.SetFocus()
        
    def Lines(self, a):
        #~ print('Lines')
        lines = int(self.Button.Lines)
        lines += 1
        self.Button.Lines = str(lines)
        self.Master.Result = 'L'
        self.Destroy()
        self.Master.SetFocus()
        
    def CancelIt(self, a):
        #~ print('Cancel')
        self.Master.Result = 'F'
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
        #~ print('*' * 20, 'Enter Edit Dialog')
        self.Master = master
        self.Edit = edit
        super().__init__(None, -1, title = f'Show Button {button.Name}', size = (500, 500))
        font12 = wx.Font(wx.FontInfo(12).Bold())
        font15 = wx.Font(wx.FontInfo(15).Bold())
        self.Button = button 
        
        button.dump(label = 'Edit Dialog/Show')
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
            value = self.Button.allOptions[Key]
            if Key == 'Command':
                v = eval(value)
                v = ' '.join(v)
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
            value = CODE.str2bool(self.Button.allOptions[Key])
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
            value = self.Button.allOptions[Key]
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
        print('*' * 20, 'Leave Edit Dialog', self.Edit)
        
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
        
class PopMenu(wx.Menu): 
    def __init__(self, master, button): 
        super().__init__() 
        self.Master = master
        self.Button = button
        self.SetTitle(self.Button.Name)
                  
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
        self.Bind(wx.EVT_MENU, Command(self.Master.NewCommand, None, button = self.Button), menuCommand )
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
        
class PopMenuTab(wx.Menu): 
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

        menuRun = wx.MenuItem(self,  wx.ID_ANY, 'Run a Button') 
        self.Append(menuRun)
        menuRun.Enable(True)
        self.Bind(wx.EVT_MENU, Command(self.Master.Run, None, open = self.tabName), menuRun )
        
        if not isFrequent:
            menuDeleteButton = wx.MenuItem(self,  wx.ID_ANY, 'Delete a Butten (sync)')
            self.Append(menuDeleteButton)
            menuDeleteButton.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.SelectDeleteButton, None, tab = self.tabName), menuDeleteButton)
            
            menuNewButton = wx.MenuItem(self,  wx.ID_ANY, 'New Button (sync)')
            self.Append(menuNewButton)
            menuNewButton.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.SelectNewButton, None, tab = self.tabName), menuNewButton)
            
            menuNewButtonHere = wx.MenuItem(self,  wx.ID_ANY, 'New Butten here')
            self.Append(menuNewButtonHere)
            menuNewButtonHere.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.NewButton, None, tab = self.tabName), menuNewButtonHere)
            #
            self.AppendSeparator()
            #
            
            menuSelectTab = wx.MenuItem(self,  wx.ID_ANY, 'Select a Tab')
            self.Append(menuSelectTab)
            menuSelectTab.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.SelectATab, None), menuSelectTab)
            
            menuNewTab = wx.MenuItem(self,  wx.ID_ANY, 'New Tab')
            self.Append(menuNewTab)
            menuNewTab.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.MakeNewTab, None), menuNewTab)
            
            menuRenameTab = wx.MenuItem(self,  wx.ID_ANY, 'Rename this tab')
            self.Append(menuRenameTab)
            menuRenameTab.Enable(True)
            self.Bind(wx.EVT_MENU, Command(self.Master.RenameTab, None, tab = self.tabName), menuRenameTab)
            
            menuDeleteTab = wx.MenuItem(self,  wx.ID_ANY, 'Delete this Empty Tab (sync)')
            self.Append(menuDeleteTab)
            if len(tab.Buttons) == 0:
                menuDeleteTab.Enable(True)
            else:
                menuDeleteTab.Enable(False)
            self.Bind(wx.EVT_MENU, Command(self.Master.DeleteEmptyTab, None), menuDeleteTab)
            
            # 
            self.AppendSeparator()
            #
        sysMenu = wx.Menu()
        self.MenuItem('Fast Exit', self.Master.Finish, Menu = sysMenu)
        self.MenuItem('Edit .ini file', self.Master.EditIni, Menu = sysMenu)
        self.MenuItem('Update', self.Master.Update, Menu = sysMenu)
        if self.Master.DoVanish:
            msg = 'Disable Vanish'
        else:
            msg = 'Enable Vanish'
        self.MenuItem(msg, self.Master.SetVanish, Menu = sysMenu)
        self.MenuItem('Restart', self.Master.Restart, Menu = sysMenu)
        self.AppendSubMenu(sysMenu, 'System')
        self.MenuItem('Exit', self.Master.FinishOK)
        
    def MenuItem(self, Name, Command, Menu = None, Enable = True):
        if Menu is None:
            Menu = self
        menuItem = wx.MenuItem(self,  wx.ID_ANY, Name)
        Menu.Append(menuItem)
        if not Enable:
            menuItem.Enable(False)
        self.Bind(wx.EVT_MENU, Command, menuItem)

        
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
            text = wx.StaticText(self, -1, str(i), style = wx.BORDER_NONE)
            text.SetForegroundColour('white')
            self.Tab.addPlaces(box, text)
            self.NotebookTabSizer.Add(box, pos = (j + 0, k), flag = wx.ALIGN_CENTER)
            self.NotebookTabSizer.Add(text, pos = (j + 1, k), flag = wx.ALIGN_CENTER)
        self.SetSizer(self.NotebookTabSizer)
        self.NotebookTabSizer.Fit(parent)
        self.NotebookTabSizer.Layout()
        
            
class MyFrame2(wx.Frame): # what do empty tabs looklike
    def __init__(self, root, master, title, pos):
        super().__init__(None, title= NAME_STRING, pos = pos, style = wx.BORDER_NONE)
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
        self.ImagePath = ''
        self.ShortcutPath = ''
        self.PageIndex = {}
        self.PagePanel = {}
        self.CurrentSelection = 0
        self.DoVanish = False
        self.TabColours = []
        self.DontUpdate = False
        self.IsBest = False
        self.Score = False
        super().__init__(None, title= NAME_STRING, pos = pos, style = wx.BORDER_NONE)
        self.Paths() # check all paths
        self.config = configparser.ConfigParser()
        queryname = os.path.join(CONST.ICONPATH, 'query.bmp')
        IconData = wx.Image(queryname, wx.BITMAP_TYPE_BMP)  # should cache this
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
        fp = open(os.path.join(self.scriptPath, CONST.INIFILE), 'r')
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
        for section in labels:
            if CONST.SETUP in section or CONST.SYSTEM in section:
                continue
            items = self.config.items(section) # all values as tuple pair.
            items = [(x[0].capitalize(), x[1]) for x in items]
            allOptions = CODE.lt2d(items) # as dictionary
            allKeys = CODE.lt2l(items) # keys.
            name =self.config[section][CONST.NAME]
            xb = Button(self, name, section, self.config)
            self.AllButtons.append(xb)
            #~ drop = self.config[section][CONST.DROP]
            worst = self.config[section]['worst']
            #~ xb.Drop = CODE.str2bool(drop)
            xb.Worst =CODE.str2bool(worst)
            xb.makeIcon(self.ImagePath)
            xb.makeCommand(self)
            xb.makeContext(self)
            xb.allOptions = allOptions
            xb.allKeys = sorted(allKeys)
            xb.TabInstance = self.AllTabs[xb.Tab]
            self.AllTabs[xb.Tab].addButton(xb)
            
    def MakePanel(self):
        self.panel =wx.Panel(self, wx.ID_ANY, style = wx.BORDER_NONE)
        self.butt = wx.Button(self.panel, -1, NAME_STRING, size = ( CONST.myWidth, 20), style = wx.BORDER_NONE)
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
        self.ImagePath = os.path.join(scriptPath, CONST.ICONPATH)
        self.ShortcutPath = os.path.join(scriptPath, CONST.SHORTCUTPATH)
        print('Paths', self.scriptPath, self.ImagePath, self.ShortcutPath)
        
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
            
    def  NewButton(self, a, tab = None, filename = None): # tab is object, a is event place holder, tab.Name is a name
        if tab is None:
            self.ErrorMessage('Really Bad error', 'Create New Buttton')
            self.FinishOK()
            return
        fullName = filename
        thisTab = self.AllTabs[tab]
        if fullName is None:
            newName = '0' + CODE.get_random_string(5) 
            newPath = None
            newExt = '.lnk'
        else:
            newPath, newName, newExt = CODE.getFileName(filename)
            newFileName = os.path.join(self.ShortcutPath, newName + newExt)
        if newExt in ['.lnk', '.bat', '.URL']: 
            newType = 'LINK'
            if os.path.exists(newFileName):
                newCommand = f"['{newFileName}']"
            else:
                shutil.copy(fullName, newFileName)
                newCommand = f"['{newFileName}']"
            print('LINK newName', newName, newFileName)
        elif newExt in ['.exe']: 
            newType = 'EXEC'
            newCommand = f"['{fullName}']"
        elif newExt in ['.py', '.pyw', '.pyc']: 
            newType = 'PYTHON'
            newCommand = f"['{fullName}']"
        elif 'http:' or 'https:' in fullName:
            newType = 'LINK'
            newCommand = f"['{fullName}']"
        else:
            self.WarningMessage(f'Dont Understand dropped extension - {fullname}', 'Create New Button')
            return
        newSection = f'{thisTab.Name}.{newName}.{CODE.get_random_string(5)}'
        newGroup = thisTab.Name
        self.config.add_section(newSection)
        self.config.set(newSection, 'name', newName)
        self.config.set(newSection, 'tab', newGroup)
        b = Button(self, newName, newSection, self.config)
        self.AllButtons.append(b) # used to count button access.
        b.Tab = thisTab.Name
        b.Icon = 'batman.png'
        b.makeIcon()
        b.Type = newType
        b.Command = newCommand 
        b.makeCommand(self)
        b.makeContext(self)
        b.TabInstance = thisTab
        items = self.config.items(newSection) # all values as tuple pair.
        items = [(x[0].capitalize(), x[1]) for x in items]
        b.allOptions = CODE.lt2d(items) # as dictionary
        b.allKeys = CODE.lt2l(items) # keys.
        #~ b.dump(label = 'This is the new button')
        thisTab.addButton(b)
        thisTab.Hide()
        thisTab.Populate(self)
        thisTab.Show()
        self.tabControl.SetSelection(self.PageIndex[thisTab]) # causes a slight blip
        self.EditConfig(b, b.Section)
        self.Edited = True
        self.Refresh()
        
    def SelectNewButton(self, a, tab = None): # a is a place holder for evemts, tab is a name
        self.edittree = TabChoseDialog('Chose a tab to make a new button.', tab, self)
        result = self.edittree.ShowModal()
        if self.treeResult is None:
            self.WarningMessage('Nothing Selected', 'Select Tab')
        else:
            self.NewButton(None, tab = self.treeResult)
    
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
        wc = 'Bitmap files (.bmp)|.bmp|PNG Files (.png)|.png' # format problem
        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        with wx.FileDialog(self, 'Open Bitmap File', style = style, defaultDir = './icons') as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
            icon = fileDialog.GetPath()
            junk, exc = os.path.splitext(icon)
            newname = f'{button.Section}.{button.Name}{exc}'
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
        
    def NewCommand(self, a, button = None): # a is placeholder for event stuff
        Button = button
        while True:
            self.Result = None
            #~ print('Result before', self.Result)
            commandbox =CommandDialog(self, Button)
            result = commandbox.ShowModal()
            #~ print('Result after', self.Result)
            if self.Result == 'L':
                continue
            elif self.Result == 'F':
                return
            else:
                break
        # read result to build updated command, (radioResult, commandResult, flagResult, countResult)
        #~ print(f'Newcommand {self.Result}')
        Button.Type = self.Result[0]
        #
        Button.Comand = self.Result[1]
        #
        Button.Count = int(self.Result[3])
        #
        Button.Drop = str(self.Result[2]['Drop'])
        Button.Elevation = str(self.Result[2]['Elevation'])
        #
        Button.makeCommand(self)
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
            self.WarningMesssage('Nothing to delete', 'Delete ?')
            return
        if button not in self.AllButtons:
            self.WarningMesssage('Buton may already have been deleted', 'Delete ?')
            return
        msg = f'Delete {button.Name} from {button.Tab}'
        dlg = wx.MessageDialog(None, msg, 'Delete ?', wx.YES_NO)
        ret = dlg.ShowModal()
        if ret != wx.ID_YES:
            return
        ret = self.config.remove_section(button)
        self.AllButtons.remove(button)
        tab = button.TabInstance
        tab.deleteButton(button)
        tab.Hide()
        tab.Populate(self)
        tab.Show()
        self.Edited = True # This is crucial
            
    def ShowProperty(self, button = None, editprop = None):
        print(f'----{button} {editprop}')
        editbox = EditDialog(button, self, edit = editprop)
        result = editbox.ShowModal()
        editbox.Destroy()
        self.Edited = False
        
    def EditProperty(self, button = None, editprop = None):
        print('*' * 30, 'Before edit')
        print(f'>>>>{button} {editprop}')
        editbox = EditDialog(button, self, edit = editprop)
        result = editbox.ShowModal()
        editbox.Destroy()
        print('*' * 30, 'After edit')
        print(self.Result)
        button.dump('Before Update')
        self.Edited = False
        if self.Result is not None:
            for k, v in self.Result.items():
                setattr(button, k, v)
            button.Count = int(button.Count)
            button.dump('After Update')
            self.Edited = True
        t = button.TabInstance
        t.Hide()
        t.Populate(self)
        t.Show()
        print('b.s', button.Section)
        self.EditConfig(button, button.Section)
        print('*' * 30, 'After update')
            
    def EditConfig(self, button, section):
        print(f'allOptions {allOptions}')
        for k in button.allOptions:
            v = getattr(button, k)
            self.config.set(section, k.lower(), str(v))

    def Update(self, a):
        if self.DontUpdate:
            self.DontUpdate = False
            self.Edited = False
            return
        filename = os.path.join(self.scriptPath, CONST.INIFILE)
        backupfile = filename.replace('.ini', '.ini.backup')
        #~ print(f'Backup from {filename} to {backupfile}')
        shutil.copy(filename, backupfile)
        with open(filename, 'w') as configfile:
            self.config.write(configfile)
        self.Edited = False
        
    def Restart(self, a):
        global ExitFlag
        ExitFlag = True
        self.Finish(None)
        
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
        edit = ['C:\\Programs\\wscite\\SciTE.exe', CONST.FULL_INI_PATH]
        try:
            pid = sub.Popen(edit).pid
        except:
            self.WarningMessage('sub.Popen failed', 'Edit .Ini Command')
        self.Vanish(None)

        
           
    def Command(self, *a, **b): # b is a dictionary, b[CONST.PROG] should be a list, a is some event data
        print(f'Command {b}')
        isDrop = b.get('drop', False)
        pid = None
        button = b[CONST.BUTTON]
        button.Count += 1 # update count in file
        self.config.set(button.Section, 'count', str(button.Count))
        self.Edited = True
        prog = b[CONST.PROG]
        #~ if 
        El = CODE.str2bool(button.Elevation)
        #~ print(f'Button {button.Name} = {El} {type(El)}')
        if El:
            #~ print(f'Button {button.Name} = {button.Elevation} True')
            c = prog[0]
            #~ print(f'Run {c} elevated')
            ret =ctypes.windll.shell32.ShellExecuteW(None, "runas", c, '', None, 1)
        else:
            if isDrop:
                pass # crude way must be better
            try:
                pid = sub.Popen(prog).pid
            except OSError:
                self.WarningMessage(f'Needs elevation  {prog}! (Probably.)', f'Run .exe Command')
            except:
                self.WarningMessage(f'sub.Popen failed  {prog}', f'Run .exe Command')


        self.Vanish(None)
        
    def PyCommand(self, *a, **b): # b is a dictionary, b[CONST.PROG] should be a list, a is some event data
        pid = None
        button = b[CONST.BUTTON]
        button.Count += 1 # update count in file
        self.Edited = True
        self.config.set(button.Section, 'count', str(button.Count))
        #
        startupinfo = sub.STARTUPINFO()
        startupinfo.dwFlags |= sub.STARTF_USESHOWWINDOW
        prog = b[CONST.PROG]
        try:
            pid = sub.Popen(b[CONST.PROG], startupinfo = startupinfo).pid
        except:
            self.WarningMessage(f'sub.Popen failed  {prog}', f'Executing python command')
        self.Vanish(None)
        
    def LinkCommand(self, *a, **b): # b is a dictionary, b[CONST.PROG] should be a list, a is some event data
        button = b[CONST.BUTTON]
        button.Count += 1 # update count in file
        self.Edited = True
        self.config.set(button.Section, 'count', str(button.Count))
        prog = b[CONST.PROG]

        #
        cmd = ' '.join(prog)
        print(f'Startfile {cmd}')
        os.startfile(cmd)
        #~ try:
            #~ os.startfile(cmd)
        #~ except:
            #~ self.WarningMessage(f'os.startfile failed  {cmd}', f'Executing Link command')
        self.Vanish(None)
        
    
def gogui():
    version = ' (Ver 4.00)'
    title='Launcher'
    wx.InitAllImageHandlers()
    app = wx.App()
    frm1 = MyFrame(app, NAME_STRING, (CONST.myPosition, 0)) # main gui
    frm1.Layout()
    frm2 = MyFrame2(app, frm1, 'Spare', (CONST.myPosition, 0)) # dummy gui
    frm2.Layout()
    frm1.other = frm2
    frm2.other = frm1
    frm1.Show()
    app.MainLoop()
    
if __name__ == '__main__': # tidy this up
    name = sys.argv[-1]
    name = os.path.abspath(name)
    path, name = os.path.split(name)
    #
    # over wrie constants with local path
    #
    INIFILE = 'launcher.ini'
    CONST.ICONPATH = os.path.join(path, 'icons') # 'H:\\Computers\\PythonTools\\Launcher\\icons'
    #
    CONST.ICON_PATH = CONST.ICONPATH # 'H:\\Computers\\PythonTools\\Launcher\\icons'
    INI_FILE = INIFILE # 'launcher.ini'
    CONST.FULL_INI_PATH = os.path.join(path, INI_FILE) #'H:\\Computers\\PythonTools\\Launcher\\' + INI_FILE
    #
    PICLKEFILE = CONST.FULL_INI_PATH.replace('.ini', '.pickle')
    #
    if 'PythonTools' in CONST.FULL_INI_PATH:
        NAME_STRING = 'wxLauncher - Development'
    else:
        NAME_STRING = 'wxLauncher'
    ExitFlag = None
    gogui()
    if ExitFlag:
        os.execl(sys.executable, sys.executable, *sys.argv) # This works as equired, taken from internet





