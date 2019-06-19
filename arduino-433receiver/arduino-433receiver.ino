/*
 TAKEN FROM RCSwitch Receive example
*/

// For VGJOT doorbell RCSwitch.cpp needs the following changes 
// Add to proto array
// { 1039, { 9,  4 }, {  1,  1 }, {  1,  3 }, true }      // protocol 7 (VGJOT Doorbell)
// 
// in RCSwitch::receiveProtocol function
// change
/* } else {
     // Failed
*/
// to 
/*
} else if ( ( i - firstDataTiming) > 7 ) {
			code |= 0;
		} else {
			// Failed
           	return false;
		}
*/
#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();
bool debugInfo = false;

void setup() {
  delay(1000);
  Serial.begin(115200);
  mySwitch.setReceiveTolerance(100);
  mySwitch.enableReceive(0);  // Receiver on interrupt 0 => that is pin #2
  Serial.println("Started - send D for Debug Info, send N for normal");
}

void loop() {
  if (mySwitch.available()) {
    Serial.println(mySwitch.getReceivedValue());
    if( debugInfo ) {
      output(mySwitch.getReceivedValue(), mySwitch.getReceivedBitlength(), mySwitch.getReceivedDelay(), mySwitch.getReceivedRawdata(),mySwitch.getReceivedProtocol());
    }
    mySwitch.resetAvailable();
  }
  if ( Serial.available()) {
    char serialRecv = Serial.read();
    if (serialRecv == 'D') {
      debugInfo = true;
    }
    if (serialRecv == 'N') {
      debugInfo = false;
    }
  }
}
