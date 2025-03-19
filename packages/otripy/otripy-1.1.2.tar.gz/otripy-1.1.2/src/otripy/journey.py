from typing import List, Iterator

from PySide6.QtCore import QObject, Signal

try:
    from .location import Location
except ImportError:
    from location import Location


class Journey(QObject):
    dirty = Signal(bool)

    def __init__(self, locations: List[Location] = None, parent=None):
        """Initialize the journey with a list of Location objects."""
        super().__init__(parent)
        self._locations = locations if locations is not None else []
        self._dirty = False

    def __getitem__(self, index):
        """Enable indexing and slicing."""
        return self._locations[index]

    def __setitem__(self, index, value: Location):
        """Enable item assignment."""
        if not isinstance(value, Location):
            raise TypeError("Only Location instances can be added to the journey.")
        self._dirty = True
        self.dirty.emit(self._dirty)
        self._locations[index] = value

    def __delitem__(self, index):
        """Enable item deletion."""
        self._dirty = True
        self.dirty.emit(self._dirty)
        del self._locations[index]

    def __iter__(self) -> Iterator[Location]:
        """Enable iteration."""
        return iter(self._locations)

    def __len__(self) -> int:
        """Return the number of locations in the journey."""
        return len(self._locations)

    def append(self, location: Location):
        """Add a location to the journey."""
        if not isinstance(location, Location):
            raise TypeError("Only Location instances can be added to the journey.")
        self._dirty = True
        self.dirty.emit(self._dirty)
        self._locations.append(location)

    def insert(self, index: int, location: Location):
        """Insert a location at a specific index."""
        if not isinstance(location, Location):
            raise TypeError("Only Location instances can be inserted into the journey.")
        self._dirty = True
        self.dirty.emit(self._dirty)
        self._locations.insert(index, location)

    def remove(self, location: Location):
        """Remove a location from the journey."""
        self._dirty = True
        self.dirty.emit(self._dirty)
        self._locations.remove(location)

    def __repr__(self) -> str:
        return f"Journey({self._locations})"

    def loc_by_id(self, id: str) -> Location:
        for loc in self:
            if loc.id == id:
                return loc
        return None

    def clear(self):
        self._locations.clear()
        self._dirty = False
        self.dirty.emit(self._dirty)

    def clean(self):
        self._dirty = False
        self.dirty.emit(self._dirty)
