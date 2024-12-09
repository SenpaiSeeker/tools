from .button import Button
from .chatbot import Api, ImageGen
from .database import LocalDataBase, MongoDataBase
from .encrypt import BinaryEncryptor, CryptoEncryptor, ShiftChipher, save_code
from .getuser import Extract
from .logger import LoggerHandler
from .misc import Handler
from .trans import Translate

__version__ = "0.1.dev5"

mytoolsID = f"""
{"="*60}
  __  ____   __  _____ ___   ___  _     ____    ___ ____  
 |  \/  \ \ / / |_   _/ _ \ / _ \| |   / ___|  |_ _|  _ \ 
 | |\/| |\ V /    | || | | | | | | |   \___ \   | || | | |
 | |  | | | |     | || |_| | |_| | |___ ___) |  | || |_| |
 |_|  |_| |_|     |_| \___/ \___/|_____|____/  |___|____/ 
{"="*60}
"""

print(f"\033[1;37m{mytoolsID}\033[0m")
