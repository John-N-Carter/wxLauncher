#! python3
#
# Program to help with tidy up of icons.
#
import sys, os
import glob, string, math, time, getopt, shutil, configparser

fp = open('launcher.ini', 'r')
config = configparser.ConfigParser()
config.read_file(fp)
fp.close()
try:
    print('Read Labels')
    labels = config.sections()
    labels = labels[1:]
except:
    self.ErrorMessage('Read failed', 'Access config file.')
    sys.exit()
    
for l in labels:
    Icon = config[l]['Icon']
    Tab = config[l]['Tab']
    Name = config[l]['Name']
    n, Ext = os.path.splitext(Icon)
    IconName = Name.replace('.', '_')
    NewIcon = F'{IconName}__{Tab}{Ext}'
    newname = f'./icons2/{NewIcon}'
    oldname = f'./icons/{Icon}'
    config[l]['Icon'] = NewIcon
    try:
        shutil.copy(oldname, newname)
        config[l]['Icon'] = NewIcon
    except:
        print('Error in', l)
        print(Icon)
        print(Name, Tab)
        print(NewIcon)
        print(oldname)
        print(newname)
        sys.exit
with open('launcher2.ini', 'w') as configfile:
    config.write(configfile)

