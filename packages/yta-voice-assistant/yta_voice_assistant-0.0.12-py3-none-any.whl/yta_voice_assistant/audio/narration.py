from yta_general_utils.programming.decorators import singleton
from yta_general_utils.programming.validator.parameter import ParameterValidator

import pyttsx3


@singleton
class NarrationHandler:
    """
    Class to wrap the functionality related to
    voice narration.
    """

    def __init__(
        self
    ):
        self._narrator = pyttsx3.init()

    @property
    def narrator(
        self
    ) -> 'Engine':
        return self._narrator

    def narrate(
        self,
        text: str,
        do_wait_until_finished: bool = True
    ) -> None:
        """
        Play a voice sound narrating the provided 
        'text'. This narration is created in real time
        creating not a file.
        """
        ParameterValidator.validate_mandatory_string('text', text)

        self.narrator.say(text)
        
        if do_wait_until_finished:
            self.narrator.runAndWait()