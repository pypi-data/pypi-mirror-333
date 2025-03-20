# peridata

peridata is a simple, tiny (<5KiB!) data storage system using JSON and files,
meant to be easy to use, strict on typing, and to allow easy migrations via changing properties.

## usage

Create a property dictionary:
```py
from peridata import Property, PersistentStorage

epic_property_dict = {"nuclear_bombs": Property[int](default=1)}
```

Then, create a PersistentStorage instance:
```py
ps = PersistentStorage(epic_property_dict, Path(".") / "data" / "makesurethisisafileloc.json")
```

You can then use it like a dictionary; however, adding new keys will error, and typing is checked:
```py
print(ps["nuclear_bombs"]) # Output: 1 (since it's the default set earlier)
# Wait, we're British. That's it, we're invading France.
ps["nuclear_bombs"] -= 1
print(ps["nuclear_bombs"]) # Output: 0
# I'm gonna make a complex amount of nuclear bombs.
ps["nuclear_bombs"] = 2+1j # TypeError: Invalid type for property 'nuclear_bombs'. Expected int, got complex
# Fine, I'll try to store my tea in here, then.
ps["tea"] = Tea(Tea.Brand.YORKSHIRE, quantity=10000).serialize() # KeyError: 'Invalid property: tea'
```

The data is automatically saved to the file location:
```json
// in data/makesurethisisafileloc.json
{
  "nuclear_bombs": 0
}
```

And, loading the PersistentStorage again will take that instead of the default:
```py
epic_property_dict = {"nuclear_bombs": Property[int](default=1)} # The properties stay the same.
ps = PersistentStorage(epic_property_dict, Path(".") / "data" / "makesurethisisafileloc.json") # The file location is also the same.
print(ps["nuclear_bombs"]) # Output: 0
```

You can also protect data; then, if you use write_unprivileged, you will get an error on writing:

```py
epic_property_dict = {"nuclear_bombs": Property[int](default=1),
                      "tea": Property[str](default=Tea(Tea.Brand.YORKSHIRE, quantity=1).serialize(), protected=True)} # The library will manage setting new dictionary values, if you add them.
ps = PersistentStorage(epic_property_dict, Path(".") / "data" / "makesurethisisafileloc.json") # The file location still the same.
ps.write_unprivileged("nuclear_bombs", 100) # This works, since by default protected=False.
# I'm gonna annoy this brit so hard.
ps.write_unprivileged("tea", Coffee().serialize()) # PermissionError: The property 'tea' is protected and cannot be modified from write_unprivileged().
```
