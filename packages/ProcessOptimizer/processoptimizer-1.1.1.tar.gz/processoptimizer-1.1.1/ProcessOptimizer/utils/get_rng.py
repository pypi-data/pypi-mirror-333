from typing import Union

import numpy as np


def get_random_generator(
    input: Union[int, np.random.RandomState, np.random.Generator, None]
) -> np.random.Generator:
    """Get a random generator from an input.

    Parameters
    ----------
    * `input` [int, float, RandomState instance, Generator instance, or None (default)]:
        Set random state to something other than None for reproducible
        results.

    Returns
    -------
    * `rng`: [Generator instance]
       Random generator.
    """
    if input is None:
        return np.random.default_rng()
    elif isinstance(input, int):
        return np.random.default_rng(input)
    elif isinstance(input, np.random.RandomState):
        return np.random.default_rng(input.randint(1000, size=10))
    # Draws 10 integers under 1000 from the deprecated RandomState to use as a seed for
    # the current RNG. This allows for 10**30 different values.
    elif isinstance(input, np.random.Generator):
        return input
    else:
        raise TypeError(
            "Random state must be either None, an integer, a RandomState instance, or a Generator instance."
        )
