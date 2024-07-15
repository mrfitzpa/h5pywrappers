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
r"""Defines subclasses of the classes in the library :mod:`fancytypes`.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For defining classes that support enforced validation, updatability,
# pre-serialization, and de-serialization.
import fancytypes



##################################
## Define classes and functions ##
##################################

# List of public objects in objects.
__all__ = []



default_params_to_be_mapped_to_core_attrs = \
    dict()
default_skip_validation_and_conversion = \
    False
default_serializable_rep = \
    default_params_to_be_mapped_to_core_attrs
default_serialized_rep = \
    str(default_serializable_rep)
default_filename = \
    "serialized_rep_of_fancytype.json"



class PreSerializableAndUpdatable(fancytypes.PreSerializableAndUpdatable):
    @classmethod
    def _return_ctor_param_subset_of_fancytypes_cls(cls):
        ctor_param_subset_of_fancytypes_cls = \
            {"validation_and_conversion_funcs": \
             cls._validation_and_conversion_funcs_, 
             "pre_serialization_funcs": \
             cls._pre_serialization_funcs_,
             "de_pre_serialization_funcs": \
             cls._de_pre_serialization_funcs_}

        return ctor_param_subset_of_fancytypes_cls



    @classmethod
    def de_pre_serialize(cls, 
                         serializable_rep=\
                         default_serializable_rep,
                         skip_validation_and_conversion=\
                         default_skip_validation_and_conversion):
        r"""Construct an instance from a serializable representation.

        We define pre-serialization as the process of converting an object into
        a form that can be subsequently serialized into a JSON format. We refer
        to objects resulting from pre-serialization as serializable objects.

        We define de-pre-serialization as the process of converting a
        serializable object into an instance of the type
        :class:`fancytypes.PreSerializable` or a subclass thereof,
        i.e. de-pre-serialization is the reverse process of pre-serialization.

        Parameters
        ----------
        serializable_rep : `dict`, optional
            A `dict` object that has the same keys as the attribute
            ``validation_and_conversion_funcs``.

            The items of ``serializable_rep`` are expected to be objects that
            would lead to
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` not
            raising an exception for each `dict` key ``key`` in
            ``serializable_rep``, where ``de_pre_serialization`` is an attribute
            of the current class.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``serializable_rep``, where for each `dict` key ``key`` in
            ``serializable_rep``, ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            The items of ``serializable_rep`` are also expected to be set to
            objects that would lead to
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` not
            raising an exception for each `dict` key ``key`` in
            ``serializable_rep``.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``serializable_rep``, ``core_attrs[key]`` is set
            to ``validation_and_conversion_funcs[key] (core_attrs_candidate)``,
            with ``core_attrs_candidate_`` being defined in the above
            description of ``serializable_rep``, and ``core_attrs`` and
            ``validation_and_conversion_funcs`` being attributes of the
            current class.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        instance_of_current_cls : Current class
            An instance constructed from the serializable representation
            ``serializable_rep``.

        """
        kwargs = \
            {"name_of_parameter_of_given_method": "serializable_rep",
             "parameter_of_given_method": serializable_rep,
             "given_method_name": "de_pre_serialize",
             "skip_validation_and_conversion": skip_validation_and_conversion}
        instance_of_current_cls = \
            cls._construct_instance_via_given_method(**kwargs)

        return instance_of_current_cls


    
    @classmethod
    def _construct_instance_via_given_method(cls, 
                                             name_of_parameter_of_given_method, 
                                             parameter_of_given_method, 
                                             given_method_name, 
                                             skip_validation_and_conversion):
        kwargs = \
            cls._return_ctor_param_subset_of_fancytypes_cls()
        kwargs[name_of_parameter_of_given_method] = \
            parameter_of_given_method
        kwargs["skip_validation_and_conversion"] = \
            skip_validation_and_conversion

        method_alias = getattr(fancytypes.PreSerializableAndUpdatable, 
                               given_method_name)
        instance_of_fancytypes_cls = method_alias(**kwargs)

        method_alias = instance_of_fancytypes_cls.get_core_attrs
        core_attrs = method_alias(deep_copy=False)
        kwargs = {**core_attrs, "skip_validation_and_conversion": True}
        instance_of_current_cls = cls(**kwargs)

        return instance_of_current_cls



    @classmethod
    def loads(cls,
              serialized_rep=\
              default_serialized_rep,
              skip_validation_and_conversion=\
              default_skip_validation_and_conversion):
        r"""Construct an instance from a serialized representation.

        Parameters
        ----------
        serialized_rep : `str` | `bytes` | `bytearray`, optional
            The serialized representation.

            ``serialized_rep`` is expected to be such that
            ``json.loads(serialized_rep)`` does not raise an exception.

            Let ``serializable_rep=json.loads(serialized_rep)``. 

            ``serialized_rep`` is also expected to be such that
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` does not
            raise an exception for each `dict` key ``key`` in
            ``de_pre_serialization``, where ``de_pre_serialization`` is an
            attribute of the current class.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``serializable_rep``, where for each `dict` key ``key`` in
            ``serializable_rep``, ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            ``serialized_rep`` is also expected to be such that
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` does
            not raise an exception for each `dict` key ``key`` in
            ``serializable_rep``, where ``validation_and_conversion_funcs`` is
            an attribute of the current class.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``core_attrs_candidate``, ``core_attrs[key]`` is
            set to ``validation_and_conversion_funcs[key]
            (core_attrs_candidate)``, with ``core_attrs_candidate_`` being
            defined in the above description of ``serializable_rep``, and
            ``core_attrs`` and ``validation_and_conversion_funcs`` being
            attributes of the current class.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        instance_of_current_cls : Current class
            An instance constructed from the serialized representation.

        """
        kwargs = \
            {"name_of_parameter_of_given_method": "serialized_rep",
             "parameter_of_given_method": serialized_rep,
             "given_method_name": "loads",
             "skip_validation_and_conversion": skip_validation_and_conversion}
        instance_of_current_cls = \
            cls._construct_instance_via_given_method(**kwargs)

        return instance_of_current_cls



    @classmethod
    def load(cls,
             filename=\
             default_filename,
             skip_validation_and_conversion=\
              default_skip_validation_and_conversion):
        r"""Construct an instance from a serialized representation that is 
        stored in a JSON file.

        Parameters
        ----------
        filename : `str`, optional
            The relative or absolute path to the JSON file that is storing the
            serialized representation of an instance.

            ``filename`` is expected to be such that ``json.load(open(filename,
            "r"))`` does not raise an exception.

            Let ``serializable_rep=json.load(open(filename, "r"))``.

            ``filename`` is also expected to be such that
            ``de_pre_serialization_funcs[key](serializable_rep[key])`` does not
            raise an exception for each `dict` key ``key`` in
            ``de_pre_serialization``, where ``de_pre_serialization`` is an
            attribute of the current class.

            Let ``core_attrs_candidate`` be a `dict` object that has the same
            keys as ``serializable_rep``, where for each `dict` key ``key`` in
            ``serializable_rep``, ``core_attrs_candidate[key]`` is set to
            de_pre_serialization_funcs[key](serializable_rep[key])``.

            ``filename`` is also expected to be such that
            ``validation_and_conversion_funcs[key](core_attrs_candidate)`` does
            not raise an exception for each `dict` key ``key`` in
            ``serializable_rep``, where ``validation_and_conversion_funcs`` is
            an attribute of the current class.
        skip_validation_and_conversion : `bool`, optional
            If ``skip_validation_and_conversion`` is set to ``False``, then for
            each key ``key`` in ``core_attrs_candidate``, ``core_attrs[key]`` is
            set to ``validation_and_conversion_funcs[key]
            (core_attrs_candidate)``, with ``core_attrs_candidate_`` being
            defined in the above description of ``serializable_rep``, and
            ``core_attrs`` and ``validation_and_conversion_funcs`` being
            attributes of the current class.

            Otherwise, if ``skip_validation_and_conversion`` is set to ``True``,
            then ``core_attrs`` is set to ``core_attrs_candidate``. This option
            is desired primarily when the user wants to avoid potentially
            expensive copies and/or conversions of the `dict` values of
            ``core_attrs_candidate``, as it is guaranteed that no copies or
            conversions are made in this case.

        Returns
        -------
        instance_of_current_cls : Current class
            An instance constructed from the serialized representation
            stored in the JSON file.

        """
        kwargs = \
            {"name_of_parameter_of_given_method": "filename",
             "parameter_of_given_method": filename,
             "given_method_name": "load",
             "skip_validation_and_conversion": skip_validation_and_conversion}
        instance_of_current_cls = \
            cls._construct_instance_via_given_method(**kwargs)

        return instance_of_current_cls



###########################
## Define error messages ##
###########################
