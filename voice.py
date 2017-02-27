#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import winsound
except ImportError:
    import os
    def playsound(frequency=450,duration=150,mac_say="", win_sound=""):
        content="say " + mac_say
        os.system(content)
else:

    def playsound(frequency=450,duration=150,mac_say="", win_sound=""):
        winsound.Beep(frequency,duration)
    '''    
    def playsound(frequency=450,duration=150,mac_say="", win_sound=""):       
        sound_file=win_sound
        winsound.PlaySound(sound_file,winsound.SND_ASYNC)
    '''