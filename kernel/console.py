
from operations.base import Base
from operations.ega import EGA
from operations.song import Song
from operations.minibam import Minibam
from operations.icgc import ICGC
from operations.jtracker import jtracker

def libraries():
    return {
        Base.name(): Base,
        EGA.name(): EGA,
        Song.name(): Song,
        Minibam.name(): Minibam,
        ICGC.name(): ICGC,
        jtracker.name(): jtracker
    }