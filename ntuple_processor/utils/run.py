import os
import re
import json

from ROOT import TFile

import logging
logger = logging.getLogger(__name__)



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

