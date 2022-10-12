r"""For loading and saving HDF5 "scalars".

"""



#####################################
## Load libraries/packages/modules ##
#####################################

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
    dataset = h5pywrappers.dataset.load(scalar_id, read_only=True)

    if len(dataset.shape) != 0:
        dataset.file.close()
        raise TypeError(_load_err_msg_1)
    
    try:
        scalar = complex(dataset[()])
        dataset.file.close()
    except:
        dataset.file.close()
        raise TypeError(_load_err_msg_1)

    if scalar.imag == 0:
        scalar = scalar.real

    return scalar



def save(scalar, scalar_id, write_mode="w-"):
    r"""Save an HDF5 "scalar" to an HDF5 file as a zero-dimensional HDF5 
    dataset.

    By "scalar", we mean the single numerical data element from a
    zero-dimensional HDF5 dataset.

    Parameters
    ----------
    scalar : `float` | `complex` | :class:`h5py._hl.dataset.Dataset`
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
    scalar = h5pywrappers.dataset._check_dataset(scalar)
    if len(scalar.shape) != 0:
        raise TypeError(_save_err_msg_1)

    try:
        complex(scalar[()])
    except:
        raise TypeError(_save_err_msg_1)
    
    h5pywrappers.dataset.save(scalar, scalar_id, write_mode)

    return None



###########################
## Define error messages ##
###########################

_load_err_msg_1 = \
    ("The object at the HDF5 path of the HDF5 file specified by the parameter "
     "``scalar_id`` is not of the expected type, i.e. an HDF5 scalar.")

_save_err_msg_1 = \
    ("The object ``scalar`` must be of the type `float` or `complex`, or it "
     "must be a zero-dimensional HDF5 dataset containing numerical data.")
