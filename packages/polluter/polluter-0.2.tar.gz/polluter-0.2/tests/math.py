import math
from src.pollutable import Pollutable

po = Pollutable(math, lookup_type="getAttr")
modules = po.select("type=module&builtin=no")
callables = po.select("type=callable&builtin=no")
dicts = po.select("type=dict&builtin=no")
classes = po.select("type=class&builtin=no") 

print("Modules:")
for path, value in modules.items():
  print(f"{path}: {value}")

# Select callables
print("\nCallables:")
for path, value in callables.items():
  print(f"{path}: {value}")

print("\nDicts:")
for path, value in dicts.items():
  print(f"{path}: {value}")

print("\nClasses:")
for path, value in classes.items():
  print(f"{path}: {value}")