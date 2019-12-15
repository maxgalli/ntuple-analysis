import logging
logger = logging.getLogger(__name__)



class NtupleBase:

    def __init__(self, path, directory):
        self.path = path
        self.directory = directory


class Friend(NtupleBase):

    pass


class Ntuple(NtupleBase):

    def __init__(self, path, directory, friends = None):
        NtupleBase.__init__(self, path, directory)
        self.friends = friends

    def add_to_friends(*new_friends):
        for new_friend in new_friends:
            self.friends.append(new_friend)


class Dataset:

    def __init__(self, name, ntuples):
        self.name = name
        self.ntuples = ntuples

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
                self.__check_format(cuts)
                self.cuts = cuts
            except TypeError as err:
                print(err, 'Cuts assigned to None')
                self.cuts = None
        else:
            pass

    def set_weights(self, weights):
        if weights is not None:
            try:
                self.__check_format(weights)
                self.weights = weights
            except TypeError as err:
                print(err, 'Weights assigned to None')
                self.weights = None
        else:
            pass

    def __check_format(self, list_of_dtuples):
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


class Action:
    def __init__(self, name):
        self.name = name


class BookCount(Action):
    def __init__(self):
        self.name = 'BookCount'


class BookHisto(Action):
    def __init__(
            self,
            binning, variable):
        self.name = 'BookHisto'
        self.binning = binning
        self.variable = variable

