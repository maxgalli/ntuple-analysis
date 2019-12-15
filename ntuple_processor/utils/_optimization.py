import logging
logger = logging.getLogger(__name__)

class Node:
    def __init__(self,
            name, kind, afu_block, *children):
        self.name = name
        self.kind = kind
        self.afu_block = afu_block
        self.children = [
            child for child in children]
