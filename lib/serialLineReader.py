import threading
import serial
from lib import logger

class SerialLineReader:

    def __init__(self, serPortPath, baud):
        self.callbacks = []
        self.serPortPath = serPortPath
        self.baud = baud
        self.serialConn = serial.Serial()
        self.thread = threading.Thread(target=self.serialReadCallBack)
        self.thread.start()

    def __del__(self) :
        self.serialConn.close()

    def add_callback( self, callback_handle ) :
        self.callbacks.append( callback_handle )
	
    def call_callbacks ( self, data ) :
        for callback in self.callbacks :
            callback ( data )
	
    def serialReadCallBack( self ) :
        # outer main loop attempt to access serial connection
        # serialConnected state -1=Not tried 0=disconnected after 1st try 1=connected
        serialConnected=-1 
        while True :
            try :
                self.serialConn = serial.Serial(self.serPortPath, self.baud, timeout=None)
                serialConnected=1
                logger.log("Opened connection to " + self.setPortPath + " speed " + self.baud)
            except :
                if serialConnected==-1:
                    serialConnected=0
                    logger.log("Failed to open connection to " + self.setPortPath + " will retry until open")
                    sleep(1)
            # inner main loop - keep reading data until serial disconnect
            while serialConnected == 1 :
                try :
                    ln = self.serialConn.readline().decode().rstrip()
                    self.call_callbacks(ln)
                except :
                    serialConnected=-1
                    logger.log("Lost connection to " + self.setPortPath)
                    try :
                        self.serialConn.close()
                    except :
                        logger.log("Failed to close " + self.setPortPath)






