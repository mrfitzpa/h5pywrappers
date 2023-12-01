r"""For identifying and loading HDF5 objects.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For checking whether a file exists at a given path, making directories, and
# for removing files.
import pathlib

# For removing directories.
import shutil



# For loading HDF5 files.
import h5py

# For validating and converting objects.
import czekitout.check
import czekitout.convert

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



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
           "load"]



def _check_and_convert_filename(ctor_params):
    filename = ctor_params["filename"]
    filename = czekitout.convert.to_str_from_path_like(filename, "filename")

    return filename



def _check_and_convert_path_in_file(ctor_params):
    path_in_file = ctor_params["path_in_file"]
    path_in_file = czekitout.convert.to_str_from_path_like(path_in_file,
                                                           "path_in_file")

    return path_in_file



def _pre_serialize_filename(filename):
    serializable_rep = filename
    
    return serializable_rep



def _pre_serialize_path_in_file(path_in_file):
    serializable_rep = path_in_file
    
    return serializable_rep



def _de_pre_serialize_filename(serializable_rep):
    filename = serializable_rep

    return filename



def _de_pre_serialize_path_in_file(serializable_rep):
    path_in_file = serializable_rep

    return path_in_file



class ID(fancytypes.PreSerializableAndUpdatable):
    r"""A parameter set specifying an HDF5 object in an HDF5 file or an HDF5 
    file to be.

    Parameters
    ----------
    filename : `str`
        The relative or absolute filename of the HDF5 file that contains the
        HDF5 object of interest.
    path_in_file : `str`
        The HDF5 path to the HDF5 object of interest contained in the HDF5 file
        specified by ``filename``.

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
        {"filename": _check_and_convert_filename,
         "path_in_file": _check_and_convert_path_in_file}

    _pre_serialization_funcs = \
        {"filename": _pre_serialize_filename,
         "path_in_file": _pre_serialize_path_in_file}

    _de_pre_serialization_funcs = \
        {"filename": _de_pre_serialize_filename,
         "path_in_file": _de_pre_serialize_path_in_file}

    def __init__(self, filename, path_in_file):
        ctor_params = {"filename": filename, "path_in_file": path_in_file}
        fancytypes.PreSerializableAndUpdatable.__init__(self, ctor_params)

        return None



def _check_and_convert_obj_id(ctor_params):
    obj_id = ctor_params["obj_id"]
    
    accepted_types = (ID,)
    kwargs = {"obj": obj_id,
              "obj_name": "obj_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    return obj_id



def _pre_serialize_obj_id(obj_id):
    serializable_rep = obj_id.pre_serialize()
    
    return serializable_rep



def _de_pre_serialize_obj_id(serializable_rep):
    obj_id = ID.de_pre_serialize(serializable_rep)

    return obj_id



def load(obj_id, read_only=True):
    r"""Load an HDF5 object from an HDF5 file.

    Note that users can access the HDF5 file object to which the HDF5 object of
    interest belongs via ``obj.file``, where ``obj`` is the HDF5 object of
    interest. To close the HDF5 file, users can run the command
    ``obj.file.close()``, however by doing so, any other HDF5 objects belonging
    to that file will become unusable.

    Parameters
    ----------
    obj_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the HDF5 object of interest.
    read_only : `bool`, optional
        If ``read_only`` is set to ``True``, then the HDF5 object of interest
        cannot be modified after loading it. Otherwise, if ``read_only`` is set
        to ``False``, then the HDF5 object of interest can be modified after
        loading it.

    Returns
    -------
    obj : :class:`h5py.Group` | :class:`h5py.Dataset`
        The HDF5 object of interest.

    """
    read_only = _pre_load(obj_id, read_only)

    filename = obj_id.core_attrs["filename"]
    path_in_file = obj_id.core_attrs["path_in_file"]

    if read_only:
        file_obj = h5py.File(filename, "r")
    else:
        file_obj = h5py.File(filename, "a")
    obj = file_obj[path_in_file]

    return obj



def _pre_load(obj_id, read_only):
    accepted_types = (ID,)
    kwargs = {"obj": obj_id,
              "obj_name": "obj_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    czekitout.convert.to_bool(obj=read_only, obj_name="read_only")

    filename = obj_id.core_attrs["filename"]

    try:
        if not pathlib.Path(filename).is_file():
            raise FileNotFoundError
    except FileNotFoundError:
        err_msg = _pre_load_err_msg_1.format(filename)
        raise FileNotFoundError(err_msg)
    except PermissionError:
        err_msg = _pre_load_err_msg_2.format(filename)
        raise PermissionError(err_msg)
    except BaseException as err:
        raise err

    file_mode = "r" if read_only else "a"

    try:
        with h5py.File(filename, file_mode) as file_obj:
            pass
    except OSError as err:
        if "file is already open for read-only" not in str(err):
            err_msg = _pre_load_err_msg_3.format(filename)
        else:
            err_msg = _pre_load_err_msg_4.format(filename)
        raise OSError(err_msg)
    except BaseException as err:
        raise err

    with h5py.File(filename, file_mode) as file_obj:
        path_in_file = obj_id.core_attrs["path_in_file"]
        if path_in_file not in file_obj:
            err_msg = _pre_load_err_msg_5.format(path_in_file, filename)
            raise ValueError(err_msg)

    return read_only



def _pre_save(obj_id):
    accepted_types = (ID,)
    kwargs = {"obj": obj_id,
              "obj_name": "obj_id",
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    filename = obj_id.core_attrs["filename"]
    temp_dir_path, rm_temp_dir = _mk_parent_dir(filename)

    try:
        if not pathlib.Path(filename).is_file():
            try:
                with h5py.File(filename, "w") as file_obj:
                    pass
            except PermissionError:
                err_msg = _pre_save_err_msg_1.format(filename)
                raise PermissionError(err_msg)
            except BaseException as err:
                raise err
        
            pathlib.Path(filename).unlink()
        else:
            try:
                with h5py.File(filename, "a") as file_obj:
                    pass
            except PermissionError:
                err_msg = _pre_save_err_msg_2.format(filename)
                raise PermissionError(err_msg)
            except OSError:
                err_msg = _pre_save_err_msg_3.format(filename)
                raise OSError(err_msg)
            except BaseException as err:
                raise err
    except BaseException as err:
        if rm_temp_dir:
            shutil.rmtree(temp_dir_path)
        raise err

    if rm_temp_dir:
        shutil.rmtree(temp_dir_path)

    return None



def _mk_parent_dir(filename):
    try:
        parent_dir_path = pathlib.Path(filename).resolve().parent
        temp_dir_path = pathlib.Path(parent_dir_path.root)
        rm_temp_dir = False

        for path_part in parent_dir_path.parts[1:]:
            temp_dir_path = pathlib.Path.joinpath(temp_dir_path, path_part)
            if not temp_dir_path.is_dir():
                rm_temp_dir = True
                break

        pathlib.Path(parent_dir_path).mkdir(parents=True, exist_ok=True)
    except PermissionError:
        err_msg = _mk_parent_dir_err_msg_1.format(filename)
        raise PermissionError(err_msg)
    except BaseException as err:
        raise err

    return temp_dir_path, rm_temp_dir



###########################
## Define error messages ##
###########################

_pre_load_err_msg_1 = \
    ("No file exists at the file path ``'{}'``.")
_pre_load_err_msg_2 = \
    ("Cannot access the file path ``'{}'`` because of insufficient "
     "permissions.")
_pre_load_err_msg_3 = \
    ("No HDF5 file exists at the file path ``'{}'``.")
_pre_load_err_msg_4 = \
    ("Unable to synchronously open the HDF5 file at the file path ``'{}'``: "
     "the file is already open in read-only mode.")
_pre_load_err_msg_5 = \
    ("No HDF5 object was found at the HDF5 path ``'{}'`` of the HDF5 file "
     "at the file path ``'{}'``.")

_pre_save_err_msg_1 = \
    _pre_load_err_msg_2
_pre_save_err_msg_2 = \
    ("Cannot write to the file at the file path ``'{}'`` because of "
     "insufficient permissions.")
_pre_save_err_msg_3 = \
    _pre_load_err_msg_3

_mk_parent_dir_err_msg_1 = \
    _pre_load_err_msg_2
