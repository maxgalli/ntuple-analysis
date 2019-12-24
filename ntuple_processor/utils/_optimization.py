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

    def __str__(self):
        layout = '\n'.join([
            'Name: {}'.format(self.name),
            'Kind: {}'.format(self.kind),
            'AnalysisFlowUnit: {}'.format(self.afu_block),
            'Children: {}'.format(self.children)])
        return layout

    def __eq__(self, other):
        logger.debug('__eq__ compares: names ({} with {}), kinds ({} and {}) and AFU blocks ({} and {})'.format(
                self.name, other.name,
                self.kind, other.kind,
                self.afu_block, other.afu_block))
        return self.name == other.name and \
            self.kind == other.kind and \
            self.afu_block == other.afu_block

    def __hash__(self):
        return hash((
            self.name, self.kind, self.afu_block))

