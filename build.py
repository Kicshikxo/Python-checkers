import os
import platform

system = platform.system()

if (system == 'Windows'):
    os.system("pyinstaller -F -w -i icon.ico main.py --hidden-import='PIL._tkinter_finder'")
elif (system == 'Linux'):
    os.system("pyinstaller -F -w -i icon.png main.py --hidden-import='PIL._tkinter_finder'")