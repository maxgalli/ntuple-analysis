from ROOT import RDataFrame
from ROOT import TFile
from ROOT import TTree

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
            self.__node_to_root(graph)
        logger.debug('Final pointers: {}'.format(
            self.final_ptrs))

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

    def __node_to_root(self, node, rdf = None):
        logger.debug('%%%%%%%%%% Converting from Graph to ROOT language:\nNode:\n{}'.format(
            node))
        if node.kind == 'dataset':
            result = self.__rdf_from_dataset(
                node.afu_block)
        elif node.kind == 'selection':
            result = self.__filter_from_selection(
                rdf, node.afu_block)
        elif node.kind == 'action':
            if 'Count' in node.name:
                result = self.__sum_from_count(
                    rdf, node.afu_block)
            elif 'Histo' in node.name:
                result = self.__histo1d_from_histo(
                    rdf, node.afu_block)
        if node.children:
            for child in node.children:
                logger.debug('%%%%% Do not return, apply actions in:\n{}\n on RDF:\n{}'.format(child, result))
                self.__node_to_root(child, result)
        else:
            logger.debug('%%%%% Final return: append \n{} to final pointers'.format(
                result))
            if isinstance(result, list):
                for histo in result:
                    self.final_ptrs.append(histo)
            else:
                self.final_ptrs.append(result)

    def __rdf_from_dataset(self, dataset):
        t_names = [ntuple.directory for ntuple in \
            dataset.ntuples]
        if len(set(t_names)) == 1:
            tree_name = t_names.pop()
            logger.debug('%%%%%%%%%% RDataframe from dataset: using tree "{}"'.format(
                tree_name))
        else:
            raise NameError(
                'Impossible to create RDataFrame with different tree names')
        files = []
        for ntuple in dataset.ntuples:
            files.append(ntuple.path)
            for friend in ntuple.friends:
                files.append(friend.path)
        rdf = RDataFrame(tree_name, files)
        return rdf

    def __filter_from_selection(self, rdf, selection):
        l_rdf = rdf
        if selection.cuts:
            for cut in selection.cuts:
                rdf = l_rdf.Filter(cut[0])
                l_rdf = rdf
        return l_rdf

    def __sum_from_count(self, rdf, book_count):
        return rdf

    def __histo1d_from_histo(self, rdf, book_histo):
        # Debug
        def print_info(rdf):
            names = rdf.GetColumnNames()
            print('%%%%%%%%%% Booking histogram - RDF columns:')
            for name in names:
                print(name)
        logger.debug(print_info(rdf))
        logger.debug('%%%%% Columns scan DONE')

        var = book_histo.variable
        rdf_min = rdf.Min(var).GetValue()
        logger.debug('Minimum for variable {}: {}'.format(
            var, rdf_min))
        rdf_max = rdf.Max(var).GetValue()
        logger.debug('Maximum for variable {}: {}'.format(
            var, rdf_max))
        nbins_histos = list()
        for nbins in book_histo.binning:
            name = '_'.join([var,
                str(nbins)])
            nbins_histos.append(
                rdf.Histo1D((
                    name, name, nbins,
                    rdf_min, rdf_max),
                    var))
        return nbins_histos
