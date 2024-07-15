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
r"""For identifying and loading HDF5 objects.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For performing deep copies.
import copy

# For accessing attributes of functions.
import inspect

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



# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import h5pywrappers._fancytypes



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = ["ID",
           "load"]



def _check_and_convert_filename(params):
    obj_name = "filename"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    filename = czekitout.convert.to_str_from_str_like(**kwargs)

    return filename



def _pre_serialize_filename(filename):
    serializable_rep = filename
    
    return serializable_rep



def _de_pre_serialize_filename(serializable_rep):
    filename = serializable_rep

    return filename



def _check_and_convert_path_in_file(params):
    obj_name = "path_in_file"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    path_in_file = czekitout.convert.to_str_from_str_like(**kwargs)

    return path_in_file



def _pre_serialize_path_in_file(path_in_file):
    serializable_rep = path_in_file
    
    return serializable_rep



def _de_pre_serialize_path_in_file(serializable_rep):
    path_in_file = serializable_rep

    return path_in_file



_module_alias = \
    h5pywrappers._fancytypes
_default_filename = \
    "data_file.h5"
_default_path_in_file = \
    "/data"
_default_skip_validation_and_conversion = \
    _module_alias.default_skip_validation_and_conversion



cls_alias = h5pywrappers._fancytypes.PreSerializableAndUpdatable
class ID(cls_alias):
    r"""A parameter set specifying an HDF5 object in an HDF5 file or an HDF5 
    file to be.

    Parameters
    ----------
    filename : `str`, optional
        The relative or absolute filename of the HDF5 file that contains the
        HDF5 object of interest.
    path_in_file : `str`, optional
        The HDF5 path to the HDF5 object of interest contained in the HDF5 file
        specified by ``filename``.
    skip_validation_and_conversion : `bool`, optional
        Let ``params_to_be_mapped_to_core_attrs`` be a `dict` object containing
        only the construction parameters described above, i.e. excluding the
        parameter ``skip_validation_and_conversion``, such that
        ``h5pywrappers.obj.ID(**params_to_be_mapped_to_core_attrs)`` would be a
        valid call to the constructor of the class :class:`h5pywrappers.obj.ID`.

        Let ``core_attrs`` denote the attribute
        :attr:`h5pywrappers.obj.ID.core_attrs`, which is a `dict` object.

        Let ``validation_and_conversion_funcs`` denote the attribute
        :attr:`h5pywrappers.obj.ID.validation_and_conversion_funcs`, which is a
        `dict` object.

        If ``skip_validation_and_conversion`` is set to ``False``, then for each
        key ``key`` in ``params_to_be_mapped_to_core_attrs``,
        ``core_attrs[key]`` is set to ``validation_and_conversion_funcs[key]
        (params_to_be_mapped_to_core_attrs)``.

        Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
        then ``core_attrs`` is set to
        ``params_to_be_mapped_to_core_attrs``. This option is desired primarily
        when the user wants to avoid potentially expensive copies and/or
        conversions of the `dict` values of
        ``params_to_be_mapped_to_core_attrs``, as it is guaranteed that no
        copies or conversions are made in this case.

    Attributes
    ----------
    validation_and_conversion_funcs : `dict`, read-only
        A `dict` object of callable objects.
    pre_serialization_funcs : `dict`, read-only
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``core_attrs_candidate_1`` be any `dict` object that has the same
        keys as ``validation_and_conversion_funcs``, where for each `dict` key
        ``key`` in ``core_attrs_candidate_1``,
        ``validation_and_conversion_funcs[key](core_attrs_candidate_1)`` does
        not raise an exception.

        For each `dict` key ``key`` in ``core_attrs_candidate_1``,
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])`` yields a
        serializable object, i.e. it yields an object that can be passed into
        the function ``json.dumps`` without raising an exception.
    de_pre_serialization_funcs : `dict`, read-only
        A `dict` object of callable objects that has the same keys as
        ``validation_and_conversion_funcs``. 

        Let ``core_attrs_candidate_1`` be as defined in the above description of
        ``pre_serialization_funcs``.

        Let ``serializable_rep`` be a `dict` object that has the same keys as
        ``core_attrs_candidate_1``, where for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``, ``serializable_rep[key]`` is set to
        ``pre_serialization_funcs[key](core_attrs_candidate_1[key])``.

        The items of ``de_pre_serialization_funcs`` are set to callable objects
        that lead to ``de_pre_serialization_funcs[key](serializable_rep[key])``
        not raising an exception for each `dict` key ``key`` in
        ``serializable_rep``.

        Let ``core_attrs_candidate_2`` be a `dict` object that has the same keys
        as ``serializable_rep``, where for each `dict` key ``key`` in
        ``validation_and_conversion_funcs``, ``core_attrs_candidate_2[key]`` is
        set to ``de_pre_serialization_funcs[key](serializable_rep[key])``.

        The items of ``de_pre_serialization_funcs`` are set to callable objects
        that lead to
        ``validation_and_conversion_funcs[key](core_attrs_candidate_2)`` not
        raising an exception for each `dict` key ``key`` in
        ``core_attrs_candidate_2``.
    core_attrs : `dict`, read-only
        The "core attributes", represented as a `dict` object. ``core_attrs`` is
        expected to satisfy ``core_attrs[key] ==
        validation_and_conversion_funcs[key](core_attrs)`` for each `dict` key
        ``key`` in ``validation_and_conversion_funcs``.

    """
    _validation_and_conversion_funcs_ = \
        {"filename": _check_and_convert_filename,
         "path_in_file": _check_and_convert_path_in_file}

    _pre_serialization_funcs_ = \
        {"filename": _pre_serialize_filename,
         "path_in_file": _pre_serialize_path_in_file}

    _de_pre_serialization_funcs_ = \
        {"filename": _de_pre_serialize_filename,
         "path_in_file": _de_pre_serialize_path_in_file}

    def __init__(self,
                 filename=\
                 _default_filename,
                 path_in_file=\
                 _default_path_in_file,
                 skip_validation_and_conversion=\
                 _default_skip_validation_and_conversion):
        ctor_params = {key: val
                       for key, val in locals().items()
                       if (key not in ("self", "__class__"))}
        params_to_be_mapped_to_core_attrs = ctor_params.copy()
        del params_to_be_mapped_to_core_attrs["skip_validation_and_conversion"]

        kwargs = \
            self._return_ctor_param_subset_of_fancytypes_cls()
        kwargs["params_to_be_mapped_to_core_attrs"] = \
            params_to_be_mapped_to_core_attrs
        kwargs["skip_validation_and_conversion"] = \
            skip_validation_and_conversion
        _ = \
            fancytypes.PreSerializableAndUpdatable.__init__(self, **kwargs)

        return None



def _check_and_convert_obj_id(params):
    obj_name = "obj_id"
    obj_id = copy.deepcopy(params[obj_name])

    accepted_types = (ID,)
    kwargs = {"obj": obj_id,
              "obj_name": obj_name,
              "accepted_types": accepted_types}
    czekitout.check.if_instance_of_any_accepted_types(**kwargs)

    return obj_id



def _pre_serialize_obj_id(obj_id):
    serializable_rep = obj_id.pre_serialize()
    
    return serializable_rep



def _de_pre_serialize_obj_id(serializable_rep):
    kwargs = {"serializable_rep": serializable_rep,
              "skip_validation_and_conversion": True}
    obj_id = ID.de_pre_serialize(**kwargs)

    return obj_id



def _check_and_convert_read_only(params):
    obj_name = "read_only"
    kwargs = {"obj": params[obj_name], "obj_name": obj_name}
    read_only = czekitout.convert.to_bool(**kwargs)

    return read_only



_default_read_only = read_only



def load(obj_id, read_only=_default_read_only):
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
    params = locals()
    for param_name in params:
        func_name = "_check_and_convert_" + param_name
        func_alias = globals()[func_name]
        params[param_name] = func_alias(params)

    func_name = "_" + inspect.stack()[0][3]
    func_alias = globals()[func_name]
    kwargs = params
    obj = func_alias(**kwargs)

    return obj



def _load(obj_id, read_only):
    read_only = _pre_load(obj_id, read_only)

    obj_id_core_attrs = obj_id.get_core_attrs(deep_copy=False)
    filename = obj_id_core_attrs["filename"]
    path_in_file = obj_id_core_attrs["path_in_file"]

    if read_only:
        file_obj = h5py.File(filename, "r")
    else:
        file_obj = h5py.File(filename, "a")
        
    obj = file_obj[path_in_file]

    return obj



def _pre_load(obj_id, read_only):
    obj_id_core_attrs = obj_id.get_core_attrs(deep_copy=False)
    filename = obj_id_core_attrs["filename"]
    path_in_file = obj_id_core_attrs["path_in_file"]

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
        if "Unable to synchronously open" not in str(err):
            err_msg = _pre_load_err_msg_3.format(filename)
        else:
            err_msg = _pre_load_err_msg_4.format(filename)
        raise OSError(err_msg)
    except BaseException as err:
        raise err

    with h5py.File(filename, file_mode) as file_obj:
        if path_in_file not in file_obj:
            err_msg = _pre_load_err_msg_5.format(path_in_file, filename)
            raise ValueError(err_msg)

    return read_only



def _pre_save(obj_id):
    obj_id_core_attrs = obj_id.get_core_attrs(deep_copy=False)
    filename = obj_id_core_attrs["filename"]

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
            except OSError as err:
                if "Unable to synchronously open" not in str(err):
                    err_msg = _pre_save_err_msg_3.format(filename)
                else:
                    err_msg = _pre_load_err_msg_4.format(filename)
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
     "see traceback for details.")
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
_pre_save_err_msg_4 = \
    _pre_load_err_msg_4

_mk_parent_dir_err_msg_1 = \
    _pre_load_err_msg_2
