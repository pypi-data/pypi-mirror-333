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
from yta_voice_assistant.audio.sounds import Sound
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
        speech_detector: Union[WitSpeechDetector, WebSpeechDetector] = WebSpeechDetector
    ):
        ParameterValidator.validate_mandatory_class_of('speech_detector', speech_detector, [WitSpeechDetector, WebSpeechDetector])

        self._audio_transcriptor = speech_detector()
        self._sound_handler = SoundHandler()
        self._narration_handler = NarrationHandler()

    def _play_sound(
        self,
        sound: Sound,
        do_wait_until_finished: bool = True
    ) -> None:
        """
        For internal use only.
        """
        sound = Sound.to_enum(sound)

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
        return self.audio_transcriptor.get_user_speech()

    def play_activated_sound(
        self
    ) -> None:
        """
        Play the deactivation sound and waits until
        it ends.
        """
        return self._play_sound(Sound.ACTIVATION)

    def play_deactivated_sound(
        self
    ) -> None:
        """
        Play the deactivation sound and waits until
        it ends.
        """
        # TODO: Use 'deactivated.wav'
        return self._play_sound(Sound.DEACTIVATION)
    
    def activate_voice_detection(
        self,
        do_play_sound: bool = False
    ):
        """
        Click on the button to activate the transcription
        (if inactive) and plays a sound when done if
        'do_play_sound' is True.

        This method does not load the page, so make sure it
        has been loaded.
        """
        self.audio_transcriptor.activate_transcription()
        if do_play_sound:
            self.play_activated_sound()

    def deactivate_voice_detection(
        self,
        do_play_sound: bool = False
    ):
        """
        Click on the button to deactivate the transcription
        (if active) and plays a sound when done if
        'do_play_sound' is True.

        This method does not load the page, so make sure it
        has been loaded.
        """
        self.audio_transcriptor.deactivate_transcription()
        if do_play_sound:
            self.play_deactivated_sound()

    # TODO: Create methods to just obtain the texts

    def wait_for_text(
        self,
        text: str,
        do_play_sound: bool = False
    ):
        """
        Wait until the provided 'text' is found in the
        temporary or definitive audio transcription. It
        will play a sound if the 'do_play_sound' parameter
        is True.

        This method does not load the page nor click any
        button, so make sure the web has been loaded and
        the narration is activated.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)

        if (
            self.audio_transcriptor.detect_text(text) and
            do_play_sound
        ):
            self.play_activated_sound()
    
    """
    Methods for automatic handling below. These 
    methods will be applied and the results will
    be handled by themselves.
    """

    def detect_text(
        self,
        text: str
    ):
        """
        Detect the given 'text' in the temporary or final
        transcription, loading the website and making sure
        it is listening to the microphone.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)

        if self.audio_transcriptor.detect_fast(text):
            self.play_activated_sound()
    
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

    # TODO: Build a method that 'activates' or 
    # 'hibernates' this voice assistant
    def run(
        self
    ):
        ACTIVATION_COMMAND = 'la vida es una tombola'
        DEACTIVATION_COMMAND = 'hasta nunca'

        # 1. Activate detection
        self.activate_voice_detection(True)

        # 2. Wait until activation sentence is detected
        self.wait_for_text(ACTIVATION_COMMAND, True)

        # 3. Process final results only and handle
        # 4. or deactivation sentence is detected
        do_continue: bool = True
        while (do_continue):
            command = self._get_user_speech()

            if command == DEACTIVATION_COMMAND:
                do_continue = False
            else:
                # TODO: Process command
                print(f'TODO: Process command -> "{command}"')

        # 5. Deactivate detection and exit
        self.deactivate_voice_detection(True)