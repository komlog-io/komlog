'''
In this file we define the different error codes that will be
added to the exceptions in the interface web modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 250000 - 300000

'''

from enum import Enum

class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

