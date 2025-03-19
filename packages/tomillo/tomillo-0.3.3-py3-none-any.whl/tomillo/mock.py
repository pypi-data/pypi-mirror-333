from .core import Configuration as Config

from loguru import logger
from pathlib import Path

class Configuration(Config):

    def __init__(self, config: Path):
        self._stgfile = config
        self.project = 'mock'
        logger.debug('parsing settings file..')
        self.map = self.__parse()
