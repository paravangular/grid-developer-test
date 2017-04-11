# 0. Environment
- Python 3.6

# 1. Instructions

To run the program, simply type in the command line:
```sh
python3 viagogo.py
```

There is also a test program, which can be run by the command:
```sh
python3 test_viagogo.py
```

# 2. Assumptions

- Each event can have a maximum of 99 tickets. 99 is just an arbitrary integer >1.
- Ticket prices range from $0.01 up to $1000.00.
- At least 1 event must exist in the world and up to 21 * 21 events can exist (i.e. all locations have an event).
- Each event has a unique, non-repeatable ID.


# 3. Support for multiple events
Support for multiple events can be included by storing a list of events instead of a single event inside the World class grid. This might not be optimal for fast retrieval, though; currently, the retrieval function `closest_events()` runs in O(N * M) time, where NxM are the dimensions of the world. The slow running time is insignificant with such a small world, but when you allow multiple events in each coordinate, the running time becomes O(N * M * E) where E is the average number of events per square. This wouldn't matter much if E is small, but we don't know how big E is.

Alternatively, instead of a 2D array of locations, the `World` class can maintain a list of events, each with their own `location` property. Assuming a simple linear search, running time would be O(E), where E is the total number of events. Further optimisation of running time is possible using different data structures, as detailed below.

# 4. Support for a larger world size
Several changes must be made. For example, if the world size gets large enough, a database might be needed. Furthermore, there may be performance issues due to the O(N^2) running time. Thus, performance optimisations are necessary. One of the methods we can use is to reduce the search space by filtering events (e.g. by country or city).

We can also improve performance by storing the locations/events in a different data structure. Since this task is essentially a k-nearest neighbour search within a 2D space, spatial indexing using a Quadtree may work. However, since the QuadTree is quite a complex algorithm, the trade-off to implementing it is that the code may be harder to debug/maintain (unless, maybe, if you use a trusted external library!). Other spatial indexing algorithms also exist that may be more suitable.