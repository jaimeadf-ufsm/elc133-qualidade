import os

class Settings:
    MAIN_BASE_URL = os.getenv('BASE_URL', 'https://www.uni-rostock.de')
    BSZ_BASE_URL = os.getenv('BSZ_BASE_URL', 'https://www.bsz.uni-rostock.de')