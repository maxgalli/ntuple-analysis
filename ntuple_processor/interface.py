from ntuple_processor.utils import Dataset
from ntuple_processor.utils import CountBooker
from ntuple_processor.utils import HistoBooker
from ntuple_processor.utils import _add_trees_from_dataset_files_to_TChain
from ntuple_processor.utils import Friend
from ntuple_processor.utils import Ntuple
from ntuple_processor.utils import Dataset

from ROOT import TChain
from ROOT import RDataFrame
from ROOT import TFile

import os
import re
import json



class ResultManager:
    """
    Container for 'schedule'-type objects.

    Attributes:
        __booked_counts (CountBooker): list of scheduled
        CountBooker objects, initially empty
        __booked_histos (HistoBooker): list of scheduled
        HistoBooker objects, initially empty
    """
    def __init__(self):
        self.__booked_counts = []
        self.__booked_histos = []

    def get_booked_counts(self):
        return self.__booked_counts

    def get_booked_histos(self):
        return self.__booked_histos

    def book_count(self, dataset, selections):
        """Book a '.Count' operation by adding it to
        the __booked_counts list.
        """
        self.__booked_counts.append(
            CountBooker(dataset, selections))

    def book_histo(self, dataset, selections,
            binning, variable):
        """Book a '.Histo' operation by adding it to
        the __booked_histos list.
        """
        self.__booked_histos.append(
                HistoBooker(
                    dataset, selections,
                    binning, variable))


class RunManager:
    """PyROOT based objects taking a schedule-type object
    as argument and a channel which create RDataFrames
    based on the above mentioned schedule-type object.

    Args:
        channel (str): 'em', 'et', 'mt', 'tt', channel(s)
            for which we want to create a set of RDataFrames
        schedule (ResultManager): Set of histos/counts
            booked, from which we get the information to pass
            to the .Filter and .Histo1D operations

    Attributes:
        __tchains (list): list of ROOT.TChain objects, each
            with a one-to-one correspondence with the elements
            of 'schedule'
        __input_dataframes (list): list of ROOT.RDataFrame
            objects created from the elements of __tchains
        __output_dataframes (list): list of ROOT.RDataFrame
            objects generated by applying the operations
            in 'schedule' to the elements of __input_dataframes
        __histos (list): list of ROOT.TH1D objects generated by
            applying the operation .Histo1D() to the elements
            of __output_dataframes
    """
    def __init__(self, channel, schedule):
        self.__tchains = []
        for booked_histo in schedule.get_booked_histos():
            self.__tchains.append(
                self._get_tchain_from_dataset(
                    channel, booked_histo.get_dataset()))
        self.__input_dataframes = []
        for chain in self.__tchains:
            self.__input_dataframes.append(
                RDataFrame(chain))
        self.__output_dataframes = []
        for (in_rdf, booked_histo) in \
                zip(self.__input_dataframes,
                        schedule.get_booked_histos()):
            self.__output_dataframes.append(
                self._apply_selections(
                    in_rdf,
                    booked_histo.get_selections()))
        self.__histos = []
        for (out_rdf, booked_histo) in \
                zip(self.__output_dataframes,
                        schedule.get_booked_histos()):
            self.__histos.append(
                self._get_histos_from_dataframes(
                    out_rdf,
                    booked_histo.get_variable()))

    def get_tchains(self):
        return self.__tchains

    def get_input_RDFs(self):
        return self.__input_dataframes

    def get_output_RDFs(self):
        return self.__output_dataframes

    def run_locally(self, of_name):
        """Save to file the histograms booked.

        Args:
            of_name (str): Name of the output .root
                file
        """
        root_file = TFile(of_name, 'RECREATE')
        for histo in self.__histos:
            histo.Write()
        root_file.Close()

    def _get_tchain_from_dataset(self, channel, dataset):
        chain = TChain()
        _add_trees_from_dataset_files_to_TChain(
            chain, channel,
            dataset.get_files(),
            'ntuple')
        _add_trees_from_dataset_files_to_TChain(
            chain, channel,
            dataset.get_friends(),
            'ntuple')
        return chain

    def _apply_selections(self, in_rdf, selections):
        local_rdf = in_rdf
        if selections is not None:
            for selection in selections:
                for cut in selection:
                    out_rdf = local_rdf.Filter(cut[0])
                    local_rdf = out_rdf
        else:
            out_rdf = in_rdf
        return out_rdf

    def _get_histos_from_dataframes(self, rdf, var):
        return rdf.Histo1D(var)



class DatasetFromDatabase:
    """Fake class introduced to simulate a static behavior for
    the dataset, in order for it to be created only once.
    The function can be called with the name 'dataset_from_database'
    from the API.

    Attributes:
        dataset (Dataset): Dataset object created with the function
        inner_dataset_from_database
    """
    def __init__(self):
        self.dataset = None

    def __call__(
            self,
            dataset_name, path_to_database,
            queries, channel,
            files_base_directories,
            friends_base_directories):
        if self.dataset is None:
            self.dataset = self.inner_dataset_from_database(
                dataset_name, path_to_database,
                queries, channel,
                files_base_directories,
                friends_base_directories)
        return self.dataset

    def inner_dataset_from_database(
            self,
            dataset_name, path_to_database,
            queries, channel,
            files_base_directories,
            friends_base_directories):
        """Create a Dataset object from a database
        in JSON format.

        Args:
            dataset_name (str): Name of the dataset
            path_to_database (str): Absolute path to a json file
            queries (dict, list): Dictionary or list of dictionaries
            channel (str): Channel that determines also the queries
            files_base_directories (str, list): Path (list of paths) to
                the files base directory (directories)
            friends_base_directories (str, list): Path (list of paths) to
                the friends base directory (directories)

        Returns:
            dataset (Dataset): Dataset object containing TTrees
        """
        def load_database(path_to_database):
            if not os.path.exists(path_to_database):
                raise Exception
            return json.load(open(path_to_database, "r"))

        def check_recursively(entry, query, database):
            for attribute in query:
                q_att = query[attribute]
                d_att = database[entry][attribute]
                if isinstance(d_att, str) or isinstance(d_att, str):
                    result = re.match(q_att, d_att)
                    if result == None:
                        return False
                elif isinstance(d_att, bool):
                    if not q_att == d_att:
                        return False
                else:
                    raise Exception
            return True

        def get_nicks_with_query(database, query):
            nicks = []
            if isinstance(query, list):
                for s_query in query:
                    for entry in database:
                        passed = check_recursively(
                            entry, s_query, database)
                        if passed:
                            nicks.append(entry)
            else:
                for entry in database:
                    passed = check_recursively(
                        entry, query, database)
                    if passed:
                        nicks.append(entry)
            return nicks

        def get_complete_filenames(directory, files):
            full_paths = []
            for f in files:
                full_paths.append(
                    os.path.join(
                        directory, f, "{}.root".format(f)
                        )
                    )
            return full_paths

        def get_full_tree_names(
                channel, path_to_root_file, tree_name):
            root_file = TFile(path_to_root_file)
            full_tree_names = []
            for key in root_file.GetListOfKeys():
                if key.GetName().startswith(channel):
                    full_tree_names.append(
                        '/'.join([key.GetName(), tree_name]))
            return full_tree_names

        database = load_database(path_to_database)
        names = get_nicks_with_query(database, queries)
        root_files = get_complete_filenames(
            files_base_directories, names)
        ntuples = []
        for (root_file, name) in zip(root_files, names):
            tdfs_tree = get_full_tree_names(
                channel, root_file, 'ntuple')
            for tdf_tree in tdfs_tree:
                friends = []
                friend_paths = []
                for friends_base_directory in friends_base_directories:
                    friend_paths.append(os.path.join(
                        friends_base_directory, name, "{}.root".format(name)))
                for friend_path in friend_paths:
                    friends.append(Friend(friend_path, tdf_tree))
                ntuples.append(Ntuple(root_file, tdf_tree, friends))
        dataset = Dataset(dataset_name, ntuples)
        return dataset

dataset_from_database = DatasetFromDatabase()
