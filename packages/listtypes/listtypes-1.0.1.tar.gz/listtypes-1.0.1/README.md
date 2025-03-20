# ListTypes
A python package full of diffrent types of lists, all of which are type safe.

## Install
Use pip to install the package.
```
pip install listtypes
```

Then import into any project like so:
```py
from listtypes import TypeList, StringList, IntList # etc
```

## Types of Lists
Here is a full list of all the types of lists you can import.
```py
TypeList(t: type, l: list = []) # used as a base for every list, can be used to make custom lists of a certian type.
StringList(l: list = [])
IntList(l: list = [])
FloatList(l: list = [])
BoolList(l: list = [])
DictList(l: list = [])
```

## Contributing
If you'd like to contribute to this project just open a Pull Request detailing what you're adding, removing and otherwise fixing.

## Issues
If you were to find a bug in this package (which is likely to happen at some point) report it on the issues page.
