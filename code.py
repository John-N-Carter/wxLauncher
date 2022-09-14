#!/usr/bin/env python3.10
from imports import *
import constants as CONST


#
# home for non class code
#

def getFileName(a):
    path, name = os.path.split(a)
    name, ext = os.path.splitext(name)
    return path, name, ext

parseFileName = getFileName

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(r.choice(letters) for _ in range(length))

def lt2d(a): # replace with b = dict(iter(a)), suspect
    return a if a is dict else {k[0]: k[1] for k in a}

def lt2l(a):
    return [k[0] for k in a]


def str2bool(a): # converts strings that mean True to bool
    if type(a) is str:
        a = a.lower()
    true = ['true', 't', '1', 1, True, 'ok', 'yes']
    return a in true

def decodeException():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno



if __name__ == '__main__':
    print('Code Test:', bool(str2bool('Yes')))

