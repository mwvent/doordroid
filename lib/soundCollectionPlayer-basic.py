import os
import random
from lib import season
from lib import logger
from lib import soundDevices
# https://github.com/larsimmisch/pyalsaaudio
import alsaaudio
import wave

class SoundCollectionPlayer :
	def __init__(self, folder) :
		self.basePath=folder

	def playRandomSound(self, *args) :
		logger.log("Playrandom sound called")
		collectionToUse = season.getSeason()

		soundCollections = {}
		for collection in os.listdir(self.basePath):
			soundCollections[collection] = {}
			for soundfile in os.listdir(self.basePath + "/" + collection + "/"):
				fullpath = self.basePath + "/" + collection + "/" + soundfile
				soundCollections[collection][fullpath] = fullpath

		soundo_key = random.sample( list(soundCollections[ collectionToUse ]), 1 )[0]
		logger.log("Playing sound " + soundo_key)
		for soundDevice in soundDevices.getSinks() :
			try:
				pid = os.fork()
				if pid == 0:
					os.system("paplay \"" +  soundo_key + "\" -d " + soundDevice)
					os._exit(0)
			except:
					logger.log("Error playing sound " + soundo_key + " on " + soundDevice)

