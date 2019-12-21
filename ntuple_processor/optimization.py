from .booking import AnalysisFlowUnit

from .utils import Node

import logging
logger = logging.getLogger(__name__)



class Graph(Node):
    """
    A Graph is itself a node where every has other nodes as children.
    Due to the way it is constructed, the root node will always be of
    kind 'dataset'.

    Args:
        analysis_flow_unit (AnalysisFlowUnit): analysis flow unit
            object from which a graph in its basic form is generated
    """
    def __init__(self, afu = None):
        if afu:
            Node.__init__(self,
                afu.dataset.name,
                'dataset',
                afu.dataset)
            nodes = self.__nodes_from_afu(afu)
            for no_last, no_first in zip(
                    nodes[:-1], nodes[1:]):
                no_last.children.append(no_first)
            self.children.append(nodes[0])
            # Debug
            def print_info(graph):
                for child in graph.children:
                    print('Node: \n{} \nChild: \n{}\n'.format(
                        graph, child))
                    print_info(child)
            logger.debug('\nConstruct graph from AFU:\n')
            logger.debug(print_info(self))

    def __nodes_from_afu(self, afu):
        nodes = []
        for selection in afu.selections:
            nodes.append(
                Node(
                    selection.name,
                    'selection',
                    selection))
        nodes.append(
            Node(
                afu.action.name,
                'action',
                afu.action))
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
        self.merge_datasets()

    def merge_datasets(self):
        logger.debug('Merge datasets:')
        merged_graphs = list()
        for graph in self.graphs:
            if graph not in merged_graphs:
                merged_graphs.append(graph)
            else:
                for merged_graph in merged_graphs:
                    if merged_graph == graph:
                        for child in graph.children:
                            merged_graph.children.append(child)
        # Debug
        logger.debug('Merged graphs:')
        for graph in merged_graphs:
            logger.debug(graph)
        self.graphs = merged_graphs
