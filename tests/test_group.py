# -*- coding: utf-8 -*-
# Copyright 2024 Matthew Fitzpatrick.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
r"""Contains tests for the module :mod:`h5pywrappers.group`.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For removing files.
import pathlib

# For removing directories.
import shutil



# For general array handling.
import numpy as np

# For operations related to unit tests.
import pytest



# For loading and saving HDF5 objects.
import h5pywrappers.obj

# For loading and saving HDF5 datasets.
import h5pywrappers.dataset

# For loading and saving HDF5 groups.
import h5pywrappers.group



##################################
## Define classes and functions ##
##################################



@pytest.fixture
def dataset_id():
    fixture_output = h5pywrappers.obj.ID(filename="./test_data/test_file.h5",
                                         path_in_file="group_1/dataset_1")

    return fixture_output



def test_1_of_load(dataset_id):
    kwargs = {"dataset": np.arange(10),
              "dataset_id": dataset_id,
              "write_mode": "w"}
    h5pywrappers.dataset.save(**kwargs)

    filename = dataset_id.core_attrs["filename"]
    path_to_group = "group_1"
    group_id = h5pywrappers.obj.ID(filename="./test_data/test_file.h5",
                                   path_in_file="group_1")
    group = h5pywrappers.group.load(group_id, read_only=True)

    path_1 = pathlib.Path(group.name).resolve()
    path_2 = pathlib.Path(path_to_group).resolve()
    assert group.name == path_to_group

    path_1 = pathlib.Path(group.file.filename).resolve()
    path_2 = pathlib.Path(filename).resolve()
    assert path_1 == path_2

    group.file.close()

    shutil.rmtree(pathlib.Path(filename).parent)
            
    return None



###########################
## Define error messages ##
###########################
