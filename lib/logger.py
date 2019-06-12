import time

logger_lastmessage = ""
logger_repeatcount = 0
def log(t):
	global logger_lastmessage, logger_repeatcount
	if t == logger_lastmessage :
		logger_repeatcount = logger_repeatcount + 1
		return
	logger_lastmessage = t

	if logger_repeatcount > 0 :
		print("Last message repeats " + str(logger_repeatcount) + " times")
		logger_repeatcount = 0
	
	print(time.strftime("%c") + " : " + t)
