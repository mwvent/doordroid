import os
from lib import eventHandler
from lib import soundCollectionPlayer
from lib import zoneMinderTrigger
from lib import ev1527
from lib import logger
import time
import pigpio

rx = ev1527.Ev1527_receiver( 27 )
pi = pigpio.pi()

doorbell_pin = 26
doorbell_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/doorbell" )
doorbell_eventHandler = eventHandler.EventHandler ( "Doorbell", 2 )
doorbell_eventHandler.ignoreNextTriggers = 0
pi.set_glitch_filter(doorbell_pin, 20001) 
receiver_edgeChangeCallBack_handle = pi.callback(doorbell_pin, pigpio.EITHER_EDGE, doorbell_eventHandler.trigger)
doorbell_eventHandler.add_callback( doorbell_sounds.playRandomSound, [] )
doorbell_eventHandler.add_callback( zoneMinderTrigger.send, ["7", "doorbell"] )


pir_greeting_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/pir_in" )
pir_goodbye_sounds = soundCollectionPlayer.SoundCollectionPlayer( "/opt/doordroid2/media/pir_out" )
pir_eventHandler = eventHandler.EventHandler ( "PIR", 40 )
pir_eventHandler.add_callback ( pir_greeting_sounds.playRandomSound, [] )
pir_eventHandler.add_noRateLimit_callback ( zoneMinderTrigger.send, ["7", "pir"] )
pir_eventHandler.setOutroCallBackFunction( pir_goodbye_sounds.playRandomSound, 5 )
def pirRxCodeCheck( decodedBits ) :
	# pir sends out 1X00X11XFFXX but accept some common variations due to interference
	if decodedBits.find("1X00X11X") > -1 or decodedBits.find("XX00X11X") > -1 or decodedBits.find("XF00FF11") > -1 :
		pir_eventHandler.trigger()
rx.add_callback ( pirRxCodeCheck )

logger.log("Doordroid Ready")

while True :
    time.sleep(1000)
