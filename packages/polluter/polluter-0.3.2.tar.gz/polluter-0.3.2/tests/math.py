import math
from polluter import Pollutable

po = Pollutable(math, lookup_type="getAttr")
modules = po.select("type=module")
callables = po.select("type=callable")
dicts = po.select("type=dict")
classes = po.select("type=class") 
strings = po.select("type=string")

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

print("\nStrings:")
for path, value in strings.items():
  print(f"{path}: {value}")