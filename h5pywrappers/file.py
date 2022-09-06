r"""For generating test HDF5 files.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For generating random numpy arrays.
import numpy as np

# For converting objects.
import czekitout.convert



# For saving HDF5 datasets, scalars, and JSON documents.
import h5pywrappers.obj
import h5pywrappers.dataset
import h5pywrappers.scalar
import h5pywrappers.json.document



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
__all__ = ["generator_1",
           "generator_2"]



def generator_1(filename="foo.h5", overwrite=False):
    r"""Generate an HDF5 with a particular file structure and partially random 
    data for demonstration purposes.

    This Python function generates an HDF5 file with the following file
    structure:

    - group-1-A: <HDF5 group>
    
      * scalar-1-A: <HDF5 scalar>

        + units: <HDF5 attribute>

      * dataset-1-A: <HDF5 dataset>        

        + was_randomly_generated: <HDF5 attribute>

    - group-1-B: <HDF5 group>
      
      * numerical_id: <HDF5 attribute>

      * json-document-1-B: <HDF5 JSON document>

    See the documentation for the function :class:`h5pywrappers.scalar.load` for
    the definition of an HDF5 scalar adopted in the ``h5pywrappers`` library;
    and see the documentation for the function
    :class:`h5pywrappers.json.document.load` for the definition of a JSON
    document adopted in the ``h5pywrappers`` library.

    Given an HDF5 file object ``file_obj`` that has read access to an HDF5 with
    the above file structure, one could access e.g. the HDF5 group containing
    the HDF5 dataset by ``file_obj["group-1-A"]``, the HDF5 dataset by
    ``file_obj["group 1.A/dataset-1-A"]``, or the HDF5 attribute of the HDF5
    dataset by
    ``file_obj["group-1-A/dataset-1-A"].attrs["was_randomly_generated]``.

    Parameters
    ----------
    filename : `str`, optional
        The relative or absolute filename of the HDF5 file to be generated.
    overwrite : `bool`, optional
        If ``overwrite`` is set to ``False``, and a file already exists with the
        filename ``filename``, then an error is raised and the pre-existing file
        is left unmodified. Otherwise, the HDF5 file with the file structure
        given above will be generated with the filename ``filename``, replacing
        completely any pre-existing file with the same filename.

    Returns
    -------

    """
    overwrite = czekitout.convert.to_bool(obj=overwrite, obj_name="overwrite")
    
    scalar = 0.5
    scalar_id = h5pywrappers.obj.ID(filename=filename,
                                    path_in_file="group-1-A/scalar-1-A")
    write_mode = "w" if overwrite else "w-"
    h5pywrappers.scalar.save(scalar, scalar_id, write_mode)
    
    attr = "m"
    attr_id = h5pywrappers.attr.ID(obj_id=scalar_id, attr_name="units")
    write_mode = "a"
    h5pywrappers.attr.save(attr, attr_id, write_mode)

    dataset = np.random.rand(12, 9, 128, 150)
    dataset_id = h5pywrappers.obj.ID(filename=filename,
                                     path_in_file="group-1-A/dataset-1-A")
    h5pywrappers.dataset.save(dataset, dataset_id, write_mode)

    attr = True
    attr_id = h5pywrappers.attr.ID(obj_id=dataset_id,
                                   attr_name="was_randomly_generated")
    h5pywrappers.attr.save(attr, attr_id, write_mode)

    json_document = {"a": 1, "b": 2, "c": 3}
    json_document_id = \
        h5pywrappers.obj.ID(filename=filename,
                            path_in_file="group-1-B/json-document-1-B")
    h5pywrappers.json.document.save(json_document, json_document_id, write_mode)

    attr = 555
    obj_id = h5pywrappers.obj.ID(filename=filename, path_in_file="group-1-B")
    attr_id = h5pywrappers.attr.ID(obj_id=obj_id, attr_name="numerical_id")
    h5pywrappers.attr.save(attr, attr_id, write_mode)

    return None



###########################
## Define error messages ##
###########################