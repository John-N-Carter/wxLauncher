#!/usr/bin/env python3.10
import os
import win32gui as gui

def getWindows():
    titles = set()
    def foreach_window(hwnd, lParam):
        if gui.IsWindowVisible(hwnd):
            t = gui.GetWindowText(hwnd)
            if os.path.isdir(t):
                titles.add(t)
            return True

    gui.EnumWindows(foreach_window, 0)
    return list(titles)

if __name__ == '__main__':
    Titles = getWindows()
    print(F'Open Directories {len(Titles)}')
    for t in Titles:
        print(F'   {t}')