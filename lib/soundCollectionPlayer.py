#!/usr/bin/env python
import ctypes
import wave
import sys
import os
import random
from lib import season
from lib import logger
from lib import pulseAudioStream

class SoundCollectionPlayer :
    def __init__(self, folder) :
        self.name = os.path.basename(folder)
        self.stream = pulseAudioStream.PulseAudioStream( self.name )
        # load sound collections
        self.basePath=folder
        self.soundCollections = {}
        self.samples = {}
        logger.log("Loading sound collection " + self.name)
        for collection in os.listdir(self.basePath):
            self.soundCollections[collection] = {}
            for soundfile in os.listdir(self.basePath + "/" + collection + "/"):
                logger.log("    Loading " + self.basePath + "/" + collection + "/" + soundfile)
                self.soundCollections[collection][soundfile] = soundfile
                samplePath=self.basePath + "/" + collection + "/" + soundfile
                sampleName=soundfile
                self.addSample( sampleName, samplePath )

    def playRandomSound(self, *args) :
        collectionToUse = season.getSeason()
        soundo_key = random.sample( list(self.soundCollections[ collectionToUse ]), 1 )[0]
        logger.log("Playing sound from collection " + self.name + " " + collectionToUse + " " + soundo_key)
        self.playSample( soundo_key )

    def addSample( self, name, filePath ) :
        waveObject = wave.open(filePath, 'rb')
        waveData = waveObject.readframes(-1)
        if waveObject.getframerate() != 44100 or waveObject.getnchannels() != 2 :
            logger.log("Bad Wav File - " + filePath + " should be 44100mhz 2 channel")
        self.samples [ name ] = waveData

    def playSample( self, name ) :
        error = ctypes.c_int(0)
        waveData = self.samples [ name ]
        self.stream.pulseConnection.pa_simple_write(self.stream.pulsePlayBackStream, waveData, len(waveData), error)
        self.stream.pulseConnection.pa_simple_drain(self.stream.pulsePlayBackStream, error)

