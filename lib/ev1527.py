import pigpio

class Ev1527_receiver:
	pirStartPulseLength = 9220
	pirStartPulseLength_variance = 50
	pirTetraBitLength = 2400
	pirHalfTetraBitLength = 1200
	receiver_pin = 27
	pi = 0

	debugs_startPulseTime = 0
	debugs_endDataTime = 0 
	debugs_edges = 0
	debugs_tetrabittimes = []
	

	def __init__(self, receiver_pin_v):
		self.pi = pigpio.pi()
		self.receiver_pin = receiver_pin_v
		self.pi.set_glitch_filter(self.receiver_pin, 200) 
		receiver_edgeChangeCallBack_handle = self.pi.callback(self.receiver_pin, pigpio.EITHER_EDGE, self.receiver_edgeChangeCallBack)
		self.callbacks = []
		# set to 1 when receive a valid length pulse
		self.pir_listener_got_start_pulse = 0
		# set to ticks on end & start of start pulse
		self.pir_listener_start_pulse_starttime = 0
		self.pir_listener_start_pulse_endtime = 0
		# record state changes in this array 
		self.waveform_record = []
	
	def add_callback( self, callback_handle ) :
		self.callbacks.append( callback_handle )
	
	def call_callbacks ( self, bits ) :
		for callback in self.callbacks :
			callback ( bits )
	
	def decode_waveform(self, wavearray ) :
		if len ( wavearray ) == 0 :
			return ""
		self.debugs_tetrabittimes = []
		lastState = -1
		lastTime = -1
		bits = ""
		lastHalfBit = ""
		for changes in wavearray :
			newState = changes[1]
			newTime = changes[0]
			if lastTime > -1 :
				if newState == 1  and lastHalfBit == "" :
					self.debugs_tetrabittimes.append( newTime - self.pir_listener_start_pulse_endtime )
				if newState == 0 :
					pulseLength = newTime - lastTime
					if pulseLength < 500 :
						halfBitCode = "s"
					else :
						halfBitCode = "l"

					if lastHalfBit == "" :
						lastHalfBit = halfBitCode
					else:
						bitCode = lastHalfBit + halfBitCode
						lastHalfBit = ""
						if bitCode == "ss" : bits = bits + "0"
						if bitCode == "ll" : bits = bits + "1"
						if bitCode == "sl" : bits = bits + "F"
						if bitCode == "ls" : bits = bits + "X"
			lastState = newState
			lastTime = newTime
		self.debugs_endDataTime = lastTime - wavearray[0][0]
		return bits

	def receiver_edgeChangeCallBack(self, gpio, level, tick) :
		# record start of starting pulse
		if self.pir_listener_got_start_pulse == 0 and level == 0 :
			self.pir_listener_start_pulse_starttime = tick
			return None
		# validate potential starting pulse
		if self.pir_listener_got_start_pulse == 0 and level == 1 :
			pulseLength = tick - self.pir_listener_start_pulse_starttime
			minAcceptedPulse = self.pirStartPulseLength - self.pirStartPulseLength_variance
			maxAcceptedPulse = self.pirStartPulseLength + self.pirStartPulseLength_variance
			if pulseLength > minAcceptedPulse and pulseLength < maxAcceptedPulse :
				self.debugs_startPulseTime = pulseLength
				self.pir_listener_got_start_pulse = 1
				self.pir_listener_start_pulse_endtime = tick
			# dont return here - we want to move on and capture this as the first edge in the array
			# return None
		# gather waveform
		if self.pir_listener_got_start_pulse == 1 :
			dataEndTime = self.pir_listener_start_pulse_endtime + ( self.pirTetraBitLength * 12.3 )
			if tick < dataEndTime and len( self.waveform_record ) < 49: 
				change = [ tick, level ]
				self.waveform_record.append( change )
				return None
			# if we get here we are either over max time data should have arrived or we have the data (edge count)
			self.debugs_edges = len( self.waveform_record )
			self.pir_listener_got_start_pulse = 0
			self.call_callbacks( self.decode_waveform(self.waveform_record) )
			self.waveform_record.clear()
			# this edge change may be the start of a new pulse so set things up for that
			if level == 0 :
				self.pir_listener_start_pulse_starttime = tick
			return None




