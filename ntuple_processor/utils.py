import os
import re
import json



# Hidden

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



# Available to the user

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
