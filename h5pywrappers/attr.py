r"""For loading and saving HDF5 object attributes.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For saving HDF5 attributes.
import h5py

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



# For identifying HDF5 objects.
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
__all__ = ["ID",
           "load",
           "save"]



def _check_and_convert_attr_name(ctor_params):
    attr_name = ctor_params["attr_name"]
    attr_name = czekitout.convert.to_str_from_path_like(attr_name, "attr_name")

    return attr_name



def _pre_serialize_attr_name(attr_name):
    serializable_rep = attr_name
    
    return serializable_rep



def _de_pre_serialize_attr_name(serializable_rep):
    attr_name = serializable_rep

    return attr_name



class ID(fancytypes.PreSerializableAndUpdatable):
    r"""A parameter set specifying an HDF5 attribute of an HDF5 object in an
    HDF5 file or an HDF5 file to be.

    Parameters
    ----------
    obj_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the HDF5 object from which to load the
        HDF5 attribute of interest.
    attr_name : `str`
        The name of the HDF5 attribute of interest.

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
        {"obj_id": h5pywrappers.obj._check_and_convert_obj_id,
         "attr_name": _check_and_convert_attr_name}

    _pre_serialization_funcs = \
        {"obj_id": h5pywrappers.obj._pre_serialize_obj_id,
         "attr_name": _pre_serialize_attr_name}

    _de_pre_serialization_funcs = \
        {"obj_id": h5pywrappers.obj._de_pre_serialize_obj_id,
         "attr_name": _de_pre_serialize_attr_name}

    def __init__(self, obj_id, attr_name):
        ctor_params = {"obj_id": obj_id, "attr_name": attr_name}
        fancytypes.PreSerializableAndUpdatable.__init__(self, ctor_params)

        return None



def load(attr_id):
    r"""Load an HDF5 attribute from an HDF5 file.

    Parameters
    ----------
    attr_id : :class:`h5pywrappers.attr.ID`
        The parameter set specifying the HDF5 attribute of interest.

    Returns
    -------
    attr : `any_type`
        The HDF5 attribute of interest.

    """
    accepted_types = (ID,)
    kwargs = {"obj": attr_id,
              "obj_name": "attr_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    obj_id = attr_id.core_attrs["obj_id"]
    obj = h5pywrappers.obj.load(obj_id, read_only=True)
    attr_name = attr_id.core_attrs["attr_name"]

    try:
        attr = obj.attrs[attr_name]
        obj.file.close()
    except:
        obj.file.close()
        filename = obj_id.core_attrs["filename"]
        path_in_file = obj_id.core_attrs["path_in_file"]
        err_msg = _load_err_msg_1.format(path_in_file, filename, attr_name)
        raise ValueError(err_msg)

    return attr



def save(attr, attr_id, write_mode="a-"):
    r"""Save an HDF5 attribute to an HDF5 file.

    Parameters
    ----------
    attr_val : `any_type`
        The HDF5 attribute of interest to save to an HDF5 file.
    attr_id : :class:`h5pywrappers.attr.ID`
        The parameter set specifying where to save the HDF5 attribute of 
        interest.
    write_mode : "a" | "a-", optional
        The write mode upon opening the HDF5 file to which to save the HDF5
        attribute of interest: if ``write_mode`` is set to ``"a-"``, then the
        HDF5 attribute of interest is saved without emptying the target HDF5
        file unless an HDF5 attribute with the same name as the target attribute
        name already exists at the target HDF5 path of the target HDF5 file, in
        which case an error is raised and the target HDF5 file is left
        unmodified; else if ``write_mode`` is set to ``"a"``, then the HDF5
        attribute of interest is saved without emptying the target HDF5 file,
        replacing any HDF5 object at the target HDF5 path should one exist prior
        to saving.

    Returns
    -------

    """
    accepted_values = ("a", "a-")
    if write_mode not in accepted_values:
        raise ValueError(_save_err_msg_1)

    obj_id = attr_id.core_attrs["obj_id"]
    h5pywrappers.obj._pre_save(obj_id)
    obj = h5pywrappers.obj.load(obj_id, read_only=False)

    attr_name = attr_id.core_attrs["attr_name"]
    filename = obj_id.core_attrs["filename"]
    path_in_file = obj_id.core_attrs["path_in_file"]
    if (write_mode == "a-") and (attr_name in obj.attrs):
        obj.file.close()
        err_msg = _save_err_msg_2.format(attr_name, path_in_file, filename)
        raise IOError(err_msg)

    obj.attrs[attr_name] = attr
    obj.file.close()

    return None



###########################
## Define error messages ##
###########################

_load_err_msg_1 = \
    ("The HDF5 object located at the HDF5 path ``'{}'`` of the HDF5 file at "
     "the file path ``'{}'`` has no HDF5 attribute named ``'{}'``.")

_save_err_msg_1 = \
    ("The object ``write_mode`` must be one of the following strings: ``'a'`` "
     "or ``'a-'``.")
_save_err_msg_2 = \
    ("Cannot save the HDF5 attribute named ``'{}'`` to an object at the HDF5 "
     "path ``'{}'`` of the HDF5 file at the file path ``'{}'`` because an HDF5 "
     "attribute of the same name already exists there and the parameter "
     "``write_mode`` was set to ``'a-'``, which prohibits replacing any such "
     "pre-existing HDF5 attribute.")
