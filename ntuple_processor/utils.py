import os
import re
import json

from ROOT import TFile



# Classes


class NtupleBase:

    def __init__(self, path, directory):
        self.path = path
        self.directory = directory


class Friend(NtupleBase):

    pass


class Ntuple(NtupleBase):

    def __init__(self, path, directory, *args):
        NtupleBase.__init__(self, path, directory)
        self.friends = [ntuple for ntuple in args]

    def add_to_friends(*new_friends):
        for new_friend in new_friends:
            self.friends.append(new_friend)


class Dataset:

    def __init__(self, name, *args):
        self.name = name
        self.ntuples = [ntuple for ntuple in args]

    def add_to_ntuples(*new_ntuples):
        for new_ntuple in new_ntuples:
            self.ntuples.append(new_ntuple)


class Selection:
    def __init__(
            self, name = None,
            cuts = None, weights = None):
        self.name = name
        self.set_cuts(cuts)
        self.set_weights(weights)

    def set_cuts(self, cuts):
        if cuts is not None:
            try:
                _check_format(cuts)
                self.cuts = cuts
            except TypeError as err:
                print(err, 'Cuts assigned to None')
                self.cuts = None
        else:
            pass

    def set_weights(self, weights):
        if weights is not None:
            try:
                _check_format(weights)
                self.weights = weights
            except TypeError as err:
                print(err, 'Weights assigned to None')
                self.weights = None
        else:
            pass


class CountBooker:

    def __init__(
            self, dataset, selections):
        self.dataset = dataset
        self.selections = selections


class HistoBooker(CountBooker):

    def __init__(
            self, dataset, selections,
            binning, variable):
        CountBooker.__init__(self, dataset, selections)
        self.binning = binning
        self.variable = variable



# Functions


def _load_database(path_to_database):
    if not os.path.exists(path_to_database):
        raise Exception
    return json.load(open(path_to_database, "r"))


def _check_recursively(entry, query, database):
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


def _get_nicks_with_query(database, query):
    nicks = []
    if isinstance(query, list):
        for s_query in query:
            for entry in database:
                passed = _check_recursively(
                    entry, s_query, database)
                if passed:
                    nicks.append(entry)
    else:
        for entry in database:
            passed = _check_recursively(
                entry, query, database)
            if passed:
                nicks.append(entry)
    return nicks


def _get_complete_filenames(directory, files):
    full_paths = []
    if isinstance(directory, list):
        for s_directory in directory:
            for f in files:
                full_paths.append(
                    os.path.join(
                        s_directory, f, "{}.root".format(f)
                        )
                    )
    else:
        for f in files:
            full_paths.append(
                os.path.join(
                    directory, f, "{}.root".format(f)
                    )
                )
    return full_paths


def _check_format(list_of_dtuples):
    if isinstance(list_of_dtuples, list):
        for dtuple in list_of_dtuples:
            if isinstance(dtuple, tuple)\
                    and len(dtuple) == 2:
                return True
            else:
                raise TypeError(
                        'TypeError: tuples of lenght 2 are needed.\n')
    else:
        raise TypeError(
                'TypeError: a list of tuples is needed.\n')


def _get_list_of_TDF_names(st_channel, root_file_name):
    root_file = TFile(root_file_name)
    return [key.GetName() for key in root_file.GetListOfKeys() \
        if key.GetName().startswith(st_channel)]


def _add_trees_from_dataset_files_to_TChain(
        chain, st_channel, file_names, tree_name):
    for file_name in file_names:
        TDF_names = _get_list_of_TDF_names(
            st_channel, file_name)
        for TDF_name in TDF_names:
            chain.Add(
                '/'.join(
                    [file_name, TDF_name,
                     tree_name]))
