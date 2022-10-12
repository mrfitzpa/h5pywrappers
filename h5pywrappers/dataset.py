r"""For loading and saving HDF5 datasets.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For checking whether a file exists at a given path.
import pathlib

# For removing directories.
import shutil



# For saving HDF5 datasets and checking whether an object is an HDF5 dataset.
import h5py

# For checking whether an object is a numpy array.
import numpy as np

# For type-checking, validating, and converting objects.
import czekitout.check
import czekitout.convert



# For loading and pre-saving HDF5 objects.
import h5pywrappers.obj



############################
## Authorship information ##
############################

__author__     = "Matthew Fitzpatrick"
__copyright__  = "Copyright 2022"
__credits__    = ["Matthew Fitzpatrick"]
__maintainer__ = "Matthew Fitzpatrick"
__email__      = "mrfitzpa@uvic.ca"
__status__     = "Development"



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["load",
           "save"]



def load(dataset_id, read_only=True):
    r"""Load an HDF5 dataset from an HDF5 file.

    Note that users can access the HDF5 file object to which the HDF5 dataset of
    interest belongs via ``dataset.file``, where ``dataset`` is the HDF5 dataset
    of interest. To close the HDF5 file, users can run the command
    ``dataset.file.close()``, however by doing so, any other HDF5 objects
    belonging to that file will become unusable.

    Parameters
    ----------
    dataset_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the HDF5 dataset of interest.
    read_only : `bool`, optional
        If ``read_only`` is set to ``True``, then the HDF5 dataset of interest
        cannot be modified after loading it. Otherwise, if ``read_only`` is set
        to ``False``, then the HDF5 dataset of interest can be modified after
        loading it.

    Returns
    -------
    dataset : :class:`h5py.Dataset`
        The HDF5 dataset of interest.

    """
    dataset = h5pywrappers.obj.load(dataset_id, read_only)
    accepted_types = (h5py._hl.dataset.Dataset,)
    kwargs = {"obj": dataset,
              "obj_name": "dataset",
              "accepted_types": accepted_types}
    try:
        czekitout.check.if_instance_of_any_accepted_types(**kwargs)
    except BaseException as err:
        dataset.file.close()
        raise err

    return dataset



def _check_and_convert_dataset_id(ctor_params):
    dataset_id = ctor_params["dataset_id"]
    
    accepted_types = (h5pywrappers.obj.ID,)
    kwargs = {"obj": dataset_id,
              "obj_name": "dataset_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    return dataset_id



def _pre_serialize_dataset_id(dataset_id):
    serializable_rep = h5pywrappers.obj._pre_serialize_obj_id(dataset_id)
    
    return serializable_rep



def _de_pre_serialize_dataset_id(serializable_rep):
    dataset_id = h5pywrappers.obj._de_pre_serialize_obj_id(serializable_rep)

    return dataset_id



def save(dataset, dataset_id, write_mode="w-"):
    r"""Save an HDF5 dataset to an HDF5 file.

    Parameters
    ----------
    dataset : :class:`h5py.Dataset` | `array_like` | `str`
        The HDF5 dataset of interest to save to an HDF5 file.
    dataset_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying where to save the HDF5 dataset of interest.
    write_mode : "w" | "w-" | "a" | "a-", optional
        The write mode upon opening the HDF5 file to which to save the HDF5
        dataset of interest: if ``write_mode`` is set to ``"w"``, then the
        target HDF5 file is emptied prior to saving the HDF5 dataset of
        interest; else if ``write_mode`` is set to ``"w-"``, then the HDF5
        dataset of interest is saved unless a file already exists with the
        target filename, in which case an error is raised and the target HDF5
        file is left unmodified; else if ``write_mode`` is set to ``"a-"``, then
        the HDF5 dataset of interest is saved unless an HDF5 object already
        exists at the target HDF5 path of the target HDF5 file, in which case an
        error is raised and the target HDF5 file is left unmodified; else if
        ``write_mode`` is set to ``"a"``, then the HDF5 dataset of interest is
        saved without emptying the target HDF5 file, replacing any HDF5 object
        at the target HDF5 path should one exist prior to saving.

    Returns
    -------

    """
    dataset, write_mode = _pre_save(dataset, dataset_id, write_mode)

    filename = dataset_id.core_attrs["filename"]
    path_in_file = dataset_id.core_attrs["path_in_file"]

    try:
        with h5py.File(filename, "a") as file_obj:
            if isinstance(dataset, (np.ndarray, str)):
                file_obj.create_dataset(path_in_file, data=dataset)
            else:
                file_obj.copy(dataset, path_in_file)
    except BaseException as err:
        raise err

    return None



def _pre_save(dataset, dataset_id, write_mode):
    dataset = _check_dataset(dataset)

    write_mode = czekitout.convert.to_str_from_str_like(obj=write_mode,
                                                        obj_name="write_mode")
    accepted_values = ("w", "w-", "a", "a-")
    if write_mode not in accepted_values:
        raise ValueError(_pre_save_err_msg_1)

    h5pywrappers.obj._pre_save(dataset_id)

    filename = dataset_id.core_attrs["filename"]
    path_in_file = dataset_id.core_attrs["path_in_file"]
    parent_dir_path, rm_parent_dir_if_error_occurs = \
        h5pywrappers.obj._mk_parent_dir(filename)

    try:
        if write_mode in ("w", "w-"):
            if write_mode == "w-":
                if pathlib.Path(filename).is_file():
                    err_msg = _pre_save_err_msg_2.format(path_in_file, filename)
                    raise IOError(err_msg)
            with h5py.File(filename, "w") as file_obj:
                pass
        
        with h5py.File(filename, "a") as file_obj:
            if path_in_file in file_obj:
                if write_mode == "a-":
                    err_msg = _pre_save_err_msg_3.format(path_in_file, filename)
                    raise IOError(err_msg)
                del file_obj[path_in_file]
                
    except BaseException as err:
        if rm_parent_dir_if_error_occurs:
            shutil.rmtree(parent_dir_path)
        raise err

    return dataset, write_mode



def _check_dataset(dataset):
    if not isinstance(dataset, (h5py._hl.dataset.Dataset, str)):
        try:
            dataset = czekitout.convert.to_numpy_array(obj=dataset,
                                                       obj_name="dataset")
        except:
            raise TypeError(_check_dataset_err_msg_1)

    return dataset



###########################
## Define error messages ##
###########################

_pre_save_err_msg_1 = \
    ("The object ``write_mode`` must be one of the following strings: ``'w'``, "
     "``'w-'``, ``'a'``, or ``'a-'``.")
_pre_save_err_msg_2 = \
    ("Cannot save the dataset to the HDF5 path ``'{}'`` of the HDF5 file at "
     "the file path ``'{}'`` because an HDF5 file already exists at said file "
     "path and the parameter ``write_mode`` was set to ``'w-'``, which "
     "prohibits modifying any such pre-existing file.")
_pre_save_err_msg_3 = \
    ("Cannot save the dataset to the HDF5 path ``'{}'`` of the HDF5 file at "
     "the file path ``'{}'`` because an HDF5 object already exists there and "
     "the parameter ``write_mode`` was set to ``'a-'``, which prohibits "
     "replacing any such pre-existing HDF5 object.")

_check_dataset_err_msg_1 = \
    ("The object ``dataset`` must be array-like, an HDF5 dataset, or a string.")
