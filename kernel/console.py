
from operations.base import Base
from operations.ega import EGA
from operations.jtracker import jtracker

def libraries():
    return {
        Base.name(): Base,
        EGA.name(): EGA,
        jtracker.name(): jtracker
    }