from .button import Button
from .chatbot import Api, ImageGen
from .database import DataBase
from .encrypt import FARNET, BinaryEncryptor
from .getuser import Extract
from .logger import LoggerHandler
from .misc import Handler
from .trans import Translate

__version__ = "0.0.0.1.dev0"

mytoolsID = """
                    __              __     ________     __       ______  _   __           _____           ___ __   _          
   ____ ___  __  __/ /_____  ____  / /____/  _/ __ \    \ \     / ____ \/ | / /___  _____/ ___/____  ____/ (_) /__(_)___      
  / __ `__ \/ / / / __/ __ \/ __ \/ / ___// // / / /     \ \   / / __ `/  |/ / __ \/ ___/\__ \/ __ \/ __  / / //_/ / __ \     
 / / / / / / /_/ / /_/ /_/ / /_/ / (__  )/ // /_/ /      / /  / / /_/ / /|  / /_/ / /   ___/ / /_/ / /_/ / / ,< / / / / /     
/_/ /_/ /_/\__, /\__/\____/\____/_/____/___/_____/      /_/   \ \__,_/_/ |_/\____/_/   /____/\____/\__,_/_/_/|_/_/_/ /_/      
          /____/                                               \____/                                                         
"""

print(f"\033[1;37;41m{mytoolsID}\033[0m")
