"""
Tree set based on code from:
https://github.com/Luca1995it/SweepLineAlgorithm
"""
import bisect
from typing import TypeVar, Generic, List, Iterable, Optional, Any

T = TypeVar('T')


class TreeSet(Generic[T]):
    """ Implements binary-tree set. """

    def __init__(self):
        """ Creates binary-tree set """
        self.data: List[T] = []

    def push_all(self, elements: Iterable[T]):
        """ Adds all elements to this tree set. """
        for element in elements:
            self.push(element)

    def push(self, element: T):
        """ Adds given element to this tree set. """
        if element not in self:
            bisect.insort_right(self.data, element)

    def pop(self, index: int = 0) -> Optional[T]:
        """ Returns first element from data. """
        return self.data.pop(index)

    def swap(self, e1: T, e2: T):
        """ Swaps given two elements. """
        i1 = self.data.index(e1)
        i2 = self.data.index(e2)
        self.data[i1] = e2
        self.data[i2] = e1

    def greater(self, element: T) -> Optional[T]:
        """ Returns element that is greater than given one. """
        index = bisect.bisect_right(self.data, element)
        if index >= len(self.data):
            return None
        return self.data[index]

    def lesser(self, element: T) -> Optional[T]:
        """ Returns element that is lesser than given one. """
        index = bisect.bisect_left(self.data, element)
        if index < 1:
            return None
        return self.data[index - 1]

    def remove(self, element: T) -> T:
        """ Removes element from this tree. """
        index = bisect.bisect_left(self.data, element)
        if 0 <= index < len(self.data) and self.data[index] == element:
            return self.data.pop(index)
        return None

    def clear(self):
        """ Clears this tree set. """
        self.data = []

    def __contains__(self, element: T) -> bool:
        """ Returns whether given elements exists in tree. """
        index = bisect.bisect_left(self.data, element)
        return 0 <= index < len(self.data) and self.data[index] == element

    def is_empty(self) -> bool:
        """ Returns where this set is empty """
        return len(self.data) == 0

    def __len__(self) -> int:
        """ Returns size of this tree. """
        return len(self.data)

    def __str__(self) -> str:
        """ Returns string representation. """
        return '[' + ' '.join([str(i) for i in self.data]) + ']'

    def __iter__(self):
        """ Returns ascending iterator. """
        for element in self.data:
            yield element
