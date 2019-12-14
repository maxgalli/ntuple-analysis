import logging
logger = logging.getLogger(__name__)

class Node:
    def __init__(self,
            name, kind, *children):
        self.name = name
        self.kind = kind
        self.children = [
            child for child in children]
