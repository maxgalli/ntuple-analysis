import os
import re
import json



# Classes


class Dataset:
    def __init__(self, name, files, friends = None):
        self._name = name
        self._files = files
        self._friends = friends

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, a_name):
        self._name = a_name

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, some_files):
        self._files = some_files

    @property
    def friends(self):
        return self._friends

    @friends.setter
    def friends(self, some_friends):
        self._friends = some_friends

    def add_to_files(*new_files):
        for new_file in new_files:
            self._files.append(new_file)

    def add_to_friends(*new_friends):
        for new_friend in new_friends:
            self._friends.append(new_friend)


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

