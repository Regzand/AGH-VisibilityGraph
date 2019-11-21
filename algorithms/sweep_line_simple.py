from dataclasses import dataclass, field
from typing import List

from algorithms.tools import PriorityQueue, Event
from geometry import Collection, Segment

EVENT_BEGIN = 'start'
EVENT_END = 'end'


@dataclass
class SweepEvent(Event):
    segment: Segment = field(compare=False, default=None)


def sweep_line_simple(collection: Collection) -> Collection:

    # create priority queue of events
    events = PriorityQueue()

    # add starting points to events
    events.push_all(SweepEvent(min(*seg), EVENT_BEGIN, seg) for seg in collection.all_segments)
    # add ending points to events
    events.push_all(SweepEvent(max(*seg), EVENT_END, seg) for seg in collection.all_segments)

    # structure for

    # while there are events to handle
    while not events.is_empty():
        event = events.pop()
        print(event)

    return Collection()
