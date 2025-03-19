"""
Welcome to Youtube Autonomous Voice Assistant
Module.

Some interesting links below.

Project about a personal assistant:
- https://github.com/ccarstens/Ava/blob/dev/ava/input.py

Commands understanding engine for FREE (Meta):
- https://wit.ai/

Metrical phonologic parser in python:
- https://github.com/quadrismegistus/prosodic
"""
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.text.transcriptor import WebRealTimeAudioTranscriptor
from pygame import mixer as PygameMixer
from typing import Union

import time
import pyttsx3


class VoiceAssistant:
    """
    Voice assistant class to improve the way you work.
    You will be able to work without using the 
    keyboard.
    """

    _TIME_TO_WAIT_UNTIL_FINISHED: float = 0.1
    """
    The time each 'sleep' method will be applied when
    waiting for a sound or narrationg being played 
    until it is over.
    """

    @property
    def audio_transcriptor(
        self
    ) -> WebRealTimeAudioTranscriptor:
        """
        The audio transcriptor capable of understanding
        what the user is saying through the microphone.
        """
        return self._audio_transcriptor

    def __init__(
        self
    ):
        self._audio_transcriptor = WebRealTimeAudioTranscriptor(do_use_local_web_page = False)
        PygameMixer.init()

    def _play_sound(
        self,
        sound: Union[PygameMixer.Sound, str],
        do_wait_until_finished: bool = True
    ) -> None:
        """
        Play the provided 'sound'. This method will wait
        until the whole sound is played if the 
        'do_wait_until_finished' flag is True.
        """
        ParameterValidator.validate_mandatory_instance_of('sound', sound, [PygameMixer.Sound, str])
        ParameterValidator.validate_mandatory_bool('do_wait_until_finished', do_wait_until_finished)

        if PythonValidator.is_string(sound):
            sound = PygameMixer.Sound(sound)

        sound.play()

        while (
            PygameMixer.get_busy() and
            do_wait_until_finished
        ):
            time.sleep(self._TIME_TO_WAIT_UNTIL_FINISHED)

    def _narrate(
        self,
        text: str,
        do_wait_until_finished: bool = True
    ) -> None:
        """
        Play a voice sound narrating the provided 
        'text'.
        """
        ParameterValidator.validate_mandatory_string('text', text)

        engine = pyttsx3.init()
        engine.say(text)
        
        if do_wait_until_finished:
            engine.runAndWait()

    def _get_user_speech(
        self
    ) -> str:
        """
        Listen to the user voice speech and get the
        transcription of it.
        """
        return self.audio_transcriptor.transcribe()
    
    def listen_n_times(
        self,
        n: int = 1
    ):
        """
        Listen to the user speech 'n' times and process
        those commands one by one.
        """
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        # TODO: I want to be able to detect when a first
        # temporary transcription is detected, so I can
        # play a sound, and return the value only when 
        # the definitive result is obtained. Here I am
        # playing a sound but it is not when the speaking
        # starts, it is when the definitive transcription
        # has been obtained...
        for _ in range(n):
            self._play_sound('C:/Users/dania/Downloads/wineglasssound.mp3')
            text_speech = self._get_user_speech()
            self._narrate(text_speech)
            