from ROOT import RDataFrame
from ROOT import TFile
from ROOT import TTree

from copy import deepcopy

import logging
logger = logging.getLogger(__name__)



class RunManager:
    """Convert the Graph-style language into PyROOT/RDataFrame
    language and schedule RDataFrame operations, like the
    following:
        Dataset()     -->   RDataFrame()
        Selection()   -->   Filter()
        BookCount()   -->   Sum()
        BookHisto()   -->   Histo1D()

    Args:
        graphs (list): List of Graph objects that are converted
            node by node to RDataFrame operations

    Attributes:
        final_ptrs (list): List of TH1D objects resulting from a
            set of Filter operations performed on RDataFrames; on
            all them we need to perform a Write operation
    """
    def __init__(self, graphs):
        self.final_ptrs = []
        for graph in graphs:
            # Create a dictionary with the same keys of the graph
            # one, that will be filled with RDataFrame objects:
            # since every key is a node of the Graph, the RDataFrame
            # associated to it is the pointer returned from the action
            # applied by the node on the RDataFrame associated to the
            # previous node.
            rdf_graph = deepcopy(graph)
            for node in graph.values():
                if node.kind == 'action':
                    continue
                if node.kind == 'dataset':
                    rdf_graph[node.name] = self.__rdf_from_dataset(
                        node.afu_block)
                for child in node.children:
                    kind = graph[child].kind
                    afu_block = graph[child].afu_block
                    if kind == 'selection':
                        rdf_graph[child] = self.__filter_from_selection(
                            rdf_graph[node.name], afu_block)
                    elif kind == 'action':
                        if 'Count' in child:
                            rdf_graph[child] = self.__sum_from_count(
                                rdf_graph[node.name], afu_block)
                        elif 'Histo' in child:
                            rdf_graph[child] = self.__histo1d_from_histo(
                                rdf_graph[node.name], afu_block)
                        self.final_ptrs.append(rdf_graph[child])

    def run_locally(self, of_name):
        """Save to file the histograms booked.

        Args:
            of_name (str): Name of the output .root
                file
        """
        root_file = TFile(of_name, 'RECREATE')
        for op in self.final_ptrs:
            op.Write()
        root_file.Close()

    def __rdf_from_dataset(self, dataset):
        t_names = [ntuple.directory for ntuple in \
            dataset.ntuples]
        if len(set(t_names)) == 1:
            tree_name = t_names.pop()
        else:
            raise NameError(
                'Impossible to create RDataFrame with \
                 different tree names')
        files = []
        for ntuple in dataset.ntuples:
            files.append(ntuple.path)
            for friend in ntuple.friends:
                files.append(friend.path)
        rdf = RDataFrame(tree_name, files)
        return rdf

    def __filter_from_selection(self, rdf, selection):
        l_rdf = rdf
        for cut in selection.cuts:
            rdf = l_rdf.Filter(cut[0])
            l_rdf = rdf
        return l_rdf

    def __sum_from_count(self, rdf, book_count):
        return rdf

    def __histo1d_from_histo(self, rdf, book_histo):
        return rdf.Histo1D(book_histo.variable)
