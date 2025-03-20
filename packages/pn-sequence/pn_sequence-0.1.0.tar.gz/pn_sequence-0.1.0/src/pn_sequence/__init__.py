"""
This module contains the functions for testing pseudo-noise (PN) sequences according to Golomb's randomness postulates.
"""


def is_first_postulate_true(sequence):
    """Tests whether the sequence satisfies the first postulate

    In the cycle s^N of s, the number of 1's differs from the number of 0's by at most 1.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the first postulate
    """
    z = sequence.count("0")
    o = sequence.count("1")

    if abs(z - o) > 1:
        return False

    return True


def is_second_postulate_true(sequence):
    """Tests whether the sequence satisfies the second postulate

    In the cycle, at least half the runs have length 1, at least one-fourth have length 2,
    at least one-eighth have length 3, etc., as long as the number of runs so indicated exceeds 1.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the second postulate
    """
    streaks = __get_streaks(sequence)
    strnum = list(streaks)

    if streaks:
        for i in range(0, len(strnum) - 1):
            if abs(strnum[i] - strnum[i + 1]) != 1:
                return False
            if len(streaks[strnum[i]]) != 2 * len(streaks[strnum[i + 1]]):
                if len(streaks[strnum[i]]) != 1 and len(streaks[strnum[i + 1]]) != 1:
                    return False
        return True

    return False


def is_third_postulate_true(sequence):
    """Tests whether the sequence satisfies the second postulate

    The autocorrelation function C(t) is two-valued.
    (Menezes, Van Oorschot and Vanstone, 2018)

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence satisfies the second postulate
    """
    sequence2 = sequence[1:] + sequence[:1]
    hamm_dist = _hamming_distance(sequence, sequence2)

    for i in range(2, len(sequence) - 1):
        sequence2 = sequence[i:] + sequence[:i]
        if hamm_dist != _hamming_distance(sequence, sequence2):
            return False

    return True


def is_pn_sequence(sequence):
    """A shorthand method to test if the sequence is a pseudo-noise sequence,
    satisfying all three postulates.

    Args:
        sequence: A string with a binary sequence to be tested.
    Returns:
        bool: Whether the sequence is a pseudo-noise (pn) sequence.

    """
    if is_first_postulate_true(sequence) and is_second_postulate_true(sequence) and is_third_postulate_true(sequence):
        return True

    return False


def __get_streaks(sequence):
    streaks = {}
    streak = 1
    i = 0

    while sequence[0] == sequence[len(sequence) - 1]:
        if i > len(sequence):
            return {}
        sequence = sequence[1:] + sequence[0]
        i += 1

    if sequence[len(sequence) - 1] == "1":
        sequence += "0"
    else:
        sequence += "1"

    for i in range(0, len(sequence) - 1):
        if sequence[i] == sequence[i + 1]:
            streak += 1
        else:
            try:
                streaks[streak].append(i)
            except:
                streaks[streak] = [i]
            streak = 1

    return streaks


def _hamming_distance(s1, s2):
    distance = 0
    for i, j in zip(s1, s2):
        if i != j:
            distance += 1

    return distance
