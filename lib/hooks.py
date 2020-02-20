from lib import doordroidSettings
import os

def callHooks(hookname):
    os.system("for f in /opt/doordroid2/hooks/"+hookname+"/*; do $f & done")
