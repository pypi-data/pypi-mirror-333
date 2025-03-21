import os
import sys
import inspect
from dataclasses import is_dataclass
from collections import OrderedDict, defaultdict, deque, Counter, ChainMap, UserDict, UserList, UserString
from importlib.util import find_spec

stdlib_paths = {
  os.path.normpath(path) for path in sys.path
  if os.path.isdir(path) and (
    "lib/python" in path and "site-packages" not in path and "dist-packages" not in path
  )
}

def is_from_standard_library(obj):
  module = inspect.getmodule(obj)
  if module is None:
    # If obj is a method-wrapper:
    if type(obj).__name__ in ["method-wrapper", "builtin_function_or_method", "method_descriptor", "getset_descriptor", ]:
      return True
    return False

  module_file = getattr(module, "__file__", None)
  # No module file, then it's module builtins
  if module_file is None:
    return True
  
  module_file = os.path.normpath(module_file)
  for path in stdlib_paths:
    if module_file.startswith(os.path.join(path, "")):
      return True
  return False

def is_standard_module(module):
  """
  Check if the module is part of the Python standard library.

  @params module: The module to check.
  @return: True if the module is part of the standard library, False otherwise.
  """
  if module is None:
    return False
  
  module_file = getattr(module, "__file__", None)
  if module_file is None:
    return False
  
  module_file = os.path.normpath(module_file)
  for path in stdlib_paths:
    if module_file.startswith(os.path.join(path, "")):
      return True
  return False

def get_type_info(val):
  """
  Get the type information of the object.

  @params val: The object to get the type information for.
  @return: A string representing the type of the object.
  """
  if val is None:
    return "None"

  type_name = type(val).__name__

  if type_name == "method-wrapper":
    return "method-wrapper"
  elif type_name == "builtin_function_or_method":
    return "builtin method"
  elif isinstance(val, str) and val.__class__.__name__ == "str":
    return "string"
  elif type_name == "module":
    return "module"
  elif type_name == "function":
    return "function"
  elif type_name == "type":
    return "class"
  elif is_dataclass(val):
    return "dataclass"
  elif type_name == "dict":
    return "dict"
  elif isinstance(val, OrderedDict):
    return "OrderedDict"
  elif isinstance(val, defaultdict):
    return "defaultdict"
  elif isinstance(val, deque):
    return "deque"
  elif isinstance(val, Counter):
    return "Counter"
  elif isinstance(val, ChainMap):
    return "ChainMap"
  elif isinstance(val, UserDict):
    return "UserDict"
  elif isinstance(val, UserList):
    return "UserList"
  elif isinstance(val, UserString):
    return "UserString"
  elif type_name == "list":
    return "list"
  elif type_name == "tuple":
    return "tuple"
  elif type_name == "set":
    return "set"
  elif type_name in ["int", "float", "complex"]:
    return "number"
  elif type_name == "bool":
    return "boolean"
  else:
    return type_name

def get_name_info(val):
  """
  Get the name information of the object.

  @params val: The object to get the name information for.
  @return: A string representing the name of the object.
  """
  if val is None:
    return "None"

  type_name = type(val).__name__

  if type_name == "method-wrapper":
    method_name = getattr(val, "__name__", "unknown_method")
    return f"{method_name}"
  elif type_name == "builtin_function_or_method":
    method_name = getattr(val, "__name__", "unknown_method")
    return f"{method_name}"
  elif isinstance(val, str) and val.__class__.__name__ == "str":
    return val
  elif type_name == "module":
    module_name = getattr(val, "__name__", "UnknownModule")
    return module_name
  elif type_name == "function":
    return getattr(val, "__name__", "unknown_function")
  elif type_name == "type":
    class_name = getattr(val, "__name__", "UnknownClass")
    return class_name
  elif is_dataclass(val):
    class_name = val.__class__.__name__
    return class_name
  elif type_name == "dict":
    return "dict"
  elif isinstance(val, OrderedDict):
    return "OrderedDict"
  elif isinstance(val, defaultdict):
    return "defaultdict"
  elif isinstance(val, deque):
    return "deque"
  elif isinstance(val, Counter):
    return "Counter"
  elif isinstance(val, ChainMap):
    return "ChainMap"
  elif isinstance(val, UserDict):
    return "UserDict"
  elif isinstance(val, UserList):
    return "UserList"
  elif isinstance(val, UserString):
    return "UserString"
  elif type_name == "list":
    return "list"
  elif type_name == "tuple":
    return "tuple"
  elif type_name == "set":
    return "set"
  elif type_name in ["int", "float", "complex"]:
    return str(val)
  elif type_name == "bool":
    return str(val)
  else:
    return type_name

def is_c_written(func):
  """
  Check if the function is written in C.

  @params func: The function to check.
  """
  try:
    return type(func).__flags__ & (1<<9)
  except Exception as e:
    return False