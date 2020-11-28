import sys
import math

from int_overflow import int_overflow


def get_diff(i, nums, m):
    # diff[0] = x1 - x0 (mod m)
    diff = nums[i + 1] - nums[i]
    if diff < 0:
        diff += m
    return diff


def get_diff_list(sample, m):
    diff = list()
    for i in range(0, len(sample) - 1):
        diff.append(get_diff(i, sample, m))
    return diff


def calc_observed_diffs_list(diffs, a, m):
    return [(a * diff) % m for diff in diffs]


def modular_inverse(num, mod):
    return pow(num, -1, mod=mod)


def calc_c_value(x, xnext, a, m):
    mult_mod = (a * x) % m
    left = m - mult_mod
    c = (left + xnext) % m
    return c 


def crack(sample, max_m, min_m=0):
    for m in range(min_m, max_m):
        diffs = get_diff_list(sample, m)

        try:
            inv = modular_inverse(diffs[0], m)
        except ValueError:
            continue

        a = (diffs[1] * inv) % m

        obs_diffs = calc_observed_diffs_list(diffs, a, m)

        if (diffs[1:] == obs_diffs[:-1]):
            c = calc_c_value(sample[0], sample[1], a, m)
            return a, c, m

    return None, None, None


def get_generator(seed, a, c, m):
    prev = seed
    while True:
        cur = math.fmod(int_overflow(a*prev + c), m)
        yield int(cur)
        prev = cur