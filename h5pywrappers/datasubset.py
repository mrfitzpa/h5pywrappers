r"""For loading and saving HDF5 "datasubsets".

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For updating HDF5 datasets.
import h5py

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For identifying HDF5 objects.
import h5pywrappers.obj

# For loading and saving HDF5 datasets.
import h5pywrappers.dataset



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
            if isinstance(datasubset, dict):
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
        {"dataset_id": _check_and_convert_obj_id,
         "multi_dim_slice": _check_and_convert_multi_dim_slice}

    _pre_serialization_funcs = \
        {"dataset_id": _pre_serialize_obj_id,
         "multi_dim_slice": _pre_serialize_multi_dim_slice}

    _de_pre_serialization_funcs = \
        {"dataset_id": _de_pre_serialize_obj_id,
         "multi_dim_slice": _de_pre_serialize_multi_dim_slice}

    def __init__(self, dataset_id, multi_dim_slice=None):
        ctor_params = {"dataset_id": dataset_id,
                       "multi_dim_slice": multi_dim_slice}
        fancytypes.PreSerializableAndUpdatable.__init__(self, ctor_params)

        return None



def load(attr_id):
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
        _multi_dim_slice_triplet(datasubset_id)

    dataset_id = datasubset_id.core_attrs["dataset_id"]
    multi_dim_slice = datasubset_id.core_attrs["multi_dim_slice"]
    
    dataset = h5pywrappers.dataset.load(dataset_id)
    datasubset = dataset[multi_dim_slice_2][multi_dim_slice_3]

    return datasubset



def save(datasubset, datasubset_id):
    r"""Save an HDF5 attribute to an HDF5 file.

    By "datasubset", we mean an array obtained by taking a multidimensional
    slice of an HDF5 dataset in an HDF5 file.

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

    _, multi_dim_slice_2, multi_dim_slice_3 = \
        _multi_dim_slice_triplet(datasubset_id)

    dataset_id = datasubset_id.core_attrs["dataset_id"]
    datasubset = _check_datasubset(datasubset, multi_dim_slice_2, dataset_id)

    obj_id = dataset_id.core_attrs["obj_id"]
    h5pywrappers.obj._pre_save(obj_id)

    filename = obj_id.core_attrs["filename"]
    with h5py.File(filename, "a") as file_obj:
        path_in_file = obj_id.core_attrs["path_in_file"]
        dataset = file_obj[path_in_file]
        dataset[multi_dim_slice_2] = datasubset[multi_dim_slice_3]

    return None



def _check_datasubset(datasubset, multi_dim_slice_2, dataset_id):
    datasubset = czekitout.convert.to_numpy_array(obj=datasubset,
                                                  obj_name="datasubset")

    return datasubset



###########################
## Define error messages ##
###########################

