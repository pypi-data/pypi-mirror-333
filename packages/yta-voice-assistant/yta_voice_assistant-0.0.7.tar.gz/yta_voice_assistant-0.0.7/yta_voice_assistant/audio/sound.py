from yta_general_utils.programming.decorators import singleton
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.programming.validator import PythonValidator
from typing import Union
from pygame import mixer as PygameMixer
from time import sleep as time_sleep


@singleton
class SoundHandler:
    """
    Class to handle sounds with the pygame system.
    """

    _TIME_TO_WAIT_UNTIL_FINISHED: float = 0.1
    """
    The time each 'sleep' method will be applied when
    waiting for a sound or narrationg being played 
    until it is over.
    """

    def __init__(
        self
    ):
        PygameMixer.init()

    def play_sound(
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
            time_sleep(self._TIME_TO_WAIT_UNTIL_FINISHED)