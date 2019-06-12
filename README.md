# Doordroid

My Rasberry PI door greeter, doorbell sound player and zoneminder PIR trigger service backed up online in case anybody finds any of it useful. The setup is hardcoded in.

Depends on pigpiod installed and run on boot as a service called pigpiod and pulseaudio set up to work headless

Depends on python3 with socket, os, random, ctypes, wave, sys, time, datetime, threading, traceback, pigpio

In my /etc/systemd/system I have a unit called 

doordroid.service

'
[Unit]
Description=Doordroid Service
Requires=pulseaudio.service,pigpiod.service
After=pulseaudio.service,pigpiod.service

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
PrivateTmp=true
Restart=always
RestartSec=3
ExecStart=/opt/doordroid2/service.sh
'
