from yta_general_utils.programming.enum import YTAEnum as Enum


class Sound(Enum):
    """
    Enum class that hold the sound names and the
    filenames as values.
    """
    
    MINI_DRUM = 'mini_drum.wav'
    """
    Sound when the speech starts being detected.
    """
    ACTIVATION = 'activation.wav'
    """
    Sound when the system has been activated.
    """
    DEACTIVATION = 'deactivation.wav'
    """
    Sound when the system has been deactivated.
    """

    @property
    def path(
        self
    ) -> str:
        """
        Path to the sound file location.
        """
        return f'audio/sounds/{self.value}'