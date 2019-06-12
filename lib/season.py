import time
import datetime

def getSeason() :
	season = "normal"
	# play halloween all october after 6pm
	if datetime.datetime.now().month == 10 and datetime.datetime.now().hour > 17:
	    season = "halloween"
	# play halloween all october day after oct 23th
	if datetime.datetime.now().month == 10 and datetime.datetime.now().day > 22:
	    season = "halloween"
	# xmas all december 
	if datetime.datetime.now().month == 12:
	    season = "xmas"
	return season
