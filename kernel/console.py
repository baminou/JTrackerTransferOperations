
from operations.base import Base
from operations.ega import EGA
from operations.song import Song
from operations.minibam import Minibam

def libraries():
    return {
        Base.name(): Base,
        EGA.name(): EGA,
        Song.name(): Song,
        Minibam.name(): Minibam
    }