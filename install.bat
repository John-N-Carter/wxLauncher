REM ~ @echo off
rem
rem Install wxLauncher
rem First backup previous , by day
rem

set launcher_devel=H:\Computers\PythonTools\Launcher\

set launcher_home=C:\Programs\wxLauncher\

set archive_home=C:\Programs\wxLauncher-archive\

set t=%_TIME
set t2=%@REPLACE[:,-,%t]
set d=%_DATE
set d2=%@REPLACE[/,-,%d]
set n=%archive_home%archive-%d2%-%t2%.7z
echo %n

7z a  %n %launcher_home

del /S /[!*.ini] %launcher_home%\*.*

copy/w %launcher_devel%\*.py %launcher_home%\
copy/w  %launcher_devel%\*.pyw %launcher_home%\
copy/s/u/w  %launcher_devel%\icons\*.* %launcher_home%\icons\
copy/s/u/w  %launcher_devel%\newicons\*.* %launcher_home%\newicons\
copy/s/u/w  %launcher_devel%\shortcuts\*.* %launcher_home%\shortcuts
copy/u/w  %launcher_devel%\*.bat %launcher_home%\

REM ~ copy/s/w *.ini %launcher_home% 
REM ~ Dont copy ini filess


