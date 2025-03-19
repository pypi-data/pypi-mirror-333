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
from yta_voice_assistant.audio.sound import SoundHandler
from yta_voice_assistant.audio.narration import NarrationHandler
from yta_voice_assistant.audio.speech.detector import WebSpeechDetector, WitSpeechDetector
from yta_general_utils.programming.validator.parameter import ParameterValidator
from typing import Union


class VoiceAssistant:
    """
    Voice assistant class to improve the way you work.
    You will be able to work without using the 
    keyboard.
    """

    @property
    def audio_transcriptor(
        self
    ) -> WebSpeechDetector:
        """
        The audio transcriptor capable of understanding
        what the user is saying through the microphone.
        """
        return self._audio_transcriptor
    
    @property
    def sound_handler(
        self
    ) -> SoundHandler:
        """
        The sound handler that is able to play sounds
        by using the Pygame system.
        """
        return self._sound_handler
    
    @property
    def narration_handler(
        self
    ) -> NarrationHandler:
        """
        The narration handler that is able to create
        voice narrations by using the pyttsx3 library.
        """
        return self._narration_handler

    def __init__(
        self,
        speech_detector: Union[WitSpeechDetector, WebSpeechDetector]
    ):
        ParameterValidator.validate_mandatory_class_of('speech_detector', speech_detector, [WitSpeechDetector, WebSpeechDetector])
        
        self._audio_transcriptor = speech_detector()
        self._sound_handler = SoundHandler()
        self._narration_handler = NarrationHandler()

    def _play_sound(
        self,
        sound: str,
        do_wait_until_finished: bool = True
    ) -> None:
        """
        For internal use only.
        """
        return self.sound_handler.play_sound(sound, do_wait_until_finished)

    def _narrate(
        self,
        text: str,
        do_wait_until_finished: bool = True
    ) -> None:
        """
        Narrate the 'text' provided with an artificial
        voice.
        """
        return self.narration_handler.narrate(text, do_wait_until_finished)

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
            