import logging
logger = logging.getLogger(__name__)

class RDataFrameEssentials:
    def __init__(self,
            rdataframe,
            tchain = None):
        self.rdataframe = rdataframe
        self.tchain = tchain
