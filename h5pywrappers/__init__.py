"""``h5pywrappers`` is a simple Python library that defines some classes with
useful features, such as enforced validation, updatability, pre-serialization,
and de-pre-serialization. These classes can be used to define more complicated
classes that inherit some subset of the aforementioned features.

"""



#####################################
## Load libraries/packages/modules ##
#####################################

# Import child modules and packages of current package.
import h5pywrappers.obj
import h5pywrappers.dataset
import h5pywrappers.datasubset
import h5pywrappers.scalar
import h5pywrappers.json
import h5pywrappers.attr
import h5pywrappers.file
import h5pywrappers.version



############################
## Authorship information ##
############################

__author__       = "Matthew Fitzpatrick"
__copyright__    = "Copyright 2022"
__credits__      = ["Matthew Fitzpatrick"]
__version__      = h5pywrappers.version.version
__full_version__ = h5pywrappers.version.full_version
__maintainer__   = "Matthew Fitzpatrick"
__email__        = "mrfitzpa@uvic.ca"
__status__       = "Development"



###################################
## Useful background information ##
###################################

# See e.g. ``https://docs.python.org/3/reference/import.html#regular-packages``
# for a brief discussion of ``__init__.py`` files.



##################################
## Define classes and functions ##
##################################

# List of public objects in package.
__all__ = ["show_config"]



def show_config():
    """Print information about the version of ``h5pywrappers`` and libraries it 
    uses.

    """
    print(version.version_summary)

    return None



###########################
## Define error messages ##
###########################
