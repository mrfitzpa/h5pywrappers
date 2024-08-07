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
r"""For loading and saving HDF5 "scalars".

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For accessing attributes of functions.
import inspect



# For loading and saving HDF5 datasets.
import h5pywrappers.dataset



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["load",
           "save"]



def _check_and_convert_scalar_id(params):
    current_func_name = inspect.stack()[0][3]
    char_idx = 19
    obj_name = current_func_name[char_idx:]

    param_name_1 = "obj_id"
    param_name_2 = "name_of_obj_alias_of_"+param_name_1
    params = params.copy()
    params[param_name_2] = obj_name
    params[param_name_1] = params[params[param_name_2]]

    module_alias = h5pywrappers.obj
    basename_of_func_alias = current_func_name[:char_idx]+param_name_1
    func_alias = module_alias.__dict__[basename_of_func_alias]
    scalar_id = func_alias(params)

    return scalar_id



def load(scalar_id):
    r"""Load an HDF5 "scalar" from an HDF5 file.

    By "scalar", we mean the single data element from a zero-dimensional HDF5
    dataset.

    Parameters
    ----------
    scalar_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the HDF5 scalar of interest.

    Returns
    -------
    scalar : `float` | `complex`
        The HDF5 scalar of interest.

    """
    params = locals()
    for param_name in params:
        func_name = "_check_and_convert_" + param_name
        func_alias = globals()[func_name]
        params[param_name] = func_alias(params)

    func_name = "_" + inspect.stack()[0][3]
    func_alias = globals()[func_name]
    kwargs = params
    scalar = func_alias(**kwargs)

    return scalar



def _load(scalar_id):
    current_func_name = inspect.stack()[0][3]

    kwargs = {"dataset_id": scalar_id, "read_only": True}
    dataset = h5pywrappers.dataset.load(**kwargs)

    if len(dataset.shape) != 0:
        dataset.file.close()
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise TypeError(err_msg)
    
    try:
        scalar = complex(dataset[()])
        dataset.file.close()
    except:
        dataset.file.close()
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise TypeError(err_msg)

    if scalar.imag == 0:
        scalar = scalar.real

    return scalar



def _check_and_convert_scalar(params):
    current_func_name = inspect.stack()[0][3]
    char_idx = 19
    obj_name = current_func_name[char_idx:]

    param_name_1 = "dataset"
    param_name_2 = "name_of_obj_alias_of_"+param_name_1
    params = params.copy()
    params[param_name_2] = obj_name
    params[param_name_1] = params[params[param_name_2]]

    try:
        module_alias = h5pywrappers.dataset
        basename_of_func_alias = current_func_name[:char_idx]+param_name_1
        func_alias = module_alias.__dict__[basename_of_func_alias]
        scalar = func_alias(params)

        if len(scalar.shape) != 0:
            raise

        complex(scalar[()])
    except:
        err_msg = globals()[current_func_name+"_err_msg_1"]
        raise TypeError(err_msg)

    return scalar



def _check_and_convert_write_mode(params):
    current_func_name = inspect.stack()[0][3]
    
    module_alias = h5pywrappers.dataset
    basename_of_func_alias = current_func_name
    func_alias = module_alias.__dict__[basename_of_func_alias]
    write_mode = func_alias(params)

    return write_mode



_module_alias = h5pywrappers.dataset
_default_write_mode = _module_alias._default_write_mode



def save(scalar, scalar_id, write_mode=_default_write_mode):
    r"""Save an HDF5 "scalar" to an HDF5 file as a zero-dimensional HDF5 
    dataset.

    By "scalar", we mean the single numerical data element from a
    zero-dimensional HDF5 dataset.

    Parameters
    ----------
    scalar : `float` | `complex` | :class:`h5py.Dataset`
        The HDF5 scalar of interest to save to an HDF5 file.
    scalar_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying where to save the HDF5 scalar of interest.
    write_mode : "w" | "w-" | "a" | "a-", optional
        The write mode upon opening the HDF5 file to which to save the HDF5
        scalar of interest: if ``write_mode`` is set to ``"w"``, then the target
        HDF5 file is emptied prior to saving the HDF5 scalar of interest; else
        if ``write_mode`` is set to ``"w-"``, then the HDF5 scalar of interest
        is saved unless a file already exists with the target filename, in which
        case an error is raised and the target HDF5 file is left unmodified;
        else if ``write_mode`` is set to ``"a-"``, then the HDF5 scalar of
        interest is saved unless an HDF5 object already exists at the target
        HDF5 path of the target HDF5 file, in which case an error is raised and
        the target HDF5 file is left unmodified; else if ``write_mode`` is set
        to ``"a"``, then the HDF5 scalar of interest is saved without emptying
        the target HDF5 file, replacing any HDF5 object at the target HDF5 path
        should one exist prior to saving.

    Returns
    -------

    """
    params = locals()
    for param_name in params:
        func_name = "_check_and_convert_" + param_name
        func_alias = globals()[func_name]
        params[param_name] = func_alias(params)

    func_name = "_" + inspect.stack()[0][3]
    func_alias = globals()[func_name]
    kwargs = params
    func_alias(**kwargs)

    return None



def _save(scalar, scalar_id, write_mode):
    kwargs = {"dataset": scalar,
              "dataset_id": scalar_id,
              "write_mode": write_mode}
    h5pywrappers.dataset.save(**kwargs)

    return None



###########################
## Define error messages ##
###########################

_load_err_msg_1 = \
    ("The object at the HDF5 path of the HDF5 file specified by the parameter "
     "``scalar_id`` is not of the expected type, i.e. an HDF5 scalar.")

_check_and_convert_scalar_err_msg_1 = \
    ("The object ``scalar`` must be of the type `float` or `complex`, or it "
     "must be a zero-dimensional HDF5 dataset containing numerical data.")
