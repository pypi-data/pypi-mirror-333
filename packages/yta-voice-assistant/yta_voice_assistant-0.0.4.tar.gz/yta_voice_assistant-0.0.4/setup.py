from setuptools import setup, find_packages


VERSION = '0.0.4'
DESCRIPTION = 'Youtube Autonomous Voice Assitant.'
LONG_DESCRIPTION = 'This is the Youtube Autonomous Voice Assitant'

setup(
    name = "yta_voice_assistant", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_audio',
        'yta_general_utils',
    ],
    
    keywords = [
        'youtube autonomous voice assistant software'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)