# Object references, mutability and recycling
"""
    Example 8-2 : Variacles are assigned to objects only after the objects are created.

    Example 'Choosing between '==' and 'is'
    -> The '== operator' computes the values of objects(the data they hold), while 'is'
       compares their identities.

    The relative immutability of tuples

    Copies are shallow by default....
    -> using the constructor or [:] produces a shallow copy

    Deep and shallow copies of arbitrary object
    -> using copy() and deepcopy()
"""

"""
    Function parameters as references
    The only mode of parameter passing in Python is "call by sharing."
    "call by sharing" means that each formal parameter of the function gets
    a copy of each reference in the arguments. In other words, the parameters inside
    the function become aliases of the actual arguments.
    
    The result of this scheme is that a function may change any mutable object passed
    as a parameter, but it cannot change the identity of those objects.
"""

"""
    Mutable types as parameter defaults: bad idea
    You should avoid mutable objects as default values for parameters
    
"""
