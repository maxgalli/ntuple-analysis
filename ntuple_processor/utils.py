import os
import re
import json

from ROOT import TFile



# Classes


class Dataset:
    def __init__(self, name, files, friends = None):
        self.__name = name
        self.__files = files
        self.__friends = friends

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_files(self):
        return self.__files

    def set_files(self, files):
        self.__files = files

    def get_friends(self):
        return self.__friends

    def set_friends(self, friends):
        self.__friends = friends

    def add_to_files(*new_files):
        for new_file in new_files:
            self.__files.append(new_file)

    def add_to_friends(*new_friends):
        for new_friend in new_friends:
            self.__friends.append(new_friend)


class Selection:
    def __init__(
            self, name = None,
            cuts = None, weights = None):
        self.set_name(name)
        self.set_cuts(cuts)
        self.set_weights(weights)

    def get_name(self):
        return self.__name

    def get_cuts(self):
        return self.__cuts

    def get_weights(self):
        return self.__weights

    def set_name(self, name):
        self.__name = str(name)

    def set_cuts(self, cuts):
        if cuts is not None:
            try:
                _check_format(cuts)
                self.__cuts = cuts
            except TypeError as err:
                print(err, 'Cuts assigned to None')
                self.__cuts = None
        else:
            pass

    def set_weights(self, weights):
        if weights is not None:
            try:
                _check_format(weights)
                self.__weights = weights
            except TypeError as err:
                print(err, 'Weights assigned to None')
                self.__weights = None
        else:
            pass


class CountBooker:

    def __init__(
            self, dataset, selections):
        self.set_dataset(dataset)
        self.set_selections(selections)

    def get_dataset(self):
        return self.__dataset

    def get_selections(self):
        return self.__selections

    def set_dataset(self, dataset):
        self.__dataset = dataset

    def set_selections(self, selections):
        self.__selections = selections


class HistoBooker(CountBooker):

    def __init__(
            self, dataset, selections,
            binning, variable):
        CountBooker.__init__(self, dataset, selections)
        self.set_binning(binning)
        self.set_variable(variable)

    def get_binning(self):
        return self.__binning

    def get_variable(self):
        return self.__variable

    def set_binning(self, binning):
        self.__binning = binning

    def set_variable(self, variable):
        self.__variable = variable



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
