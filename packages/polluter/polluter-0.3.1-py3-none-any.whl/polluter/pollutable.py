#!/usr/bin/env python3
"""
@description
---------------------
This script contains the useful functions to find the pollutables reflectively during runtime.

import polluter as pl
po = new pl.Pollutable(obj, max_layer=1, lookup_type="getAttr")
"""
import inspect
import logging
from .utils import get_type_info, get_name_info, is_from_standard_library, is_standard_module

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)

class Pollutable:
  def __init__(self, target, max_layer=3, lookup_type="getAttr"):
    """
    @description
    ---------------------
    The class to represent the pollutable object.

    @params target: The object to pollute.
    @params max_layer: The maximum layer to search for pollutables.
    @params lookup_type: The type of pollutables to find. Default is "getAttr" and alternative is "getBoth".
    """ 
    self.target = target
    self.max_layer = max_layer
    self.lookup_type = lookup_type

    self.summary = self.search(max_layer)
  
  def search(self, max_layer=-1):
    """
    @description
    ---------------------
    Find all the pollutables in the given object with logging support.

    @params max_layer: The maximum layer to search for pollutables.
    """
    if max_layer == -1:
      max_layer = self.max_layer

    logging.debug(f"Starting find_all_pollutables. Type: {self.lookup_type}, Layer: {0}, Max Layer: {max_layer}")

    if self.lookup_type == "getAttr":
      logging.info("Using 'getAttr' method to find pollutables.")
      self.summary = self.find_all_pollutables_getattr_only(self.target, 0, max_layer)
    elif self.lookup_type == "getBoth":
      logging.warning("'getBoth' type is not implemented yet.")
      raise NotImplementedError("getBoth is not implemented")
    else:
      logging.error(f"Unknown type specified: {self.lookup_type}")
      raise Exception(f"Unknown type: {self.lookup_type}")

    return self.summary
  
  def find_all_pollutables_getattr_only(self, obj, layer=0, max_layer=1, callable_only=False):
    """Find all pollutables in the given object using getattr recursively, logging module names."""
    logging.debug(f"Entering layer {layer}. Object type: {type(obj)}")
    
    pollutables = {}
    if layer >= max_layer:
      logging.debug(f"Reached maximum layer ({max_layer}). Stopping recursion.")
      return pollutables
    
    for name in dir(obj):
      try:
        value = getattr(obj, name)
        logging.debug(f"Accessed attribute: {name}")
      except Exception as e:
        logging.warning(f"Could not access attribute '{name}': {str(e)}")
        continue
      
      if callable_only and not callable(value):
        logging.debug(f"Skipping non-callable attribute: {name}")
        continue
      
      current_path = name
      
      if inspect.ismodule(value):
        module_name = getattr(value, "__name__", "UnknownModule")
        is_standard = is_standard_module(value)
        pollutables[current_path] = ("module", module_name, is_standard, True)
      else:
        try:
          # (type, name, standard?, writable?)
          type_info = get_type_info(value)
          name_info = get_name_info(value)
          is_standard = is_from_standard_library(value)
          pollutables[current_path] = (type_info, name_info, is_standard, True)
          logging.debug(f"Added attribute: {current_path} (Value: {pollutables[current_path]})")
        except Exception as e:
          type_name = type(value).__name__
          pollutables[current_path] = (type_name, type_name, True, True)
          logging.warning(f"Could not get repr for {current_path}. Using type name: {type_name}. Error: {str(e)}")
      
      if layer < max_layer and not inspect.ismodule(value):
        logging.debug(f"Recursing into attribute: {current_path} at layer {layer + 1}")
        sub_pollutables = self.find_all_pollutables_getattr_only(
          value, layer + 1, max_layer, callable_only
        )
        for sub_path, sub_type in sub_pollutables.items():
          full_path = f"{current_path}.{sub_path}"
          pollutables[full_path] = sub_type
          logging.debug(f"Added sub-attribute: {full_path} (Type: {sub_type})")
    
    return pollutables

  def find(self, path):
    """
    Find the object based on the path.

    @params path: The path to find the object.
    @return obj: The object found based on the path.
    """
    obj = self.target
    for attr in path.split('.'):
      obj = getattr(obj, attr)
    return obj
  
  def select(self, query):
    """
    Select the object based on the query.

    @params query: The query to select the object.
    Supported queries:
    - "type=module" -> Select the modules.
    - "type=callable" -> Select the callables.
    - "type=method" -> Select the methods.
    - "type=function" -> Select the functions.
    - "type=noncallable" -> Select the non-callable attributes.
    - "type=dict" -> Select the dictionaries.
    - "type=OrderedDict" -> Select the OrderedDicts.
    - "type=defaultdict" -> Select the defaultdicts.
    - "type=deque" -> Select the deques.
    - "type=Counter" -> Select the Counters.
    - "type=ChainMap" -> Select the ChainMaps.
    - "type=UserDict" -> Select the UserDicts.
    - "type=UserList" -> Select the UserLists.
    - "type=UserString" -> Select the UserStrings.
    - "type=class" -> Select the classes.
    - "type=dataclass" -> Select the dataclasses.
    - "type=string" -> Select the strings.
    - "type=number" -> Select the numbers.
    - "type=boolean" -> Select the booleans.
    - "builtin=no" -> Select the user-defined objects.
    - Combined queries like "type=class&builtin=no" -> Select user-defined classes.

    @return selected: A dictionary of selected paths and their values.
    """
    selected = {}
    queries = query.split('&')  # Split combined queries

    for path, value in self.summary.items():
      type_info, name_info, is_standard, writable = value
      matches_all = True

      for q in queries:
        if '=' not in q:
          continue  # Skip invalid queries

        key, val = q.split('=')
        if key == "type":
          if val == "module" and type_info != "module":
            matches_all = False
          elif val == "callable" and type_info not in [
            "method-wrapper", "builtin method", "builtin method (C-written)", "function"
          ]:
            matches_all = False
          elif val == "method" and type_info != "method-wrapper":
            matches_all = False
          elif val == "function" and type_info != "function":
            matches_all = False
          elif val == "noncallable" and type_info in [
            "method-wrapper", "builtin method", "builtin method (C-written)", "function"
          ]:
            matches_all = False
          elif val == "dict" and type_info not in ["dict", "OrderedDict", "defaultdict"]:
            matches_all = False
          elif val == "deque" and type_info != "deque":
            matches_all = False
          elif val == "Counter" and type_info != "Counter":
            matches_all = False
          elif val == "ChainMap" and type_info != "ChainMap":
            matches_all = False
          elif val == "UserDict" and type_info != "UserDict":
            matches_all = False
          elif val == "UserList" and type_info != "UserList":
            matches_all = False
          elif val == "UserString" and type_info != "UserString":
            matches_all = False
          elif val == "class" and not type_info.startswith("class"):
            matches_all = False
          elif val == "dataclass" and not type_info.startswith("dataclass"):
            matches_all = False
          elif val == "string" and type_info != "string":
            matches_all = False
          elif val == "number" and type_info not in ["int", "float", "complex"]:
            matches_all = False
          elif val == "boolean" and type_info != "bool":
            matches_all = False
        elif key == "builtin":
          if val == "no" and is_standard:
            matches_all = False

      if matches_all:
        selected[path] = value

    return selected