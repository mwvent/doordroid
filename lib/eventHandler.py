import datetime
import time
import threading
from threading import Thread
import os
from lib import logger
import traceback

class EventHandler :
    def __init__(self, name, repeatRateLimiterSeconds) :
        self.name = name
        self.repeatRateLimiterSeconds = repeatRateLimiterSeconds
        self.ignoreNextTriggers = 0
        self.trigger_function_lock = 0
        self.last_trigger_time = datetime.datetime.now()
        self.last_trigger_time = datetime.datetime.now() - datetime.timedelta(hours=1)
        self.callbacks = []
        self.noRateLimit_callbacks = []
        self.introCalled = 0
        self.outroCallBackFunction = -1
        self.outroInactivityTimeToCallInSeconds = -1
        self.outroCallBackTimer = threading.Timer(0,0)

    # trigger function
    # handle rate limiting - do callback if valid 
    # handle outro callback if set
    def trigger(self, *args) :
        # prevent concurrent execution of function
        if self.trigger_function_lock == 1:
            #logger.log( self.name + " trigger ignored - function locked" )
            return
        # the main thread can set an ignore count - used if an unwanted edge detect fires at startup
        if self.ignoreNextTriggers > 0 :
            self.ignoreNextTriggers = self.ignoreNextTriggers - 1
            return
        
        # everything else goes in a try block as the function lock MUST be lifted at the end whatever happens
        self.trigger_function_lock = 1
        try :
            # any activity at all resets the outro timer even before rate limiting            
            if self.outroInactivityTimeToCallInSeconds != -1 and self.introCalled == 1 :
                self.outroCallBackTimer.cancel()
                self.outroCallBackTimer = threading.Timer(self.outroInactivityTimeToCallInSeconds, self.callOutro)
                self.outroCallBackTimer.start()
            # call no rate limit callbacks
            self.call_noRateLimit_callbacks()
            # work out rate limiter and return from function if rate limited
            last_trigger_timeDiff =  datetime.datetime.now() - self.last_trigger_time
            self.last_trigger_time = datetime.datetime.now()
            if last_trigger_timeDiff.seconds < self.repeatRateLimiterSeconds:
                #logger.log( self.name + " trigger ignored - rate limiter" )
                return
            # passed - execute callback functions
            logger.log( self.name + " triggered" )
            self.introCalled = 1
            self.call_callbacks()            
        except Exception :
            traceback.print_exc()
        finally :
            self.trigger_function_lock = 0

    def add_callback( self, callback_handle, args ) :
        newCallback = [ callback_handle, args ]
        self.callbacks.append( newCallback )
    
    def call_callbacks ( self ):
        for callbackf in self.callbacks:
            t = Thread(target=callbackf[0], args=callbackf[1])
            t.setDaemon(True)
            t.start()

    def add_noRateLimit_callback( self, callback_handle, args ) :
        newCallback = [ callback_handle, args ]
        self.noRateLimit_callbacks.append( newCallback )
    
    def call_noRateLimit_callbacks ( self ) :
        for callbackf in self.noRateLimit_callbacks :
            t = Thread(target=callbackf[0], args=callbackf[1])
            t.setDaemon(True)
            t.start()

    def callOutro(self) :
        self.introCalled = 0    
        self.outroCallBackFunction()

    def setOutroCallBackFunction(self, newFunction, inactivityTimeToCallInSeconds) :
        self.outroCallBackFunction = newFunction
        self.outroInactivityTimeToCallInSeconds = inactivityTimeToCallInSeconds
    
