from .button import Button
from .chatbot import Api, ImageGen
from .database import LocalDataBase, MongoDataBase
from .encrypt import BinaryEncryptor, CryptoEncryptor
from .getuser import Extract
from .logger import LoggerHandler
from .misc import Handler
from .trans import Translate

__version__ = "0.0.0.1.dev4"

mytoolsID = """
  __  ____     _________ ____   ____  _       _____ _____ _____        __     ____               _   _  ____  _____   _____  ____  _____ _____ _  _______ _   _ 
 |  \/  \ \   / /__   __/ __ \ / __ \| |     / ____|_   _|  __ \      / /    / /\ \        ____ | \ | |/ __ \|  __ \ / ____|/ __ \|  __ \_   _| |/ /_   _| \ | |
 | \  / |\ \_/ /   | | | |  | | |  | | |    | (___   | | | |  | |    / /    / /  \ \      / __ \|  \| | |  | | |__) | (___ | |  | | |  | || | | ' /  | | |  \| |
 | |\/| | \   /    | | | |  | | |  | | |     \___ \  | | | |  | |   < <    / /    > >    / / _` | . ` | |  | |  _  / \___ \| |  | | |  | || | |  <   | | | . ` |
 | |  | |  | |     | | | |__| | |__| | |____ ____) |_| |_| |__| |    \ \  / /    / /    | | (_| | |\  | |__| | | \ \ ____) | |__| | |__| || |_| . \ _| |_| |\  |
 |_|  |_|  |_|     |_|  \____/ \____/|______|_____/|_____|_____/      \_\/_/    /_/      \ \__,_|_| \_|\____/|_|  \_\_____/ \____/|_____/_____|_|\_\_____|_| \_|
                                                                                          \____/                                                                
"""

print(f"\033[1;37;41m{mytoolsID}\033[0m")
