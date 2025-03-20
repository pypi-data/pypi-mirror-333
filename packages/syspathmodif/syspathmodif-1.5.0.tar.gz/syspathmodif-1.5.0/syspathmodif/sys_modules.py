import sys


def sm_contains(module_name):
	"""
	Dictionary sys.modules maps module and package names (str) to the
	corresponding module or package. This function indicates whether
	sys.modules contains the module or package whose name is the argument.

	Args:
		module_name (str): the name of a module or package.

	Returns:
		bool: True if argument module_name is a key in sys.modules, False
			otherwise.
	"""
	return module_name in sys.modules


__all__ = [sm_contains.__name__]
