import os
import signal
import sys
from lib import eventHandler
from lib import soundCollectionPlayer
from lib import zoneMinderTrigger
from lib import serialLineReader
from lib import logger
import time
import pigpio


pi = pigpio.pi()

doorbell_pin = 26
doorbell_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/doorbell" )
doorbell_eventHandler = eventHandler.EventHandler ( "Doorbell", 2 )
doorbell_eventHandler.ignoreNextTriggers = 0
pi.set_mode(doorbell_pin, pigpio.INPUT)
pi.set_pull_up_down(doorbell_pin, pigpio.PUD_UP)
pi.set_glitch_filter(doorbell_pin, 20001) 
receiver_edgeChangeCallBack_handle = pi.callback(doorbell_pin, pigpio.EITHER_EDGE, doorbell_eventHandler.trigger)
doorbell_eventHandler.add_callback( doorbell_sounds.playRandomSound, [] )
doorbell_eventHandler.add_callback( zoneMinderTrigger.send, ["7", "doorbell"] )


pir_greeting_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/pir_in" )
pir_goodbye_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/pir_out" )
pir_eventHandler = eventHandler.EventHandler ( "PIR", 40 )
pir_eventHandler.add_callback ( pir_greeting_sounds.playRandomSound, [] )
pir_eventHandler.add_noRateLimit_callback ( zoneMinderTrigger.send, ["7", "pir"] )

rx = serialLineReader.SerialLineReader( "/dev/arduino", 115200 )
def serialRxCallBack(data) :
	if data == "" :
		return
	logger.log("Got rx code :" + data )
	if data == "14728794" :
		pir_eventHandler.trigger()
	if data == "31598" :
		doorbell_eventHandler.trigger()
	if data == "13688" :
		doorbell_eventHandler.trigger()
rx.add_callback ( serialRxCallBack )

# rx = ev1527.Ev1527_receiver( 27 )
#pir_eventHandler.setOutroCallBackFunction( pir_goodbye_sounds.playRandomSound, 10 )
#def pirRxCodeCheck( decodedBits ) :
#	if len( decodedBits ) > 1 :
#		
#	# pir sends out 1X00X11XFFXX but accept some common variations due to interference
#	if decodedBits.find("100FF110") > -1 or decodedBits.find("100X11XF") > -1  or decodedBits.find("10FF1XX1") > -1 or decodedBits.find("100FF1X0") > -1 :
#		
#rx.add_callback ( pirRxCodeCheck )

def signal_handler(sig, frame):
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

logger.log("Doordroid Ready")

while True :
    time.sleep(1000)
