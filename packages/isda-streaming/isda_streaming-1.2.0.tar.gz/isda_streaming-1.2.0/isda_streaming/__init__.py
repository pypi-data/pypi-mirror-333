"""`isda_streaming` is a minimal library intended to learn working with data streams.

The package consists of two modules: `data_stream` and `synopsis`. All public members of
the different modules are directly importable from the top-level module as well. For
example:

```python
from isda_streaming import DataStream

ds = DataStream().from_collection("/path/to/collection.csv")
```

See the respective module documentations for more details.

The implementation is highly simplified and adapted to the requirements of the course
"Informationssysteme und Datenanalyse" at TU Berlin. Therefore, it should not be taken
as a reference to implement a complete data streams management system.

If you notice any errors or inconsistencies in the documentation, please report them in
the course forum or as an issue on
[GitLab](https://git.tu-berlin.de/dima/isda/isda-streaming).
"""

from isda_streaming.data_stream import DataStream, KeyedStream, TimedStream, WindowedStream
from isda_streaming.synopsis import BloomFilter, CountMinSketch, H3HashFunctions, ReservoirSample

__all__ = [
    "BloomFilter",
    "CountMinSketch",
    "DataStream",
    "H3HashFunctions",
    "KeyedStream",
    "ReservoirSample",
    "TimedStream",
    "WindowedStream",
]
__version__ = "1.2.0"
