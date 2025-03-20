"""This module defines different data structures for summaries over data streams."""

from __future__ import annotations

import hashlib
from ctypes import c_int32
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray

__all__ = ["BloomFilter", "CountMinSketch", "H3HashFunctions", "ReservoirSample"]

MAX_INT = 2**32 - 1


def _int32(val: Any) -> int:
    """Hash an arbitrary value into a 32-bit integer."""
    if isinstance(val, int) and -MAX_INT <= val <= MAX_INT:
        return val

    if isinstance(val, str):
        # Generate a consistent hash value for the string
        hash_value = int(hashlib.sha256(val.encode()).hexdigest(), 16) % (2**31 - 1) - 2**31
    else:
        hash_value = abs(hash(val))

    if -MAX_INT <= hash_value <= MAX_INT:
        return hash_value
    return c_int32(hash_value).value


class H3HashFunctions:
    """A collection of hash functions from the H3 hash family."""

    n_functions: int
    seed: int
    limit: int
    q_matrices: NDArray[np.int32]
    _rng: np.random.Generator

    def __init__(
        self,
        n_functions: int,
        limit: int,
        seed: int = 42,
        json_dict: dict[str, Any] | None = None,
    ) -> None:
        """Create a collection of H3 hash functions.

        Args:
            n_functions: number of functions
            limit: largest number a hash function can map to
            seed: state of the internal random number generator
            json_dict: optional checkpoint file that overwrites all other parameters
        """
        if json_dict is None:
            self.n_functions = n_functions
            self.seed = seed
            self.limit = limit
            self._rng = np.random.default_rng(seed)

            ii32 = np.iinfo(np.int32)
            self.q_matrices = self._rng.integers(
                ii32.min, ii32.max, size=(n_functions, 32), dtype=np.int32
            )
        else:
            self.n_functions = json_dict["n_functions"]
            self.limit = json_dict["limit"]
            self.q_matrices = np.asarray(json_dict["q_matrices"])

    def __str__(self) -> str:
        """Return a string representation of the `H3HashFunctions`."""
        return (
            "H3HashFunctions\nn_functions = "
            + str(self.n_functions)
            + "\nlimit = "
            + str(self.limit)
            + "\nq_matrices = "
            + str(self.q_matrices)
        )

    def hash(self, inp: Any) -> NDArray[np.int32]:
        """Hash an arbitrary input with each function in `self.q_matrices`."""
        inp = _int32(inp)
        if inp == 0:
            inp = 2**32 - 1
        result = np.zeros(self.n_functions, dtype=np.int32)
        inp_copy = inp
        for i in range(self.n_functions):
            current = 0
            for k in range(32):
                if inp_copy == 0:
                    break
                current = current ^ ((1 & inp_copy) * self.q_matrices[i][k])
                inp_copy >>= 1
            if current < 0:
                current = -1 * current
            if self.limit > 0:
                result[i] = int(current % self.limit)
            else:
                result[i] = int(current)
            inp_copy = inp
        return result


class CountMinSketch:
    """A basic implementation of a Count-Min sketch."""

    _depth: int
    _width: int
    _hash_functions: H3HashFunctions
    _counters: NDArray[np.int32]

    def __init__(self, width: int, depth: int, seed: int = 0) -> None:
        """Create a new `CountMinSketch`.

        Args:
            width: width of the sketch (>= 1)
            depth: depth of the sketch (>= 1)
            seed: random state of the internal hash functions
        """
        if not isinstance(depth, int) or depth < 1:
            raise SynopsisError(
                "To construct a CountMinSketch, the depth must be of type int and larger than 0."
            )
        if not isinstance(width, int) or width < 1:
            raise SynopsisError(
                "To construct a CountMinSketch, the width must be of type int and larger than 0."
            )

        self._width = width
        self._depth = depth
        self._hash_functions = H3HashFunctions(depth, width, seed)
        self._counters = np.zeros((self._depth, self._width), dtype=np.int32)

    def __str__(self) -> str:
        """Return a string representation of the `CountMinSketch`."""
        return (
            "Count-Min Sketch\ndepth = "
            + str(self._depth)
            + " width = "
            + str(self._width)
            + "\n"
            + str(self._counters)
        )

    def get_depth(self) -> int:
        """Return the depth (i.e., number of rows) of the sketch."""
        return self._depth

    def get_hash_functions(self) -> H3HashFunctions:
        """Return the hash functions of the sketch."""
        return self._hash_functions

    def get_counting_matrix(self) -> NDArray[np.int32]:
        """Return the counting matrix of the sketch (mainly useful for debugging)."""
        return self._counters.copy()

    def update(self, element: Any) -> None:
        """Update the sketch with an arbitrary input element.

        The function hashes `element` for each row using an independent hash-function,
        updating one index per row in the `CountMinSketch`.
        """
        hash_values = self._hash_functions.hash(element)
        for i, hash_val in enumerate(hash_values):
            self._counters[i][hash_val] += 1

    def query(self, element: Any) -> int:
        """Return an approximate count of how often `element` appears in the sketch."""
        hash_values = self._hash_functions.hash(element)
        result = 2**32 - 1
        for i, hash_val in enumerate(hash_values):
            result = min(result, self._counters[i][hash_val])
        return result


class BloomFilter:
    """A basic implementation of a bloom filter."""

    _n_bits: int
    _n_hash_functions: int
    _hash_functions: H3HashFunctions
    _bitmap: NDArray[np.int32]

    def __init__(self, n_bits: int, n_hash_functions: int, seed: int = 0) -> None:
        """Create a new `BloomFilter`.

        Args:
            n_bits: length of the bitmap per hash function (>= 1)
            n_hash_functions: number of hash functions (>= 1)
            seed: random state of the internal hash functions
        """
        if not isinstance(n_bits, int) or n_bits < 1:
            raise SynopsisError(
                "To construct a BloomFilter, the number of bits must be of type int "
                "and larger than 0."
            )
        if not isinstance(n_hash_functions, int) or n_hash_functions < 1:
            raise SynopsisError(
                "To construct a BloomFilter, the number of hash functions must be of "
                "type int and larger than 0."
            )

        self._n_bits = n_bits
        self._n_hash_functions = n_hash_functions
        self._hash_functions = H3HashFunctions(n_hash_functions, n_bits, seed)
        self._bitmap = np.zeros((self._n_bits), dtype=np.int32)

    def __str__(self) -> str:
        """Return a string representation of the `BloomFilter`."""
        return (
            "BloomFilter\nnumber of bits = "
            + str(self._n_bits)
            + " number of hash functions = "
            + str(self._n_hash_functions)
            + "\n"
            + str(self._bitmap)
        )

    def get_bitmap(self) -> NDArray[np.int32]:
        """Return the bitmap of the `BloomFilter`."""
        return self._bitmap.copy()

    def get_hash_functions(self) -> H3HashFunctions:
        """Return the hash functions of the bloom filter."""
        return self._hash_functions

    def update(self, element: Any) -> None:
        """Update the bloom filter with an arbitrary input element.

        The function hashes `element` `n_hash_functions` times. The bits of each
        respective bitmap are set to one at the hashed indexes (if they are not already
        set to one).
        """
        hash_values = self._hash_functions.hash(element)
        for hash_val in hash_values:
            self._bitmap[hash_val] = 1

    def query(self, element: Any) -> bool:
        """Approximate whether `element` appears in the `BloomFilter`.

        A `BloomFilter` approximates whether an `element` is not contained in a set.
        If it is not contained in the set, `query` always returns `False`. If it returns
        `True`, the `element` is _potentially_ contained in the set.
        """
        hash_values = self._hash_functions.hash(element)
        return all(self._bitmap[hash_val] != 0 for hash_val in hash_values)


class ReservoirSample:
    """A basic implementation of a reservoir sample."""

    _sample: list[Any]
    _sample_size: int
    _processed_elements: int
    _rng: np.random.Generator

    def __init__(self, sample_size: int, seed: int = 0) -> None:
        """Create a new `ReservoirSample`.

        Args:
            sample_size: size of the sample (>= 1)
            seed: state of the internal random number generator
        """
        if not isinstance(sample_size, int) or sample_size < 1:
            raise SynopsisError(
                "To construct a ReservoirSample, the sample size must be of type int "
                "and larger than 0."
            )
        self._sample = []
        self._sample_size = sample_size
        self._processed_elements = 0
        self._rng = np.random.default_rng(seed)

    def __str__(self) -> str:
        """Return a string representation of the `ReservoirSample`."""
        return f"ReservoirSample\nsample size = {self._sample_size}\n{self._sample}"

    def get_sample(self) -> list[Any]:
        """Return a copy of the current reservoir sample."""
        return self._sample.copy()

    def get_sample_size(self) -> int:
        """Return the size of the `ReservoirSample`."""
        return self._sample_size

    def get_processed_elements(self) -> int:
        """Return the number of previously processed elements."""
        return self._processed_elements

    def update(self, element: Any, debug: bool = False) -> None:
        """Update the `ReservoirSample`.

        If the `sample` is not yet fully filled, the element is simply inserted. If the
        `sample` buffer is already full, a random number between 0 and 1 is generated
        and compared to the fraction of the sample size over the number of previously
        observed elements. If the random number is smaller, a random index within the
        bounds of the sample buffer is generated and the element at this location is
        replaced.

        Args:
            element: arbitrary input element
            debug: optional parameter for additional print logs during the update
        """
        if self._processed_elements < self._sample_size:
            self._processed_elements += 1
            self._sample.append(element)
        else:
            self._processed_elements += 1
            rand_num = self._rng.random()
            if debug:
                print("Random number: ", rand_num)
                print(
                    "Fraction (Sample size / Number of processed elements) = ",
                    float(self._sample_size) / float(self._processed_elements),
                )
            if rand_num < (float(self._sample_size) / float(self._processed_elements)):
                index = self._rng.integers(0, self._sample_size)
                if debug:
                    print("Index: ", index)
                self._sample[index] = element


class SynopsisError(Exception):
    """An error caused by wrong usage of a synopsis."""
