import ctypes

class struct_pa_sample_spec(ctypes.Structure):
    __slots__ = [
        'format',
        'rate',
        'channels',
    ]

struct_pa_sample_spec._fields_ = [
    ('format', ctypes.c_int),
    ('rate', ctypes.c_uint32),
    ('channels', ctypes.c_uint8),
]
pa_sample_spec = struct_pa_sample_spec  # /usr/include/pulse/sample.h:174

class PulseAudioStream :
    def __init__(self, name) :
        # init a persitent pulseaudio connection & stream
        PA_STREAM_PLAYBACK = 1
        PA_SAMPLE_S16LE = 3
        self.pulseConnection = ctypes.cdll.LoadLibrary('libpulse-simple.so.0')

         # Defining sample format.
        ss = struct_pa_sample_spec()
        ss.rate = 44100 # wf.getframerate()
        ss.channels = 2
        ss.format = PA_SAMPLE_S16LE
        error = ctypes.c_int(0)

        appId = "Doordroid-" + name
        appId_b = appId.encode('utf-8')
        mediaId = name
        mediaId_b = mediaId.encode('utf-8')
        soundDev = "alsa_output.platform-soc_audio.analog-stereo"
        soundDev_b = soundDev.encode('utf-8')
        self.pulsePlayBackStream = self.pulseConnection.pa_simple_new(
            None,  # Default server.
            appId_b,  # Application's name.
            PA_STREAM_PLAYBACK,  # Stream for playback.
            soundDev_b,  # Default device.
            mediaId_b,  # Stream's description.
            ctypes.byref(ss),  # Sample format.
            None,  # Default channel map.
            None,  # Default buffering attributes.
            ctypes.byref(error)  # Ignore error code.
        )
        if not self.pulsePlayBackStream:
            raise Exception('Could not create pulse audio stream: {0}!'.format(
                self.pulseConnection.strerror(ctypes.byref(error))))
                
