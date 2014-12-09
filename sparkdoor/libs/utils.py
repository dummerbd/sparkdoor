"""
utils.py - utility functions and classes.
"""
def str_import(dot_path):
    """
    Dynamically import a class, function, or module from a dot path. For
    instance, to import a class named `cls` from a module `mod` that is
    a package `pkg`, you would pass in `pkg.mod.cls`.
    """
    path, name = dot_path.rsplit('.', 1)
    return getattr(__import__(path, globals(), locals(), [name]), name)
