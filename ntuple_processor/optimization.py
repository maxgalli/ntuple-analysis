from .booking import AnalysisFlowUnit

from .utils import Node

import logging
logger = logging.getLogger(__name__)



class Graph(dict):
    """
    Way to represent a complete analysis flow which takes into
    consideration overlapping operations, condensing them in
    the same block.
    Dictionary of nodes, where every node is an object containing
    a name, a kind (dataset, selection, action), the corresponding
    block in the AnalysisFlowUnit world and a list of children.

    Args:
        analysis_flow_unit (AnalysisFlowUnit): analysis flow unit
            object from which a graph in its basic form is generated
    """
    def __init__(self,
            analysis_flow_unit = None):
        if analysis_flow_unit:
            nodes = self.__nodes_from_afu(
                analysis_flow_unit)
            for node in nodes:
                self[node.name] = node

    def __nodes_from_afu(self, afu):
        nodes = []
        nodes.append(
            Node(
                afu.dataset.name,
                'dataset',
                afu.dataset,
                afu.selections[0].name))
        for (no_l, no_f) in \
                zip(afu.selections[:-1], afu.selections[1:]):
            nodes.append(
                Node(
                    no_l.name,
                    'selection',
                    no_l,
                    no_f.name))
        nodes.append(
            Node(
                afu.selections[-1:][0].name,
                'selection',
                afu.selections[-1:][0],
                afu.action.name))
        nodes.append(
            Node(
                afu.action.name,
                'action',
                afu.action))
        # Debug
        logger.debug('Nodes in graph imported from AFU:\n')
        for node in nodes:
            logger.debug(node)
        return nodes


class GraphManager:
    """
    Manager for Graph-type objects, with the main function of
    optimize/merge them with the 'optimize' function.

    Args:
        analysis_flow_units (list): List of AnalysisFlowUnit
            objects used to fill the 'graphs' attribute

    Attributes:
        graphs (list): List of Graph objects that at some point
            will be merged and optimized
    """
    def __init__(self, analysis_flow_units):
        self.graphs = [
            Graph(unit) \
                for unit in analysis_flow_units]

    def add_graph(self, graph):
        self.graphs.append(graph)

    def add_graph_from_afu(self, afu):
        self.graphs.append(Graph(afu))

    def optimize(self):
        # at the moment dataset nodes and selection nodes have unambiguous names,
        # but histo and sum operations don't. this is fine in __node_from_afu since
        # there is only one operation at the end, but in the optimization process
        # we need to add another part to the name since in a graph we can have more
        # than one histo or sum and we need to distnguish
        pass
