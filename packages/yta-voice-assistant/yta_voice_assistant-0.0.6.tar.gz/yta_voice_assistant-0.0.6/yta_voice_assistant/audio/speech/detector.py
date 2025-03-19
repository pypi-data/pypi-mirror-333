from yta_general_utils.text.transcriptor import WebRealTimeAudioTranscriptor
from yta_general_utils.programming.env import Environment
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
    
    def get_user_speech(
        self
    ):
        return self.transcriptor.transcribe()
    
class WitSpeechDetector(SpeechDetector):
    """
    Class able to detect the user speech by using
    a the Wit platform speech detection engine.

    This detector needs the 'WIT_ACCESS_TOKEN'
    environment variable set in the .env file.
    """

    def __init__(
        self
    ):
        self._recognizer = sr.Recognizer()
        try:
            self._microphone = sr.Microphone()
        except:
            # TODO: This is not ok
            raise Exception('Sorry, Microphone...')
        self.recognizer.adjust_for_ambient_noise(self._microphone)

    @property
    def recognizer(
        self
    ) -> 'Recognizer':
        return self._recognizer
    
    @property
    def microphone(
        self
    ) -> any:
        return self._microphone

    def get_user_speech(
        self
    ) -> Union[str, None]:
        with sr.Microphone() as source:
            #self.recognizer.adjust_for_ambient_noise(source)

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
        