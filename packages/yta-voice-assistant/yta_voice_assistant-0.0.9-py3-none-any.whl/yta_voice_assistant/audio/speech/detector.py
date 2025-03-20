from yta_general_utils.text.transcriptor import WebRealTimeAudioTranscriptor
from yta_general_utils.programming.env import Environment
from yta_general_utils.programming.validator.parameter import ParameterValidator
from abc import ABC, abstractmethod
from typing import Union

import speech_recognition as sr


class SpeechDetector(ABC):
    """
    Class to wrap the functionality related to
    detecting a speech by the user who is using
    the app.
    """

    @abstractmethod
    def get_user_speech(
        self
    ):
        """
        Get the user's speech by detecting and
        transcribing it.
        """
        pass

class WebSpeechDetector(SpeechDetector):
    """
    Class able to detect the user speech by using
    a web page that records the microphone and
    transcripts it in real time.

    This detector is able to detect results very
    quick, which is very interesting to detect
    some 'activate' or 'deactivate' commands, 
    while it is also very reliable with the
    results that have been determined as 
    definitive.
    """

    def __init__(
        self
    ):
        self._transcriptor = WebRealTimeAudioTranscriptor(do_use_local_web_page = False)

    @property
    def transcriptor(
        self
    ) -> WebRealTimeAudioTranscriptor:
        return self._transcriptor
    
    def activate_transcription(
        self
    ):
        """
        TODO: Add documentation

        For manually handle only.
        """
        return self.transcriptor.activate_transcription()
    
    def deactivate_transcription(
        self
    ):
        """
        TODO: Add documentation

        For manually handle only.
        """
        return self.transcriptor.deactivate_transcription()
    
    def detect_text(
        self,
        text: str
    ):
        """
        TODO: Add documentation

        For manually handle only.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)

        return self.transcriptor.detect_text(text)
    
    """
    Methods for automatic handling below. These 
    methods will be applied and the results will
    be handled by themselves.
    """
    
    def detect_fast(
        self,
        text: str
    ):
        """
        Detect the provided 'text' fast, which means
        looking for it even in the temporary results,
        making sure web is loaded and transcription
        engine is listening.
        """
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)

        return self.transcriptor.detect_fast(text)
    
    def get_user_speech(
        self
    ):
        """
        Load the web page, activates the speech recognition
        system and waits until a final speech recognition
        result is detected and return it.
        """
        return self.transcriptor.transcribe()
    
class WitSpeechDetector(SpeechDetector):
    """
    Class able to detect the user speech by using
    a the Wit platform speech detection engine.

    This detector must be used when the whole speech
    has been said by the user, so we are sure that
    the whole audio is handled by the wit system.

    This detector needs the 'WIT_ACCESS_TOKEN'
    environment variable set in the .env file.
    """

    def __init__(
        self
    ):
        self._recognizer = sr.Recognizer()

    @property
    def recognizer(
        self
    ) -> 'Recognizer':
        return self._recognizer
    
    def get_user_speech(
        self
    ) -> Union[str, None]:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

            try:
                # Just changing this line you can use another engine
                # return self.recognizer.recognize_whisper(
                return self.recognizer.recognize_wit(
                    self.recognizer.listen(source),
                    Environment.get_current_project_env('WIT_ACCESS_TOKEN')
                )
            except:
                # TODO: Maybe raise Exception (?)
                return None
            # except sr.UnknownValueError:
            #     print("No se pudo entender lo que dijiste.")
            # except sr.RequestError as e:
            #     print(f"Error al conectar con el servicio de reconocimiento: {e}")
        