from ntuple_processor.utils import Dataset
from ntuple_processor.utils import Friend
from ntuple_processor.utils import Ntuple

from ntuple_processor.utils import Action
from ntuple_processor.utils import BookCount
from ntuple_processor.utils import BookHisto

from ROOT import TFile

import os
import re
import json

import logging
logger = logging.getLogger(__name__)


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

class AnalysisFlowUnit:
    """
    Building block of a minimal analysis flow, consisting
    of a dataset, a set of selections to apply on the data
    and an action.

    Attributes:
        dataset (Dataset): Set of TTree objects to run the
            analysis on
        selections (list): List of Selection-type objects
        action (Action): Action to perform on the processed
            dataset, can be 'Histo1D' or 'Sum'
    """
    def __init__(
            self,
            dataset, selections, action = None):
        self.__set_dataset(dataset)
        self.__set_selections(selections)
        self.__set_action(action)

    def __str__(self):
        layout = '\n'.join([
            'Dataset: {}'.format(self.dataset.name),
            'Selections: {}'.format(self.selections),
            'Action: {}'.format(self.action)])
        return layout

    def book_count(self):
        self.action = BookCount()

    def book_histo(self, binning, variable):
        self.action = BookHisto(
            self.binning, self.variable)

    def __set_dataset(self, dataset):
        if isinstance(dataset, Dataset):
            self.dataset = dataset
        else:
            raise TypeError(
                'TypeError: not a Dataset object.')

    def __set_selections(self, selections):
        if isinstance(selections, list):
            self.selections = selections
        else:
            raise TypeError(
                'TypeError: not a list object.')

    def __set_action(self, action):
        if isinstance(action, Action):
            self.action = action
        else:
            raise TypeError(
                    'TypeError: not an Action object.')


class AnalysisFlowManager:
    """
    Manager of all the AnalysisFlowUnit objects that are created.
    It can both be initialized with a variable amount of AnalysisFlowUnit
    objects as arguments or with no arguments, with the above mentioned
    objects added in a second time with the functions 'book_count' and
    'book_histo'.

    Args:
        *args (AnalysisFlowUnit): Objects with the structure [dataset,
            selections, action]

    Attributes:
        booked_units (list): List of the booked units, updated during
            initialization or with the functions 'book_count' and
            'booked_histo'
    """

    def __init__(self, *args):
        self.booked_units = [arg for arg in args]

    def book_count(self,
            dataset, selections):
        self.booked_units.append(
            AnalysisFlowUnit(
                dataset, selections, BookCount()))

    def book_histo(self,
            dataset, selections,
            binning, variable):
        self.booked_units.append(
            AnalysisFlowUnit(
                dataset, selections, BookHisto(
                    binning, variable)))

