from ntuple_processor.utils import _load_database
from ntuple_processor.utils import _get_nicks_with_query
from ntuple_processor.utils import _get_complete_filenames
from ntuple_processor.utils import Dataset
from ntuple_processor.utils import CountBooker
from ntuple_processor.utils import HistoBooker



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



def dataset_from_database(
        dataset_name, path_to_database,
        queries, files_base_directories,
        friends_base_directories):
    """Create a Dataset object from a database
    in JSON format.

    Args:
        dataset_name (str): Name of the dataset
        path_to_database (str): Absolute path to a json file
        queries (dict, list): Dictionary or list of dictionaries
        files_base_directories (str, list): Path (list of paths) to
            the files base directory (directories)
        friends_base_directories (str, list): Path (list of paths) to
            the friends base directory (directories)

    Returns:
        dataset (Dataset): Dataset object containing .root files
    """
    database = _load_database(path_to_database)
    names = _get_nicks_with_query(database, queries)
    files = _get_complete_filenames(
        files_base_directories, names)
    friends = _get_complete_filenames(
        friends_base_directories, names)
    dataset = Dataset(
        dataset_name, files, friends)
    return dataset
