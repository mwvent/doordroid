from lib import doordroidSettings
import socket

def send(monitor, eventname):
    sendstring = monitor + "|on+20|" + monitor + "|" + eventname + "|" + eventname + "\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((doordroidSettings.getZoneminderServer(), doordroidSettings.getZoneminderPort()))
    s.send(sendstring.encode())
    s.close()
