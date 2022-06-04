#!/usr/bin/env python3.10
#
# Button and tab code for launcher.
#
from imports import *
import constants as CONST
import code as CODE


class Button():
    """ Class to hold all button information """
    """ Bug with circular imports """

    IconCache = {} # take cache out of this class and put in myFrame

    def __init__(self, master, name, section, config):
        self.Master = master
        self.Name = name
        self.Config = config
        self.IconData = None
        self.CommandData = None
        self.Action = None
        self.allOptions = None
        self.allKeys = None
        self.control = None
        self.textTitle = None
        self.iconControl = None
        self.Elevation = False
        self.ButtonContextData = None
        self.TabInstance = None
        self.Drop = None
        self.Position = None
        self.Worst = None
        self.Lines = 1
        self.Section = section
        self.Tab = self.Config[self.Section][CONST.TAB]
        self.Icon = self.Config[self.Section][CONST.ICON]
        self.Command = self.Config[self.Section][CONST.COMMAND]
        self.Type = self.Config[self.Section][CONST.TYPE]
        self.Count = int(self.Config[self.Section][CONST.COUNT])
        self.Colour = self.Config[self.Section][CONST.COLOUR]
        self.Elevation =  self.Config[self.Section][CONST.ELEVATION]
        self.Lines = self.Config[self.Section][CONST.LINES]
        self.Drop = self.Config[self.Section][CONST.DROP]
        self.Drop = CODE.str2bool(self.Drop)
        self.Elevation = CODE.str2bool(self.Elevation)
        self.Iconcode = None
        self.DefaultArgument = ''
        self.Working = 'H:/'
        self.Working = self.Config[self.Section][CONST.WORKING]
        self.Defaultargument = self.Config[self.Section][CONST.DEFAULTARGUMENT] #  convert string


    def dump(self, label = None):
        print( 'Button Dump', label)
        print( 'Name',self.Name)
        print( 'Section', self.Section)
        print( 'Tab', self.Tab)
        print( 'Icon', self.Icon)
        print( 'Commmand', self.Command)
        print( 'Count', self.Count)
        print( 'All options', self.allOptions)
        print( 'Tab Instance Name', self.TabInstance.Name)
        print( 'Can Drop On', self.Drop)
        print( 'Elevation', self.Elevation)
        print( 'Working', self.Working)
        print( 'Default Argument', self.Defaultargument)

    def __repr__(self):
        return f'{self.Name} + {self.Section}'

    def makeIcon(self, path = CONST.ICONPATH):
        iconType = None
        if '.png' in self.Icon:
            iconType = wx.BITMAP_TYPE_PNG
        elif '.bmp' in self.Icon:
            iconType = wx.BITMAP_TYPE_BMP
        elif '.ico' in self.Icon:
            iconType = wx.BITMAP_TYPE_ICO
        elif '.jpg' in self.Icon:
            iconType = wx.BITMAP_TYPE_JPG
        else:
            sys.exit()
        Icon = os.path.join(path, self.Icon)
        if Icon in self.IconCache:
            self.IconData = self.IconCache[Icon]
        #put protection in here
        if os.path.exists(Icon):
            IconData = wx.Image(Icon, iconType)
            if IconData.GetWidth() != 48:
                IconData.Rescale(48, 48, quality = wx.IMAGE_QUALITY_HIGH)
            self.IconData = IconData.ConvertToBitmap()
        else:
            self.IconData = self.Master.IconData
            self.Icon = 'Unknown'
            self.Master.ErrorMessage(f'icon problems - {Icon} with {self.Name}')
        self.IconCache[Icon] = self.IconData

    def makeContext(self, Master):
        self.ButtonContextData = lambda a, x = self : self.Master.ButtonContextMenu(a, Button = x)

    def makeCommand(self, Master):
        #
        # command function take two parametrs so needs a leading placeholder.
        #
        # check things exist, when command built.
        #
        self.ValidTypes = self.Config[CONST.SETUP]['Types']
        self.ValidTypes = eval(self.ValidTypes)
        command = self.Command
        if type(command) == list:
            command = str([x.replace('\\', '/') for x in command])
        else:
            command = command.replace('\\', '/')
        try:
            self.Command = eval(command)
        except:
            self.Master.ErrorMessage(f'Badly formatter command {command}',  'Make Command for Buttton')
            self.Master.FinishOK()
        if self.Type == 'INTERNAL': # must match ini file INTERNAL
            self.CommandData = command
        elif self.Type in ['PYTHON', 'LINK', 'EXEC']: # PYTHON or LINK, EXEC
            self.CommandData = lambda a, x = self.Command : self.Master.AllCommand(a, program = x, Button = self)
        elif self.Type is None:
            self.Command = None
            self.Master.WarningMessage(f'No Command: {command}', 'Make Command for Buttton')
        else:
            self.Comand = None
            self.Master.ErrorMessage( f'Unknown Command {command}', 'Make Command for Buttton')
            self.Master.Finish()

class ButtonFileDrop(wx.FileDropTarget):
    def __init__(self, master, button = None): # needs error traps
        self.Master= master
        self.Button = button
        super(ButtonFileDrop, self).__init__()
    def OnDropFiles(self, x, y, filenames):
        fileNames = copy.copy(filenames)
        self.Master.DropOnButton(None, button = self.Button, files = fileNames)
        return False

class Tab:
    #
    #  This class will hold all the data about tabs, replacing global variables in myFrame.
    #
    def __init__(self, name):
        self.Name = name
        self.LegalName = self.MakeLegal(self.Name)
        self.Buttons = []
        self.oldButtons = []
        self.iconImage = []
        self.iconName = []
        self.Format = ('',)
    def MakeLegal(self, name):
        return name.replace(' ', '_')
    def addButton(self, b):
        self.Buttons.append(b)
    def deleteButton(self, b):
        self.Buttons.remove(b)
    def addPlaces(self, image, name): # Image, Text
        self.iconName.append(name)
        self.iconImage.append(image)
    def syncButtons(self):
        self.oldButtons = C.copy(self.Buttons)
    def getButton(self, a): # a is name of button
        for b in self.newButtons:
            if b.Name == a:
                return b
    def Populate(self, master): # master is containing frame.
        NumberIcons = min(CONST.PER_ROW, len(self.Buttons))
        self.Buttons = sorted(self.Buttons, key =attrgetter('Count'), reverse = True)
        for i in range(NumberIcons):
            button = self.Buttons[i]
            button.Position = i
            if master.Score:
                if button.Count > 10:
                    cnt = '>10'
                else:
                    cnt = str(button.Count)
                self.iconName[i].SetLabel(f'{button.Name} [{cnt}]')
            else:
                self.iconName[i].SetLabel(f'{button.Name}')

            self.iconImage[i].SetBitmapLabel(button.IconData)
            if button.Drop:
                bfd = ButtonFileDrop(master, button = button)
                self.iconImage[i].SetDropTarget(bfd)
            master.Bind(wx.EVT_BUTTON, button.CommandData, self.iconImage[i])
            master.Bind(wx.EVT_CONTEXT_MENU, button.ButtonContextData, self.iconImage[i])
        master.Refresh()
        return

    def Hide(self):
        for i in range(CONST.PER_ROW):
            self.iconName[i].Hide()
            self.iconImage[i].Hide()
    def Show(self):
        n = len(self.Buttons)
        if n > CONST.PER_ROW:
            n = CONST.PER_ROW
        for i in range(n):
            self.iconName[i].Show()
            self.iconImage[i].Show()

if __name__ == '__main__':
    print('Button test: Run "launcher.pyw"')

