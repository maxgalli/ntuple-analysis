import logging
logger = logging.getLogger(__name__)

class RDataFrameEssentials:
    def __init__(self,
            rdataframes,
            ttrees, tfiles):
        self.rdataframes = rdataframes
        self.ttrees = ttrees
        self.tfiles = tfiles
