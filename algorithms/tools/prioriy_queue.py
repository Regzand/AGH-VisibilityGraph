"""
Priority queue based on heapq and code from:
https://github.com/Luca1995it/SweepLineAlgorithm
"""
from heapq import heappush, heappop
from typing import Generic, TypeVar, List, Iterable

T = TypeVar('T')


class PriorityQueue(Generic[T]):
    """ Class that implements (unique) priority queue using heapq. """

    def __init__(self):
        """ Creates priority queue. """
        self.queue: List[T] = []

    def push_all(self, elements: Iterable[T]):
        """ Adds all elements from given iterable. """
        for e in elements:
            self.push(e)

    def push(self, e: T):
        """ Adds given element to this queue. """
        heappush(self.queue, e)

    def pop(self) -> T:
        """ Pops first element from queue. """
        if self.is_empty():
            raise ValueError('Cannot pop element, queue is empty')
        return heappop(self.queue)

    def clear(self):
        """ Clears this queue. """
        self.queue = []

    def is_empty(self) -> bool:
        """ Returns whether this queue is empty. """
        return len(self.queue) == 0

    def __len__(self) -> int:
        """ Returns size of queue. """
        return len(self.queue)

    def __str__(self) -> str:
        """ Creates string representation of this queue. """
        return '[' + ' '.join([str(i) for i in self.queue]) + ']'
