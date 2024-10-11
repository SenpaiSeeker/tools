from .button import Button
from .chatbot import Api, ImageGen
from .database import LocalDataBase, MongoDataBase
from .encrypt import BinaryEncryptor, CryptoEncryptor
from .getuser import Extract
from .logger import LoggerHandler
from .misc import Handler
from .trans import Translate

__version__ = "0.0.0.1.dev50"

mytoolsID = """
  __  ____   __  _____ ___   ___  _     ____    ___ ____  
 |  \/  \ \ / / |_   _/ _ \ / _ \| |   / ___|  |_ _|  _ \ 
 | |\/| |\ V /    | || | | | | | | |   \___ \   | || | | |
 | |  | | | |     | || |_| | |_| | |___ ___) |  | || |_| |
 |_|  |_| |_|     |_| \___/ \___/|_____|____/  |___|____/ 
"""

print(f"\033[1;37;41m{mytoolsID}\033[0m")
