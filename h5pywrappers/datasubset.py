r"""For loading and saving HDF5 "datasubsets".

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For general array handling.
import numpy as np

# For updating HDF5 datasets.
import h5py

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For loading and saving HDF5 datasets.
import h5pywrappers.dataset



############################
## Authorship information ##
############################

__author__     = "Matthew Fitzpatrick"
__copyright__  = "Copyright 2023"
__credits__    = ["Matthew Fitzpatrick"]
__maintainer__ = "Matthew Fitzpatrick"
__email__      = "mrfitzpa@uvic.ca"
__status__     = "Development"



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["ID",
           "load",
           "save"]



def _check_and_convert_multi_dim_slice(ctor_params):
    multi_dim_slice = ctor_params["multi_dim_slice"]
    if multi_dim_slice is not None:
        kwargs = {"obj": multi_dim_slice, "obj_name": "multi_dim_slice"}
        multi_dim_slice = czekitout.convert.to_multi_dim_slice(**kwargs)

    return multi_dim_slice



def _pre_serialize_multi_dim_slice(multi_dim_slice):
    if multi_dim_slice is not None:
        serializable_rep = list(multi_dim_slice)
        for idx, single_dim_slice in enumerate(multi_dim_slice):
            if isinstance(single_dim_slice, slice):
                serializable_rep[idx] = {"start": single_dim_slice.start,
                                         "stop": single_dim_slice.stop,
                                         "step": single_dim_slice.step}
        serializable_rep = tuple(serializable_rep)
    else:
        serializable_rep = multi_dim_slice
    
    return serializable_rep



def _de_pre_serialize_multi_dim_slice(serializable_rep):
    if serializable_rep is not None:
        multi_dim_slice = list(serializable_rep)
        for idx, serializable_subitem in enumerate(serializable_rep):
            if isinstance(serializable_subitem, dict):
                multi_dim_slice[idx] = slice(serializable_subitem["start"],
                                             serializable_subitem["stop"],
                                             serializable_subitem["step"])
        multi_dim_slice = tuple(multi_dim_slice)
    else:
        multi_dim_slice = serializable_rep

    return multi_dim_slice



class ID(fancytypes.PreSerializableAndUpdatable):
    r"""A parameter set specifying an HDF5 "datasubset" in an HDF5 file.

    By "datasubset", we mean an array obtained by taking a multidimensional 
    slice of an HDF5 dataset in an HDF5 file.

    Parameters
    ----------
    dataset_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the target HDF5 dataset containing the HDF5
        datasubset of interest.
    multi_dim_slice : `tuple` (`int` | `slice` | `list` (`int`)) | `None`, optional
        The "multidimensional slice object", which specifies the
        multidimensional slice of the target HDF5 dataset that yields the HDF5
        datasubset of interest. We define a multi-dimensional slice object as a
        `tuple` of items which contains at most one item being a `list` of
        integers, and the remaining items being `slice` and/or `int`
        objects. Let ``dataset`` and ``datasubset`` be the target HDF5 dataset
        and datasubset respectively. If ``multi_dim_slice`` is set to `None`,
        then ``datasubset == dataset[()]``. Otherwise, if ``multi_dim_slice`` is
        array-like, then ``multi_dim_slice`` satisfies ``datasubset ==
        dataset[()][multi_dim_slice]``, however the actual implementation of the
        multidimensional slice is more efficient than the above.

    Attributes
    ----------
    core_attrs : `dict`, read-only
        A `dict` representation of the core attributes: each `dict` key is a
        `str` representing the name of a core attribute, and the corresponding
        `dict` value is the object to which said core attribute is set. The core
        attributes are the same as the construction parameters, except that 
        their values might have been updated since construction.

    """
    _validation_and_conversion_funcs = \
        {"dataset_id": h5pywrappers.dataset._check_and_convert_dataset_id,
         "multi_dim_slice": _check_and_convert_multi_dim_slice}

    _pre_serialization_funcs = \
        {"dataset_id": h5pywrappers.dataset._pre_serialize_dataset_id,
         "multi_dim_slice": _pre_serialize_multi_dim_slice}

    _de_pre_serialization_funcs = \
        {"dataset_id": h5pywrappers.dataset._de_pre_serialize_dataset_id,
         "multi_dim_slice": _de_pre_serialize_multi_dim_slice}

    def __init__(self, dataset_id, multi_dim_slice=None):
        ctor_params = {"dataset_id": dataset_id,
                       "multi_dim_slice": multi_dim_slice}
        fancytypes.PreSerializableAndUpdatable.__init__(self, ctor_params)

        return None



def load(datasubset_id):
    r"""Load an HDF5 "datasubset" from an HDF5 file.

    By "datasubset", we mean an array obtained by taking a multidimensional
    slice of an HDF5 dataset in an HDF5 file.

    Parameters
    ----------
    datasubset_id : :class:`h5pywrappers.datasubset.ID`
        The parameter set specifying the HDF5 datasubset of interest.

    Returns
    -------
    datasubset : `array_like`
        The HDF5 datasubset of interest.

    """
    accepted_types = (ID,)
    kwargs = {"obj": datasubset_id,
              "obj_name": "datasubset_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    _, multi_dim_slice_2, multi_dim_slice_3 = \
        _multi_dim_slice_triplet(datasubset_id, datasubset=None)

    dataset_id = datasubset_id.core_attrs["dataset_id"]
    multi_dim_slice = datasubset_id.core_attrs["multi_dim_slice"]
    
    dataset = h5pywrappers.dataset.load(dataset_id, read_only=True)
    datasubset = dataset[multi_dim_slice_2][multi_dim_slice_3]
    dataset.file.close()

    return datasubset



def _multi_dim_slice_triplet(datasubset_id, datasubset):
    dataset_id = datasubset_id.core_attrs["dataset_id"]
    dataset = h5pywrappers.dataset.load(dataset_id, read_only=True)
    dataset_shape = dataset.shape
    dataset_rank = len(dataset_shape)
    dataset.file.close()

    multi_dim_slice = datasubset_id.core_attrs["multi_dim_slice"]
    if multi_dim_slice is None:
        multi_dim_slice = tuple(slice(None) for _ in range(dataset_rank))

    if len(multi_dim_slice) != dataset_rank:
        path_in_file = dataset_id.core_attrs["path_in_file"]
        filename = dataset_id.core_attrs["filename"]
        err_msg = _multi_dim_slice_triplet_err_msg_1.format(path_in_file,
                                                            filename)
        raise IndexError(err_msg)

    multi_dim_slice_1 = multi_dim_slice
    multi_dim_slice_2 = []
    multi_dim_slice_3 = []

    if datasubset is not None:
        datasubset_shape = []

    for axis in range(dataset_rank):
        single_dim_slice_1 = multi_dim_slice_1[axis]
        max_allowed_idx = dataset_shape[axis]-1

        single_dim_slice_1, single_dim_slice_2, single_dim_slice_3 = \
            _check_and_convert_single_dim_slice(single_dim_slice_1,
                                                max_allowed_idx,
                                                axis,
                                                dataset_id)
                            
        multi_dim_slice_2.append(single_dim_slice_2)
        if single_dim_slice_3 is not None:
            multi_dim_slice_3.append(single_dim_slice_3)
            if datasubset is not None:
                datasubset_dim = \
                    len(np.arange(dataset_shape[axis])[single_dim_slice_2])
                datasubset_shape.append(datasubset_dim)
                
    if datasubset is not None:
        if datasubset_shape != list(datasubset.shape):
            raise ValueError(_check_and_convert_multi_dim_slice_err_msg_2)

    multi_dim_slice_1 = tuple(multi_dim_slice_1)
    multi_dim_slice_2 = tuple(multi_dim_slice_2)
    multi_dim_slice_3 = tuple(multi_dim_slice_3)

    return (multi_dim_slice_1, multi_dim_slice_2, multi_dim_slice_3)



def _check_and_convert_single_dim_slice(single_dim_slice,
                                        max_allowed_idx,
                                        axis,
                                        dataset_id):
    single_dim_slice_1 = single_dim_slice

    if isinstance(single_dim_slice_1, list):
        temp = []
        for idx in single_dim_slice_1:
            idx = _check_and_shift_idx(idx, max_allowed_idx, axis, dataset_id)
            temp.append(idx)
            
        if len(temp) != len(set(temp)):
            err_msg = _check_and_convert_single_dim_slice_err_msg_1.format(axis)
            raise ValueError(err_msg)
        
        single_dim_slice_2 = list(np.sort(temp))
        sort_order = np.argsort(temp)
        single_dim_slice_3 = [0]*len(temp)
        for idx in range(len(temp)):
            single_dim_slice_3[sort_order[idx]] = idx
        
    elif isinstance(single_dim_slice_1, int):
        single_dim_slice_2 = \
            _check_and_shift_idx(single_dim_slice_1,
                                 max_allowed_idx,
                                 axis,
                                 dataset_id)
        single_dim_slice_3 = None

    else:  # If a `slice` object.
        single_dim_slice_2_step = np.abs(single_dim_slice_1.step or 1)
        single_dim_slice_3_step = np.sign(single_dim_slice_1.step or 1)
        if single_dim_slice_3_step > 0:
            single_dim_slice_2 = slice(single_dim_slice_1.start,
                                       single_dim_slice_1.stop,
                                       single_dim_slice_2_step)
        else:
            temp_1 = (min(single_dim_slice_1.start, max_allowed_idx)
                      if single_dim_slice_1.start is not None
                      else max_allowed_idx)
            if temp_1 < 0:
                temp_1 = max((max_allowed_idx+1)+temp_1, 0)

            temp_2 = (min(single_dim_slice_1.stop, max_allowed_idx)
                      if single_dim_slice_1.stop is not None
                      else -1)
            if (temp_2 < 0) and (single_dim_slice_1.stop is not None):
                temp_2 = max((max_allowed_idx+1)+temp_2, -1)

            temp_3 = single_dim_slice_2_step
            temp_4 = (temp_1 - temp_2 - 1) // temp_3

            single_dim_slice_2_start = temp_1 - temp_3*temp_4
            single_dim_slice_2_stop = temp_1 + 1
            
            single_dim_slice_2 = slice(single_dim_slice_2_start,
                                       single_dim_slice_2_stop,
                                       single_dim_slice_2_step)
        
        single_dim_slice_3 = slice(None, None, single_dim_slice_3_step)

    return single_dim_slice_1, single_dim_slice_2, single_dim_slice_3



def _check_and_shift_idx(idx, max_allowed_idx, axis, dataset_id):
    idx = (max_allowed_idx+1)+idx if idx < 0 else idx

    if (idx < 0) or (idx > max_allowed_idx):
        path_in_file = dataset_id.core_attrs["path_in_file"]
        filename = dataset_id.core_attrs["filename"]
        err_msg = _check_and_shift_idx_err_msg_1.format(axis,
                                                        path_in_file,
                                                        filename)
        raise ValueError(err_msg)

    return idx



def save(datasubset, datasubset_id):
    r"""Save an HDF5 attribute to an HDF5 file.

    By "datasubset", we mean an array obtained by taking a multidimensional
    slice of an HDF5 dataset in an HDF5 file.

    Note that if the HDF5 datasubset to be saved is of a different data type
    than the aforementioned HDF5 dataset, then the current Python function will
    try to convert a copy of the former to the same data type as the latter.

    Parameters
    ----------
    datasubset : `any_type`
        The HDF5 datasubset of interest to save to an HDF5 file.
    datasubset_id : :class:`h5pywrappers.datasubset.ID`
        The parameter set specifying where to save the HDF5 datasubset of
        interest.

    Returns
    -------

    """
    accepted_types = (ID,)
    kwargs = {"obj": datasubset_id,
              "obj_name": "datasubset_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    datasubset = czekitout.convert.to_numpy_array(obj=datasubset,
                                                  obj_name="datasubset")
    
    _, multi_dim_slice_2, multi_dim_slice_3 = \
        _multi_dim_slice_triplet(datasubset_id, datasubset)

    dataset_id = datasubset_id.core_attrs["dataset_id"]
    dataset = h5pywrappers.dataset.load(dataset_id, read_only=False)
    
    try:
        dataset[multi_dim_slice_2] = datasubset[multi_dim_slice_3]
    except:
        dataset.file.close()
        err_msg = _save_err_msg_1.format(path_in_file, filename)
        raise IOError(_save_err_msg_1)

    dataset.file.close()

    return None



###########################
## Define error messages ##
###########################

_multi_dim_slice_triplet_err_msg_1 = \
    ("The 'multidimensional slice object', specified by the object "
     "``datasubset_id``, must be a sequence of length equal to the rank of the "
     "HDF5 dataset at the HDF5 path ``'{}'`` of the HDF5 file at the file path "
     "``'{}'``.")

_check_and_convert_multi_dim_slice_err_msg_2 = \
    ("The 'multidimensional slice object', specified by the object "
     "``datasubset_id``, implies an HDF5 datasubset with dimensions that are "
     "incompatible with those of the HDF5 datasubset ``datasubset``.")

_check_and_convert_single_dim_slice_err_msg_1 = \
    ("The slice for the dataset axis #{}, specified by the object "
     "``datasubset_id``, is of incorrect format: the slice contains repeating "
     "indices after converting any negative indices to their functionally "
     "equivalent positive values.")

_check_and_shift_idx_err_msg_1 = \
    ("The slice for the dataset axis #{}, specified by the object "
     "``datasubset_id``, is of incorrect format: the slice contains at least "
     "one index that is out of the bounds of the HDF5 dataset at the HDF5 path "
     "``'{}'`` of the HDF5 file at the file path ``'{}'``.")

_save_err_msg_1 = \
    ("An error occurred in trying to save the HDF5 datasubset ``datasubset`` "
     "to the HDF5 dataset at the HDF5 path ``'{}'`` of the HDF5 file at the "
     "file path ``'{}'``. Perhaps the HDF5 datasubet and dataset are of "
     "imcompatible data types. See the remaining traceback for details.")
