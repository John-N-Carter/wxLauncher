# wxLauncher
Tabbed Launch Bar (Not to be confused with Lunch Bar)

![wxLauncher: Showing Frequent tab](wxlauncher.jpg)

For a long time I used Object Dock from Stardock. However it started causing other desktop tools to misbehave so I began to look for an alternative. 

According to Google there are a number of replacements but none were suitable. The best was 'RocketDock', however I could never get it to behave as I wanted.

Consequently I began experimenting with various Python tools to see how far I could go. The result is this app, written in Python 3.8 using an augmented Anaconda Distribution. It provides a tabbed bar that sits at the top of my screen. Each tab has a collection of icons which launche tools. It should be almost platform neutral and is 100% Python.

Tabs and Tools are created vis drag and drop and context menus. It is configured by an .ini file which is updated to reflect changes made when live. It also supports drag and drop on to apps from explorer, desktop and any other source.

One of the most useful features is in keeping track of usage and sorting by most frequently used from the left of the bar. In addition the most frequently used tools are gathered to a virtual tab labelled 'Frequent' for easy access.

I'm currently using the app and recording errors. This is work in progress. It does not always save status after changes, do a manual close before shutting down your computer. I found that when links were dropped from the desktop they were oftem moved or deleted (by me). I started using a shortcuts directory to preserve links. This must be manually setup. Icons are searched for in links, otherwise the program looks for icon of same name.

I have added a .ini file, appropriate icons and some short cuts.

As the program stands there is a good chance of it working out of the box but the .ini file should reflect your computer not mine.
