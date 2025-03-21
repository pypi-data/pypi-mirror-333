# VBCableSoundPlayer/__init__.py

from .VBCableSoundPlayer import VBCableSoundPlayer

VBCableSoundPlayer.init_player()

play = VBCableSoundPlayer.play

__version__ = "0.1.0"
__all__ = ['play']