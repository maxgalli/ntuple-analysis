from .booking import AnalysisFlowUnit

import logging
logger = logging.getLogger(__name__)



class Graph(dict):
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
                [afu.selections[0]]))
        for (no_l, no_f) in \
                zip(afu.selections[:-1], afu.selections[1:]):
            nodes.append(
                Node(
                    no_l[1],
                    'selection',
                    no_f))
        nodes.append(
            Node(
                afu.selections[-1:][0].name,
                'selection',
                afu.action))
        nodes.append(
            Node(
                afu.action.name,
                'action'))
        return nodes


class GraphManager:
    def __init__(self, analysis_flow_units):
        self.graphs = [
            Graph(unit) \
                for unit in analysis_flow_units]

    def optimize(self):
        pass

