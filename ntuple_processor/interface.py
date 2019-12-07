from ntuple_processor.utils import _load_database
from ntuple_processor.utils import _get_nicks_with_query
from ntuple_processor.utils import _get_complete_filenames
from ntuple_processor.utils import Dataset


def dataset_from_database(
        dataset_name, path_to_database,
        queries, files_base_directories,
        friends_base_directories):
    """Create a Dataset object from a database
    in JSON format.

    Keyword arguments:
    dataset_name -- name of the dataset
    path_to_database -- absolute path to a json file
    queries -- dictionary or list of dictionaries
    files_base_directories -- path (list of paths) to
    the files base directory (directories)
    friends_base_directories -- path (list of paths) to
    the friends base directory (directories)
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
