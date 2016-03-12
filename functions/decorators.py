"""
Decorators
^^^^^^^^^^^^^^^^^^^
"""


# *types refers to args of the decorator,therefore are the type of variables
def requiere(*types):
    """
    This decorator, evaluates that the types pass in a method to be correct
    """

    # realfn refers to itself class,
    def realfn(func):

        # wrapper is the typical function wrapper for decorators
        def wrapper(*args):
            newarg = args[1:]
            for key, mytypes in enumerate(types):
                # isintance return true or false according to comparision,
                # one such example is, isinstance('for_comparision', str) >> return True
                if isinstance(mytypes, type(newarg[key])):  # (not mytypes) was changed by (is not) in view of pep rules
                    # __name__ is used for parser object in text, however must use type method.
                    raise ValueError('change value for {0} not {1}'.format(
                        mytypes.__name__, type(newarg[key]).__name__)
                    )
                    exit(0)
            return func(*args)
        return wrapper
    return realfn
