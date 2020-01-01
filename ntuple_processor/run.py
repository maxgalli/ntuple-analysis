from .utils import RDataFrameEssentials

from ROOT import RDataFrame
from ROOT import TFile
from ROOT import TChain

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
            # This gets the name of the graph being used
            # (which is also the name of the dataset
            # related to this graph), to put it in the
            # histogram name.
            self._last_used_dataset = graph.name
            #logger.debug('Last used dataset called {}'.format(
                #self._last_used_dataset))
            self.__node_to_root(graph)
        logger.debug('%%%%%%%%%% Final pointers (histos and cunts): {}'.format(
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
        logger.debug('%%%%%%%%%% __node_to_root, converting from Graph to ROOT language the following node\n{}'.format(
            node))
        if node.kind == 'dataset':
            rdf_ess = self.__rdf_from_dataset(
                node.afu_block)
            result = rdf_ess.rdataframe
        elif node.kind == 'selection':
            result = self.__cuts_and_weights_from_selection(
                rdf, node.afu_block)
        elif node.kind == 'action':
            if 'Count' in node.name:
                result = self.__sum_from_count(
                    rdf, node.afu_block)
            elif 'Histo' in node.name:
                result = self.__histo1d_from_histo(
                    rdf, node.afu_block, self._last_used_dataset)
        if node.children:
            for child in node.children:
                logger.debug('%%%%% __node_to_root, do not return; apply actions in "{}" on RDF "{}"'.format(
                    child.__repr__(), result))
                self.__node_to_root(child, result)
        else:
            logger.debug('%%%%% __node_to_root, final return: append \n{} to final pointers'.format(
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
        else:
            raise NameError(
                'Impossible to create RDataFrame with different tree names')
        chain = TChain(tree_name)
        for ntuple in dataset.ntuples:
            chain.Add(ntuple.path)
            for friend in ntuple.friends:
                f_chain = TChain(friend.directory)
                f_chain.Add(friend.path)
                chain.AddFriend(f_chain)
        rdf = RDataFrame(chain)
        return RDataFrameEssentials(rdf, chain)

    def __cuts_and_weights_from_selection(self, rdf, selection):
        # Also define a column with the name, to keep track and use in the histogram name
        # Is it really the best solution?
        logger.debug('%%%%% Initial number of events for selection {}: {}'.format(
            selection.name, rdf.Count().GetValue()))
        selection_name = '__selection__' + selection.name
        logger.debug('%%%%% Defining fake column with selection name {}'.format(
            selection_name))
        l_rdf = rdf.Define(selection_name, '1')
        if selection.cuts:
            for cut in selection.cuts:
                logger.debug('%%%%% Creating Filter from cut {}'.format(
                    cut))
                rdf = l_rdf.Filter(cut[0])
                l_rdf = rdf
        if selection.weights:
            weight_name = '__weight__' + selection.name
            weight_expression = '*'.join([
                weight[0] for weight in selection.weights])
            rdf = l_rdf.Define(
                weight_name,
                weight_expression)
            logger.debug('%%%%% Defining {} column with weight expression {}'.format(
                weight_name,
                weight_expression))
            l_rdf = rdf
        return rdf

    def __sum_from_count(self, rdf, book_count):
        return rdf.Sum(book_count.variable)

    def __histo1d_from_histo(self, rdf, book_histo, dataset_name):
        var = book_histo.variable
        rdf_min = rdf.Min(var).GetValue()
        logger.debug('Minimum for variable {}: {}'.format(
            var, rdf_min))
        rdf_max = rdf.Max(var).GetValue()
        logger.debug('Maximum for variable {}: {}'.format(
            var, rdf_max))
        nbins_histos = list()

        cut_prefix = '__selection__'
        selection_names = '-'.join([
            column[len(cut_prefix):] for column in rdf.GetColumnNames() \
                    if column.startswith(cut_prefix)])

        weight_expression = '*'.join([
            name for name in rdf.GetColumnNames() if name.startswith(
                '__weight__')])
        logger.debug('%%%%%%%%%% Histo1D from histo: created weight expression {}'.format(
            weight_expression))

        for nbins in book_histo.binning:
            name = '#'.join([var,
                dataset_name,
                selection_names,
                str(nbins)])
            if not weight_expression:
                nbins_histos.append(
                    rdf.Histo1D((
                        name, name, nbins,
                        rdf_min, rdf_max),
                        var))
            else:
                weight_name = 'Weight'
                logger.debug('%%%%%%%%%% Histo1D from histo: defining {} column with weight expression {}'.format(
                    weight_name, weight_expression))
                l_rdf = rdf.Define(weight_name, weight_expression)
                nbins_histos.append(
                    l_rdf.Histo1D((
                        name, name, nbins,
                        rdf_min, rdf_max),
                        var, weight_expression))

        # Debug
        def print_infos(histos):
            for histo in histos:
                print('%%%%% Info for histogram {}'.format(histo.GetName()))
                histo.Print('all')
        print_infos(nbins_histos)

        return nbins_histos
