import os
import platform

system = platform.system()

if (system == 'Windows'):
    os.system('pyinstaller -F -w -i icon.ico main.py --hidden-import="PIL._tkinter_finder" && xcopy /Y /I "assets\\" "dist\\assets\\" && xcopy /Y "icon.png" "dist\\"')
elif (system == 'Linux'):
    os.system('pyinstaller -F -w -i icon.png main.py --hidden-import="PIL._tkinter_finder" && /bin/cp -rf assets/ dist/ && /bin/cp -f icon.png dist/')
