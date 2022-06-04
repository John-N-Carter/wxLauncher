#!/usr/bin/env python3.10
import sys, os, glob, configparser
print(F'Checking shortcuts')
filename = 'launcher.ini'
config = configparser.ConfigParser(interpolation = None, allow_no_value=True)
with open(filename, 'r') as configfile:
    config.read_file(configfile)
Sections = config.sections()
Sections = [x for x in Sections if x != 'SETUP']
Links = []
for s in Sections:
    t = config[s]['type']
    c = config[s]['Command']
    c = eval(c)
    c = c[0]
    c = os.path.abspath(c)
    if t == 'LINK':
        if os.path.isdir(c):
            continue
        if c[:4] == 'http':
            continue
        if not c[0:2] == 'H:':
            continue
        e = os.path.exists(c)
        #~ if e:
            #~ continue
        p, f = os.path.split(c)
        Links.append(c)
        n = config[s]['Name']
        t = config[s]['tab']
        #~ print(c)
        #~ print(F'{s} {t } {p} __"{t}:{n}" {f} ++ {e}')
        print(F'"{t}:{n}" {f} ++ {e}')


Files = glob.glob('.\\Shortcuts\\*.*')

#~ for f in Files:
    #~ f = os.path.abspath(f)
    #~ l = f in Links
    #~ if not l:
        #~ os.remove(f)
        #~ print(f, l)

