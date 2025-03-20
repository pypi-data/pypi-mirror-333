from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.downloader import Downloader
from yta_general_utils.file.checker import FileValidator


class Sound(Enum):
    """
    Enum class that hold the sound names and the
    filenames as values.
    """
    
    MINI_DRUM = 'https://drive.google.com/file/d/1WkqZg0Agb8w7RPDXRS6MgpTnPxWKIsvp/view?usp=sharing'
    """
    Sound when the speech starts being detected.
    """
    ACTIVATION = 'https://drive.google.com/file/d/1leaAAIFLWnWu7yVVm3bcMLGo9MR3z2cE/view?usp=sharing'
    """
    Sound when the system has been activated.
    """
    DEACTIVATION = 'https://drive.google.com/file/d/1hvkV_uTHEF75iNqCfSHRxSb1EhIbu2Xt/view?usp=sharing'
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
        filename = f'audio_{self.name.lower()}.wav'
        
        return (
            filename
            if FileValidator.file_exists(filename) else
            Downloader.download_google_drive_resource(self.value, filename)
        )