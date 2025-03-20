from os.path import dirname, join as joinpath
WEB_DIR = joinpath(dirname(__file__), 'web')

from .skateboard import Skateboard
__all__ = ["Skateboard"]