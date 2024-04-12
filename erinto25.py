#!/usr/bin/env python3
# This is a Python 3 code for counting the number of "average" subsets for certain sets
#
# The investigated sets are {1, 2, 3 ... n} - all + integers upto n
# An "average" subset is defined as a subset with at least two members
# where the average of its elements is an integer. 

# Source of the problem (original text in Hungarian):
# https://ematlap.hu/hettusa/1370-hettusa-4-fordulo-2024-marcius
# it is problem 25 there

# Briefly, the problem asks to prove that the number of average subsets
# for the set {1, 2, 3, ..., 100} is even.

# The total number of subsets is 2^100 (or 2^100 - 1 -100 if
# excluding the empty set and subsets containing 1 elements only), investigating each one individually is
# computationally infeasible.

# there is an elagant proof for the original problem, however I was not able to find it, instead I have deiced to compute it

# This code provides an efficient algorithm to calculate the exact
# number of average subsets.
# For comparision/testing my result I also used bruteforce algorithm to for smaller sets, included to this code

# The algorithm has been tested successfully for sets up to 500 elements; the result were compared to the bruteforced result upto n = 34

# During the calculation, intermediate results correspond to known number sequences:
#  * https://oeis.org/A002620
#  * https://oeis.org/A061866
# This code calculates a yet-unlisted sequence.

# I have not documented the details of the algorithm used
# if you do not understand it, it might help to play with different debug levels

# please install numpy using pip, other used libraries are standards nowadays

import argparse
from itertools import combinations
import numpy as np
import sys
global total, l_count, used, count


def generate_subsets(data, k):
    """
    This part of the code is used in brute forcing only
    Generates all k-sized subsets of a set.

    Args:
        data: A set of elements.
        k: The size of the subsets to generate.

    Yields:
        A k-sized subset of the input data.
    """
    if k <= len(data):
        for subset in combinations(data, k):
            yield subset


# processing arguments
parser = argparse.ArgumentParser(
    prog='erinto25.py',
    description='Calculating solutions for erinto 25')
parser.add_argument('-t', '--total', type=int, default=100,
                    help='Integer, the maximum value in the set')
parser.add_argument('-s', '--start', type=int, default=2,
                    help='(deprecated) Currently only supports starting value 2')
parser.add_argument('-d', '--debug', type=int, default=0,
                    help='additional debug information is printed depending on the level')
# use simple bruteforce
parser.add_argument('-b', '--bforce', action='store_true',
                    help='It will not work for large numbers, good for comparisions')
args = parser.parse_args()

if args.start != 2 or args.total < 2:
    raise SystemExit('Start should be 2,  total >= 2 !!!')
args.total += 1  # usually we need this value
if not args.bforce:
    # this preparetion is not needed, when intelligent algorithm is used
    # Initialize results array for storing intermediate and final calculations
    # Use dtype=object to accommodate potentially large values
    ActStepRes = np.zeros((args.total, args.total, args.total), dtype=object)
    # first filling step 2 results manually
    # ActStepRes[Maxlength,modulo,remainder] and PrevStepRes[Maxlength,modulo,remainder]
    # are count of available series so far in different categories as result of previous steps
    # 0 length is not used - just kept for faster indexing
    # First we fill the table
    for modulo in range(2, args.total):
        ActStepRes[1][modulo][1] += 1

PoweOf2 = 4
for step in range(2, args.total):
    step1 = step+1
    count = 0
    if args.bforce:
        test_set = set(range(1, step1))
        debug = args.debug
        for i in range(args.start, step1):
            test_count = 0
            for subset in generate_subsets(test_set, i):
                s = 0
                for j in range(i):
                    s += subset[j]
                if s % i == 0:
                    if debug:
                        print(subset)
                    test_count += 1
            print(f'count={test_count} for {i} elements of {step}')
            count += test_count
        sys.stdout.flush()
    else:
        # make a copy of current result (initialized earlier) to previous result
        PrevStepRes = ActStepRes.copy()
        if args.debug >= 6:
            print(f'ActStepRes in step {step} after copy')
            print(ActStepRes)
        # categorizing the new series generated from the old ones
        # each previous series just can be extended with the new number resulting additional series in different categories
        for length in range(2, step1):
            for modulo in range(2, args.total):
                for result in range(modulo):
                    # inc variable can be optimized out by joing the two lines below, kept this way for debugging
                    inc = PrevStepRes[length-1][modulo][(result-step) % modulo]
                    ActStepRes[length][modulo][result] += inc
        if args.debug >= 5:
            print(f'ActStepRes in step {step} after extending previous series')
            print(ActStepRes)
        # now add the effect of the new 1 length element (step)
        # we should calculate remainder for all modulo used only in the future (see above and below)!
        for modulo in range(2, args.total):
            ActStepRes[1][modulo][step % modulo] += 1
        # we are ready, now calculate the number of AVARAGE set in this step
        for i in range(2, step1):
            test_count = ActStepRes[i][i][0]
            if args.debug >= 1:
                if args.debug == 1:
                    print(f'count={test_count} for {i} elements of {step}')
                elif args.debug >= 3:
                    print(f'step={step}, len={i}')
                    print(ActStepRes[i][i])
            count += test_count
        if args.debug >= 4:
            print(f'ActStepRes in step {step} when finished the step')
            print(ActStepRes)
        if args.debug == 2:
            print('===')
            for length in range(1, step1):
                for modulo in range(2,  args.total):
                    print(
                        f'step={step}, length={length} modulo={modulo} remainders={ActStepRes[length][modulo]}')
                print()

    # to see partial result
    print(f'Max size={step} AVARAGE count={count} %={count*100/PoweOf2:.3f}')
    PoweOf2 *= 2

pass # just for a break point for being able to check globals before exiting
