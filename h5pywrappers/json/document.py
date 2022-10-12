r"""For loading and saving JSON documents objects.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# For deserializing JSON documents.
import json



# For checking whether an object is an HDF5 object.
import h5py



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
__all__ = ["load",
           "save"]



def load(json_document_id):
    r"""Load a JSON document from an HDF5 file.

    A JSON document is a dictionary that can be directly serialized into the
    JSON format. JSON documents are stored as ``bytes`` objects or ``numpy``
    bytes arrays in HDF5 files.

    Parameters
    ----------
    json_document_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying the JSON document of interest.

    Returns
    -------
    json_document : `dict`
        The JSON document of interest.

    """
    try:
        dataset = h5pywrappers.dataset.load(json_document_id, read_only=True)
        json_document = json.loads(dataset[()])
        dataset.file.close()
        if not isinstance(json_document, dict):
            raise
    except:
        dataset.file.close()
        raise TypeError(_load_err_msg_1)

    return json_document



def save(json_document, json_document_id, write_mode="w-"):
    r"""Save a JSON document to an HDF5 file.

    A JSON document is a dictionary that can be directly serialized into the
    JSON format. JSON documents are stored as ``bytes`` objects or ``numpy``
    bytes arrays in HDF5 files.

    Parameters
    ----------
    json_document : `dict` | :class:`h5py.Dataset`
        The JSON document of interest to save to an HDF5 file.
    json_document_id : :class:`h5pywrappers.obj.ID`
        The parameter set specifying where to save the JSON document of 
        interest.
    write_mode : "w" | "w-" | "a" | "a-", optional
        The write mode upon opening the HDF5 file to which to save the HDF5 JSON
        document of interest: if ``write_mode`` is set to ``"w"``, then the
        target HDF5 file is emptied prior to saving the HDF5 JSON document of
        interest; else if ``write_mode`` is set to ``"w-"``, then the HDF5 JSON
        document of interest is saved unless a file already exists with the
        target filename, in which case an error is raised and the target HDF5
        file is left unmodified; else if ``write_mode`` is set to ``"a-"``, then
        the HDF5 JSON document of interest is saved unless an HDF5 object
        already exists at the target HDF5 path of the target HDF5 file, in which
        case an error is raised and the target HDF5 file is left unmodified;
        else if ``write_mode`` is set to ``"a"``, then the HDF5 JSON document of
        interest is saved without emptying the target HDF5 file, replacing any
        HDF5 object at the target HDF5 path should one exist prior to saving.

    Returns
    -------

    """
    try:
        if isinstance(json_document, dict):
            serialized_json_document = json.dumps(json_document)
        elif isinstance(json_document, h5py._hl.dataset.Dataset):
            serialized_json_document = json_document[()]
            if not isinstance(json.loads(serialized_json_document), dict):
                raise
        else:
            raise    
    except:
        raise ValueError(_save_err_msg_1)
            
    h5pywrappers.dataset.save(serialized_json_document,
                              json_document_id,
                              write_mode)

    return None



###########################
## Define error messages ##
###########################

_load_err_msg_1 = \
    ("The object at the HDF5 path of the HDF5 file specified by the parameter "
     "``json_document_id`` is not of the expected type, i.e. a JSON-serialized "
     "dictionary stored as a ``bytes`` object or a ``numpy`` bytes array.")

_save_err_msg_1 = \
    ("The object ``json_document`` must be either a JSON-serializable "
     "dictionary or a zero-dimensional HDF5 dataset that stores a "
     "JSON-serialized dictionary as a ``bytes`` object or a ``numpy`` bytes "
     "array.")
