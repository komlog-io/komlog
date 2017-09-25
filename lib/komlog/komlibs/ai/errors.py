'''
In this file we define the different error codes that will be
added to the exceptions in the ai modules, to identify
the point in the code where it raised

The pattern used to name an error is:

E_XXX_YYY_ZZZ

where:

- XXX is the code to identify the file
- YYY is the code to identify the function
- ZZZ is the code to identify the reason the exception was raised

The range reserved for Errors.in this module is 400000 - 449999

'''

from enum import Enum, unique

@unique
class Errors(Enum):
#common to every Error class

    OK              = 0
    UNKNOWN         = 1

#ai decisiontree api

    E_ADA_GIV_LNF   = 400000    # label not found in features
    E_ADA_GIV_FEX   = 400001    # feature exhaustion. no more features left to classify
    E_ADA_GIV_ESF   = 400002    # error sorting features.

    E_ADA_TMCL_EDF  = 400010    # _train_multi_classifier. Error empty dataframe
    E_ADA_TMCL_UCFL = 400011    # _train_multi_classifier. unresolved conflicts found

