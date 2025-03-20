"""This module defines different types of data streams and their operators."""

from __future__ import annotations

import csv
import numbers
from abc import ABC
from numbers import Number
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, ParamSpec, TypeVar

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

__all__ = ["DataStream", "KeyedStream", "TimedStream", "WindowedStream"]


P = ParamSpec("P")
T = TypeVar("T")


def _requires_non_empty(func: Callable[P, T]) -> Callable[P, T]:
    """Decorates arbitrary DataStream methods with a stream length check.

    If the stream length doesn't match the specified criteria, a StreamException will
    be raised.
    """

    def check_length(*args: P.args, **kwargs: P.kwargs) -> T:
        self = args[0]
        if not isinstance(self, StreamBase):
            raise TypeError("_requires_non_empty() decorator may only be used on stream objects.")
        if len(self._stream) < 1:
            raise StreamError(f"To perform {func.__name__}() on a stream, it must be non-empty.")
        return func(*args, **kwargs)

    return check_length


class StreamBase(ABC):
    """Base class for all stream types."""

    _stream: list[Any]

    def __init__(self) -> None:
        """Create an empty `DataStream`."""
        self._stream = []


class DataStream(StreamBase):
    """A basic data stream."""

    def __init__(self) -> None:
        """Create an empty `DataStream`."""
        super().__init__()

    def __eq__(self, other: object) -> bool:
        """Check if two `DataStream` objects are equal."""
        if isinstance(other, DataStream):
            return self._stream == other._stream
        return False

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the stream."""
        yield from self._stream

    def __str__(self) -> str:
        """Return a string representation of the stream."""
        return f"DataStream({self._stream})"

    def _add_element(self, element: Any) -> None:
        """Add a value to the stream."""
        if isinstance(element, list):
            raise StreamError("Got multiple elements to add, use `add_elements` instead.")
        self._stream.append(element)

    def _add_elements(self, collection: list[Any]) -> None:
        """Add multiple values to the stream."""
        for x in collection:
            if isinstance(x, list):
                raise StreamError(
                    "Stream elements must not be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )
        self._stream.extend(collection)

    def from_collection(self, collection: list[Any]) -> DataStream:
        """Initialize a `DataStream` with values from a list.

        Can only be used on empty streams.

        Args:
            collection: list of values (values must not be of type list)
        """
        if len(self._stream) > 0:
            raise StreamError("from_collection can only be used on empty streams.")
        if not isinstance(collection, list):
            raise StreamError(f"collection must be of type list, got {type(collection)}.")
        for x in collection:
            if isinstance(x, list):
                raise StreamError(
                    "Stream elements must not be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )

        self._stream = collection.copy()
        return self

    def from_csv(self, path: str, start: int | None = None, end: int | None = None) -> DataStream:
        """Initialize a `DataStream` with values from a CSV file.

        Can only be used on empty streams.

        Args:
            path: location of a CSV file to load
            start: index of the first row to be added (defaults to first line)
            end: index of the last row to be added (defaults to last line)
        """
        if len(self._stream) > 0:
            raise StreamError("from_csv can only be used on empty streams.")
        if path[-4:] != ".csv":
            raise StreamError("Only CSV files are supported.")

        if start is None:
            start = 0
        with Path(path).open(encoding="utf-8") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for i, row in enumerate(reader):
                if end is not None and i > end:
                    break
                if i >= start:
                    if len(row) > 1:
                        self._stream.append(tuple(row))
                    elif len(row) == 1:
                        self._stream.append(row[0])
        return self

    def map(self, map_function: Callable[[Any], Any]) -> DataStream:
        """Perform a `map_function` on the stream.

        A `map_function` creates exactly one output element per input element.
        """
        result = DataStream()
        for x in self._stream:
            map_x = map_function(x)
            if isinstance(map_x, list):
                raise StreamError(
                    "A map function must return a single element per processed element."
                )
            result._add_element(map_x)
        return result

    def flat_map(self, flat_map_function: Callable[[Any], list[Any]]) -> DataStream:
        """Perform a `flat_map_function` on the stream.

        A `flat_map_function` creates zero, one, or multiple elements per
        input element. Note that the output of the `flat_map_function` has to be of
        type list. Therefore, if `flat_map_function` creates zero elements return an
        empty list `[]`.
        """
        result = DataStream()
        for x in self._stream:
            flat_map_x = flat_map_function(x)
            if not isinstance(flat_map_x, list):
                raise StreamError(
                    "A flat_map function must return a list of elements per processed "
                    " element. Such list may contain zero, one, or more elements."
                )
            result._add_elements(flat_map_x)
        return result

    def filter(self, filter_function: Callable[[Any], bool]) -> DataStream:
        """Perform a `filter_function` on the stream.

        A `filter_function` evaluates a boolean predicate for each element and returns
        those for which the function is true.
        """
        result = DataStream()
        for x in self._stream:
            filter_x = filter_function(x)
            if not isinstance(filter_x, bool):
                raise StreamError(
                    "A filter function must return a single boolean value per processed element."
                )
            if filter_x:
                result._add_element(x)
        return result

    def reduce(self, reduce_function: Callable[[Any, Any], Any]) -> DataStream:
        """Perform a `reduce_function` on the stream.

        A `reduce_function` combines the current element with the last reduced value and
        outputs the result. Note that the output of the `reduce_function` has to be of
        the same type (and structure, in case of tuples) as the input values.
        """
        result = DataStream()
        first = True
        reduce_x = None

        for x in self._stream:
            if first:
                first = False
                reduce_x = x
            else:
                reduce_x = reduce_function(reduce_x, x)
            if isinstance(reduce_x, list):
                raise StreamError(
                    "A reduce function must return a single element per processed element."
                )
            if not isinstance(reduce_x, type(x)):
                raise StreamError(
                    "The output of the reduce_function has to be of the "
                    "same type as the input values."
                )
            if isinstance(reduce_x, tuple) and len(reduce_x) != len(x):
                raise StreamError(
                    "The output of the reduce_function, when dealing with tuples, "
                    "has to be of the same structure as the input values "
                    "(i.e., len(reduce_x) == len(x))."
                )
            result._add_element(reduce_x)
        return result

    def key_by(self, key_by_function: Callable[[Any], Any]) -> KeyedStream:
        """Convert the stream into a `KeyedStream` based on a `key_by_function`.

        A `key_by_function` divides a stream into disjoint partitions. All records with
        the same key are assigned to one partition.
        """
        result = KeyedStream()
        for x in self._stream:
            key_x = key_by_function(x)
            if isinstance(key_x, list):
                raise StreamError(
                    "A reduce function must return a single element per processed element."
                )
            result._add_element(key_x, x)
        return result

    @_requires_non_empty
    def landmark_window(self, size: int) -> WindowedStream:
        """Discretize the stream with tuple-based landmark windows."""
        if not isinstance(size, int) or size < 1:
            raise StreamError("The window size must be an integer and greater than 0.")
        windowed_stream = WindowedStream()
        window = []
        for i, x in enumerate(self._stream):
            window.append(x)
            if len(window) % size == 0:
                windowed_stream._add_new_window(window, 0, i)
        return windowed_stream

    @_requires_non_empty
    def tumbling_window(self, size: int) -> WindowedStream:
        """Discretize the stream with tuple-based tumbling windows."""
        if not isinstance(size, int) or size < 1:
            raise StreamError("The window size must be an integer and greater than 0.")
        windowed_stream = WindowedStream()
        window = []
        for i, x in enumerate(self._stream):
            window.append(x)
            if len(window) == size:
                windowed_stream._add_new_window(window, i + 1 - size, i)
                window = []
        return windowed_stream

    @_requires_non_empty
    def sliding_window(self, size: int, slide: int) -> WindowedStream:
        """Discretize the stream with tuple-based sliding windows."""
        if not isinstance(size, int) or size < 1 or slide < 1 or size <= slide:
            raise StreamError(
                "The window size and slide must be integers, greater than 0, and slide "
                "must be smaller than size."
            )
        windowed_stream = WindowedStream()
        windows: list[list[Any]] = [[]]
        slide_count = 0
        remove_head = False
        for i, x in enumerate(self._stream):
            if slide_count == slide:
                windows.append([])
                slide_count = 1
            else:
                slide_count += 1
            for window in windows:
                window.append(x)
                if len(window) == size:
                    windowed_stream._add_new_window(window, i + 1 - size, i)
                    remove_head = True
            if remove_head:
                windows.pop(0)
                remove_head = False
        return windowed_stream


class KeyedStream:
    """An extension of a basic `DataStream` that is partitioned by a set of keys."""

    _streams: dict[Any, Any]

    def __init__(self) -> None:
        """Create an empty `KeyedStream`."""
        self._streams = {}

    def __eq__(self, other: object) -> bool:
        """Check if two `KeyedStream` objects are equal."""
        if isinstance(other, KeyedStream):
            return self._streams == other._streams
        return False

    def __str__(self) -> str:
        """Return a string representation of the stream."""
        return f"KeyedStream({dict(sorted(self._streams.items()))})"

    def _add_element(self, key: Any, element: Any) -> None:
        """Add a value to the stream."""
        if isinstance(key, list):
            raise StreamError(
                "A key cannot be of type list. To use keys with multiple values, "
                "use tuples instead."
            )
        if isinstance(element, list):
            raise StreamError("Got multiple elements to add, use `add_elements` instead.")

        if key in self._streams:
            self._streams[key].append(element)
        else:
            self._streams[key] = [element]

    def _add_elements(self, key: Any, collection: list[Any]) -> None:
        """Add multiple values to the stream."""
        if isinstance(key, list):
            raise StreamError(
                "A key cannot be of type list. To use keys with multiple values, "
                "use tuples instead."
            )
        for x in collection:
            if isinstance(x, list):
                raise StreamError(
                    "Stream elements cannot be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )

        if key in self._streams:
            self._streams[key].extend(collection)
        else:
            self._streams[key] = collection.copy()

    def from_dict(self, dict_: dict[Any, Any]) -> KeyedStream:
        """Initialize a `DataStream` with values from a dictionary.

        Can only be used on empty streams.

        Args:
            dict_: dictionary to load into the stream (keys and values must not be of
                type list)
        """
        if len(self._streams) > 0:
            raise StreamError("from_dict can only be used on empty streams.")
        if not isinstance(dict_, dict):
            raise StreamError(f"dict_ must be of type list, got {type(dict_)}.")
        for k, v in dict_.items():
            if isinstance(k, list) or isinstance(v, list):
                raise StreamError(
                    "Stream keys or elements must not be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )

        self._streams = dict_.copy()
        return self

    def map(self, map_function: Callable[[Any], Any]) -> KeyedStream:
        """Perform a `map_function` on the stream.

        A `map_function` creates exactly one output element per input element.
        """
        result = KeyedStream()
        for key in self._streams:
            for x in self._streams[key]:
                map_x = map_function(x)
                if isinstance(map_x, list):
                    raise StreamError(
                        "A map function must return a single element per processed element."
                    )
                result._add_element(key, map_x)
        return result

    def flat_map(self, flat_map_function: Callable[[Any], list[Any]]) -> KeyedStream:
        """Perform a `flat_map_function` on the stream.

        A `flat_map_function` creates zero, one, or multiple elements per
        input element. Note that the output of the `flat_map_function` has to be of
        type list. Therefore, if `flat_map_function` creates zero elements return an
        empty list `[]`.
        """
        result = KeyedStream()
        for key in self._streams:
            for x in self._streams[key]:
                flat_map_x = flat_map_function(x)
                if not isinstance(flat_map_x, list):
                    raise StreamError(
                        "A flat_map function must return a list of elements per "
                        "processed element. Such lists may contain zero, one, or more "
                        "elements."
                    )
                result._add_elements(key, flat_map_x)
        return result

    def filter(self, filter_function: Callable[[Any], bool]) -> KeyedStream:
        """Perform a `filter_function` on the stream.

        A `filter_function` evaluates a boolean predicate for each element and returns
        those for which the function is true.
        """
        result = KeyedStream()
        for key in self._streams:
            for x in self._streams[key]:
                filter_x = filter_function(x)
                if not isinstance(filter_x, bool):
                    raise StreamError(
                        "A filter function must return a single boolean value per "
                        "processed element."
                    )
                if filter_x:
                    result._add_element(key, x)
        return result

    def reduce(self, reduce_function: Callable[[Any, Any], Any]) -> KeyedStream:
        """Perform a `reduce_function` on the stream.

        A `reduce_function` combines the current element with the last reduced value and
        outputs the result. Note that the output of the `reduce_function` has to be of
        the same type (and structure, in case of tuples) as the input values.
        """
        result = KeyedStream()

        for key in self._streams:
            first = True
            reduce_x = None

            for x in self._streams[key]:
                if first:
                    first = False
                    reduce_x = x
                else:
                    reduce_x = reduce_function(reduce_x, x)
                if isinstance(reduce_x, list):
                    raise StreamError(
                        "A reduce function must return a single element per processed element."
                    )
                if not isinstance(reduce_x, type(x)):
                    raise StreamError(
                        "The output of the reduce_function has to be of the "
                        "same type as the input values."
                    )
                if isinstance(reduce_x, tuple) and len(reduce_x) != len(x):
                    raise StreamError(
                        "The output of the reduce_function, when dealing with tuples, "
                        "has to be of the same structure as the input values "
                        "(i.e., len(reduce_x) == len(x))."
                    )
                result._add_element(key, reduce_x)
        return result


class TimedStream(StreamBase):
    """An extension of a basic `DataStream`, where each element has a time stamp."""

    _timestamps: list[float]

    def __init__(self) -> None:
        """Create an empty `TimedStream`."""
        super().__init__()
        self._timestamps = []

    def __eq__(self, other: object) -> bool:
        """Check if two `TimedStream` objects are equal."""
        if isinstance(other, TimedStream):
            return (self._stream == other._stream) and (self._timestamps == other._timestamps)
        return False

    def __iter__(self) -> Iterator[Any]:
        """Iterate over the stream."""
        yield from self._stream

    def __str__(self) -> str:
        """Return a string representation of the stream."""
        return f"TimedStream({list(zip(self._stream, self._timestamps, strict=True))})"

    def _add_element(self, element: Any, timestamp: float) -> None:
        """Add a value to the stream."""
        if isinstance(element, list):
            raise StreamError("Got multiple elements to add, use `add_elements` instead.")
        if not isinstance(timestamp, float):
            raise StreamError("Timestamps must be encoded as floats representing seconds.")
        if len(self._timestamps) > 0 and self._timestamps[-1] > timestamp:
            raise StreamError(
                "Our API does not support out-of-order elements. Make sure "
                "that the timestamps are always increasing."
            )
        self._timestamps.append(timestamp)
        self._stream.append(element)

    def _add_elements(self, collection: list[Any], timestamps: list[float]) -> None:
        """Add multiple values to the stream."""
        if len(collection) != len(timestamps):
            raise StreamError(
                "Each element in a TimedStream needs a timestamp. Make sure that "
                "the collection of elements and the timestamps are equally long."
            )
        for x in collection:
            if isinstance(x, list):
                raise StreamError(
                    "Stream elements cannot be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )
        self._stream.extend(collection)

        for t in timestamps:
            if not isinstance(t, float):
                raise StreamError("Timestamps must be encoded as floats representing seconds.")
            if len(self._timestamps) > 0 and self._timestamps[-1] > t:
                raise StreamError(
                    "Our API does not support out-of-order elements. Make sure "
                    "that the timestamps are always increasing."
                )
            self._timestamps.append(t)

    def from_collection(self, collection: list[Any], timestamps: list[float]) -> TimedStream:
        """Initialize a `TimedStream` with values from a list.

        Can only be used on empty streams.

        Args:
            collection: list of values (values must not be of type list)
            timestamps: list of timestamps (floats of increasing value)
        """
        if len(self._stream) > 0:
            raise StreamError(
                "This data stream already contains elements. Use the method "
                "`add_elements` if you really want to insert these elements."
            )
        if not isinstance(collection, list) or not isinstance(timestamps, list):
            raise StreamError(
                "collection and timestamps must be of type list, "
                f"got {type(collection)} and {type(timestamps)}."
            )
        if len(collection) != len(timestamps):
            raise StreamError(
                "Each element in the TimedStream needs a timestamp. Make sure that "
                "the collection of elements and the timestamp list are equally long."
            )
        for x in collection:
            if isinstance(x, list):
                raise StreamError(
                    "Stream elements must not be of type list. "
                    "To add elements with multiple values, use tuples instead."
                )

        self._stream = collection.copy()
        for t in timestamps:
            if not isinstance(t, float):
                raise StreamError("Timestamps must be encoded as floats representing seconds.")
            if len(self._timestamps) > 0 and self._timestamps[-1] > t:
                raise StreamError(
                    "Our API does not support out-of-order elements. Make sure "
                    "that the timestamps are always increasing."
                )
            self._timestamps.append(t)
        return self

    def from_csv(self, path: str, start: int | None = None, end: int | None = None) -> TimedStream:
        """Initialize a `TimedStream` with values from a CSV file.

        Each row in the CSV file should have at least two values, where the last value
        must always represent the timestamp as a float.
        Can only be used on empty streams.

        Args:
            path: location of a CSV file to load
            start: index of the first row to be added (defaults to first line)
            end: index of the last row to be added (defaults to last line)
        """
        if len(self._stream) > 0:
            raise StreamError(
                "This data stream already contains elements. Use the method "
                "`add_elements` if you really want to insert these elements."
            )
        if path[-4:] != ".csv":
            raise StreamError("Only CSV files are supported.")

        if start is None:
            start = 0
        with Path(path).open(encoding="utf-8") as f:
            reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
            for i, row in enumerate(reader):
                if end is not None and i > end:
                    break
                if i >= start:
                    if len(row) < 2 or not isinstance(row[-1], float):  # noqa: PLR2004
                        raise StreamError(
                            "Each row should have at least two values to create a "
                            "TimedStream, where the last value always represents the "
                            "timestamp as a float."
                        )
                    if len(row) > 2:  # noqa: PLR2004
                        self._stream.append(tuple(row[:-1]))
                    elif len(row) == 2:  # noqa: PLR2004
                        self._stream.append(row[0])
                    self._timestamps.append(row[-1])
        return self

    def map(self, map_function: Callable[[Any], Any]) -> TimedStream:
        """Perform a `map_function` on the stream.

        A `map_function` creates exactly one output element per input element.
        """
        result = TimedStream()
        for i, x in enumerate(self._stream):
            map_x = map_function(x)
            if isinstance(map_x, list):
                raise StreamError(
                    "A map function must return a single element per processed element."
                )
            result._add_element(map_x, self._timestamps[i])
        return result

    def flat_map(self, flat_map_function: Callable[[Any], list[Any]]) -> TimedStream:
        """Perform a `flat_map_function` on the stream.

        A `flat_map_function` creates zero, one, or multiple elements per
        input element. Note that the output of the `flat_map_function` has to be of
        type list. Therefore, if `flat_map_function` creates zero elements return an
        empty list `[]`.
        """
        result = TimedStream()
        for i, x in enumerate(self._stream):
            flat_map_x = flat_map_function(x)
            if not isinstance(flat_map_x, list):
                raise StreamError(
                    "A flat_map function must return a list of elements per processed "
                    " element. Such list may contain zero, one, or more elements."
                )
            result._add_elements(flat_map_x, len(flat_map_x) * [self._timestamps[i]])
        return result

    def filter(self, filter_function: Callable[[Any], bool]) -> TimedStream:
        """Perform a `filter_function` on the stream.

        A `filter_function` evaluates a boolean predicate for each element and returns
        those for which the function is true.
        """
        result = TimedStream()
        for i, x in enumerate(self._stream):
            filter_x = filter_function(x)
            if not isinstance(filter_x, bool):
                raise StreamError(
                    "A filter function must return a single boolean value per processed element."
                )
            if filter_x:
                result._add_element(x, self._timestamps[i])
        return result

    def reduce(self, reduce_function: Callable[[Any, Any], Any]) -> TimedStream:
        """Perform a `reduce_function` on the stream.

        A `reduce_function` combines the current element with the last reduced value and
        outputs the result. Note that the output of the `reduce_function` has to be of
        the same type (and structure, in case of tuples) as the input values.
        """
        result = TimedStream()
        reduce_x = None

        for i, x in enumerate(self._stream):
            reduce_x = x if i == 0 else reduce_function(reduce_x, x)
            if isinstance(reduce_x, list):
                raise StreamError(
                    "A reduce function must return a single element per processe element."
                )
            if not isinstance(reduce_x, type(x)):
                raise StreamError(
                    "The output of the reduce_function has to be of the "
                    "same type as the input values."
                )
            if isinstance(reduce_x, tuple) and len(reduce_x) != len(x):
                raise StreamError(
                    "The output of the reduce_function, when dealing with tuples, "
                    "has to be of the same structure as the input values "
                    "(i.e., len(reduce_x) == len(x))."
                )
            result._add_element(reduce_x, self._timestamps[i])
        return result

    def key_by(self, key_by_function: Callable[[Any], Any]) -> KeyedStream:
        """Convert the stream into a `KeyedStream` based on a `key_by_function`.

        A `key_by_function` divides a stream into disjoint partitions. All records with
        the same key are assigned to one partition.
        """
        result = KeyedStream()
        for x in self._stream:
            key_x = key_by_function(x)
            if isinstance(key_x, list):
                raise StreamError(
                    "A reduce function must return a single element per processed element."
                )
            result._add_element(key_x, x)
        return result

    @_requires_non_empty
    def landmark_tuple_window(self, size: int) -> WindowedStream:
        """Discretize the stream with tuple-based landmark windows."""
        if not isinstance(size, int) or size < 1:
            raise StreamError("The window size must be an integer and greater than 0.")
        windowed_stream = WindowedStream()
        window = []
        for i, x in enumerate(self._stream):
            window.append(x)
            if len(window) % size == 0:
                windowed_stream._add_new_window(window, 0, i)
        return windowed_stream

    @_requires_non_empty
    def tumbling_tuple_window(self, size: int) -> WindowedStream:
        """Discretize the stream with tuple-based tumbling windows."""
        if not isinstance(size, int) or size < 1:
            raise StreamError("The window size must be an integer and greater than 0.")
        windowed_stream = WindowedStream()
        window = []
        for i, x in enumerate(self._stream):
            window.append(x)
            if len(window) == size:
                windowed_stream._add_new_window(window, i + 1 - size, i)
                window = []
        return windowed_stream

    @_requires_non_empty
    def sliding_tuple_window(self, size: int, slide: int) -> WindowedStream:
        """Discretize the stream with tuple-based sliding windows."""
        if not isinstance(size, int) or size < 1 or slide < 1 or size <= slide:
            raise StreamError(
                "The window size and slide must be integers, greater than 0, and slide "
                "must be smaller than size."
            )
        windowed_stream = WindowedStream()
        windows: list[list[Any]] = [[]]
        slide_count = 0
        remove_head = False
        for i, x in enumerate(self._stream):
            if slide_count == slide:
                windows.append([])
                slide_count = 1
            else:
                slide_count += 1
            for window in windows:
                window.append(x)
                if len(window) == size:
                    windowed_stream._add_new_window(window, i + 1 - size, i)
                    remove_head = True
            if remove_head:
                windows.pop(0)
                remove_head = False
        return windowed_stream

    @_requires_non_empty
    def landmark_time_window(self, size_t: float) -> WindowedStream:
        """Discretize the stream with time-based landmark windows."""
        if not isinstance(size_t, numbers.Real) or size_t <= 0.0:
            raise StreamError(
                "The window size must be a number representing seconds and greater than 0."
            )
        windowed_stream = WindowedStream()
        window: list[Any] = []
        start = self._timestamps[0]
        step = 1
        for i, x in enumerate(self._stream):
            if (self._timestamps[i] - start) / size_t >= step:
                windowed_stream._add_new_window(window, start, start + (size_t * step))
                step += 1
            window.append(x)
        if len(window) > 0:
            windowed_stream._add_new_window(window, start, start + (size_t * step))
        return windowed_stream

    @_requires_non_empty
    def tumbling_time_window(self, size_t: float) -> WindowedStream:
        """Discretize the stream with time-based tumbling windows."""
        if not isinstance(size_t, numbers.Real) or size_t <= 0.0:
            raise StreamError(
                "The window size must be a number representing seconds and greater than 0."
            )
        windowed_stream = WindowedStream()
        window: list[Any] = []
        window_end = self._timestamps[0] + size_t
        for i, x in enumerate(self._stream):
            if self._timestamps[i] >= window_end:
                windowed_stream._add_new_window(window, window_end - size_t, window_end)
                window_end += size_t
                window = []
            window.append(x)
        if len(window) > 0:
            windowed_stream._add_new_window(window, window_end - size_t, window_end)
        return windowed_stream

    @_requires_non_empty
    def sliding_time_window(self, size_t: float, slide_t: float) -> WindowedStream:
        """Discretize the stream with time-based sliding windows."""
        if (
            not isinstance(size_t, numbers.Real)
            or not isinstance(slide_t, numbers.Real)
            or size_t <= 0.0
            or slide_t <= 0.0
            or size_t <= slide_t
        ):
            raise StreamError(
                "The window size and slide must be numbers representing seconds, "
                "greater than 0, and slide must be smaller than size."
            )
        windowed_stream = WindowedStream()
        windows: list[list[Any]] = [[]]
        window_end = self._timestamps[0] + size_t
        next_slide = self._timestamps[0] + slide_t
        remove_head = False
        for i, x in enumerate(self._stream):
            if self._timestamps[i] >= next_slide:
                windows.append([])
                next_slide += slide_t
            for window in windows:
                if self._timestamps[i] >= window_end:
                    windowed_stream._add_new_window(window, window_end - size_t, window_end)
                    remove_head = True
                    window_end += slide_t
                window.append(x)
            if remove_head:
                windows.pop(0)
                remove_head = False
        if len(windows[0]) > 0:
            windowed_stream._add_new_window(windows[0], window_end - size_t, window_end)
        return windowed_stream


class WindowedStream(StreamBase):
    """A discretized `DataStream` that is split based on a windowing function."""

    _window_starts: list[float]
    _window_ends: list[float]

    def __init__(self) -> None:
        """Create an empty `WindowedStream`."""
        super().__init__()
        self._window_starts = []
        self._window_ends = []

    def __eq__(self, other: object) -> bool:
        """Check if two `WindowedStream` objects are equal."""
        if isinstance(other, WindowedStream):
            return (
                (self._stream == other._stream)
                and (self._window_starts == other._window_starts)
                and (self._window_ends == other._window_ends)
            )
        return False

    def __str__(self) -> str:
        """Return a string representation of the stream."""
        s = "WindowedStream([\n"
        for i, window in enumerate(self._stream):
            s += f"\tstart({self._window_starts[i]}) {window} end({self._window_ends[i]}),\n"
        s = s[:-2]
        s += "\n])"
        return s

    def _add_new_window(self, window: list[Any], start: float, end: float) -> None:
        if not isinstance(window, list):
            raise StreamError("Windows are internally represented as lists.")
        self._stream.append(window.copy())
        self._window_starts.append(start)
        self._window_ends.append(end)

    def aggregate(self, agg: Literal["count", "sum", "min", "max", "mean"]) -> DataStream:  # noqa: C901
        """Perform an aggregation function on each window of the stream.

        For every aggregation function except `count`, the input stream must consist of
        scalar numeric elements. If your stream consists of composite elements (e.g.,
        tuples), consider using `apply` or performing a map projetion on the stream.

        The result is a new `DataStream` containing one tuple per window, where the
        first value in the tuple is the aggregate, the second is the window start, and
        the third is the window end (i.e., `(aggregate, window_start, window_end)`).
        The aggregate function must be `count`, `sum`, `min`, `max`, or `mean`.

        For empty windows, `aggregate` will be `0` for `count` and `None` for any other
        aggregation`.
        """
        if not isinstance(agg, str) or agg not in [
            "count",
            "sum",
            "min",
            "max",
            "mean",
        ]:
            raise StreamError(
                "You must pass one of the following values for `agg`: count, sum, min, max, mean."
            )

        result = DataStream()
        for i, window in enumerate(self._stream):
            window_agg = None
            if agg == "count":
                window_agg = len(window)
            else:
                if not all(isinstance(element, Number) for element in window):
                    raise StreamError(
                        "Values for all aggregations but count must be numeric. "
                        f"Encountered non-numeric element in window {window}."
                    )

                if len(window) > 0:
                    window_array = np.asarray(window)
                    try:
                        if agg == "sum":
                            window_agg = window_array.sum()
                        elif agg == "min":
                            window_agg = window_array.min()
                        elif agg == "max":
                            window_agg = window_array.max()
                        elif agg == "mean":
                            window_agg = window_array.mean()
                    except ValueError as e:
                        raise StreamError(
                            f"A window could not be aggregated using {agg}. "
                            "You must ensure that all elements are aggregable by this function."
                        ) from e

            result._add_element((window_agg, self._window_starts[i], self._window_ends[i]))
        return result

    def reduce(self, reduce_function: Callable[[Any, Any], Any]) -> DataStream:
        """Perform a `reduce_function` on each window of the stream.

        The result is a new `DataStream` containing one tuple per window, where the
        first value in the tuple is the reduced element, the second is the window start,
        and the third is the window end (i.e., `(reduced_element, window_start,
        window_end)`).
        A `reduce_function` combines the current element with the last reduced value and
        outputs the result. Note that the output of the `reduce_function` has to be of
        the same type (and structure, in case of tuples) as the input values.

        For empty windows, `reduced_element` will be `None`.
        """
        result = DataStream()

        for i, window in enumerate(self._stream):
            first = True
            window_reduce = None

            for x in window:
                if first:
                    first = False
                    window_reduce = x
                else:
                    window_reduce = reduce_function(window_reduce, x)
                if isinstance(window_reduce, list):
                    raise StreamError(
                        "A reduce function must return a single element per processed element."
                    )
                if not isinstance(window_reduce, type(x)):
                    raise StreamError(
                        "The output of the reduce_function has to be of the "
                        "same type as the input values."
                    )
                if isinstance(window_reduce, tuple) and len(window_reduce) != len(x):
                    raise StreamError(
                        "The output of the reduce_function, when dealing with tuples, "
                        "has to be of the same structure as the input values "
                        "(i.e., len(reduce_x) == len(x))."
                    )
            result._add_element((window_reduce, self._window_starts[i], self._window_ends[i]))
        return result

    def apply(self, apply_function: Callable[[list[Any]], Any]) -> DataStream:
        """Perform an arbitrary apply function on the stream.

        An apply function must take a window (i.e., list) as input and produce a single
        output element per window. The result is a new `DataStream` containing one tuple
        per window, where the first value in the tuple is the function's result, the
        second is the window start, and the third is the window end (i.e.,
        `(function_result, window_start, window_end)`).

        Note that `apply` is the most generic operator for `WindowedStream`s that could
        be used to implement more specific methods, such as `reduce` or `aggregate`.
        As the most versatile operator, `apply_function` must handle the case of empty
        windows itself.
        """
        result = DataStream()

        for i, window in enumerate(self._stream):
            window_result = apply_function(window)
            if isinstance(window_result, list):
                raise StreamError(
                    "An apply function must return a single element per processed window."
                )
            result._add_element((window_result, self._window_starts[i], self._window_ends[i]))
        return result


class StreamError(Exception):
    """An error caused by wrong usage of a data stream."""


def _check_element_structure(got: Any, expected: Any, str_expected: str) -> bool:
    if not isinstance(got, type(expected)):
        print(
            "The data type of the elements in your output do not match the "
            f"expected type. Expected {type(expected)} but got {type(got)}."
        )
        return False
    if isinstance(got, tuple) and len(got) != len(expected):
        print(
            "The datatype of the elements in your output stream match the expected type (tuple).\n"
            "However, the structure in your tuples is wrong. Expected something like "
            f"{str_expected} but got tuples like {got}."
        )
        return False
    return True


def _check_element_structure_in_stream(stream: Any, expected: Any, str_expected: str) -> None:
    print(
        f"Expected element structure in output stream: {str_expected}\n"
        "Checking element structure of output elements...\n"
    )
    if isinstance(stream, KeyedStream):
        for key in stream._streams:
            for x in stream._streams[key]:
                if not _check_element_structure(x, expected, str_expected):
                    return
    elif isinstance(stream, StreamBase):
        for x in stream._stream:
            if not _check_element_structure(x, expected, str_expected):
                return
    elif isinstance(stream, WindowedStream):
        print("Your output stream is a WindowedStream, which was not expected.")
        return
    else:
        print(f"The output of your function is not a stream but a {stream}.")
        return

    print("Test finished successfully.")
