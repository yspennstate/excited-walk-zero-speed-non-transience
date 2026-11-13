"""Exact check, on finite horizons, of the sum over the paths of Pi_c in the proof of Lemma 3.2.

For three cookie stacks on Z^2 and c = 0, 1, 2 it computes the probability that the last visit to
level 0 before level 3 comes at most c steps after time 0, directly and as the sum over short paths
of (path probability) x (probability of then reaching level 3 without returning to level 0), and
checks that the two agree and that dropping the path probabilities gives an upper bound.
old_left = 17 consumes 17 cookies at every site of level -1 and below beforehand."""
import itertools
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def probs(model, i):
    if model == "finite_two":
        beta = 0.8 if i == 1 else -0.8 if i == 2 else 0.0
    elif model == "periodic":
        beta = 0.8 if i % 2 else -0.8
    else:
        beta = 0.8 if (i.bit_length()-1) % 2 == 0 else -0.8
    return [(1+beta)/4, (1-beta)/4, 0.25, 0.25]


def actual(model, horizon, level, c, old_left):
    counts = {}
    def rec(x, y, n, last_zero):
        if x == level:
            return float(last_zero <= c)
        if n == horizon:
            return 0.0
        key = (x,y)
        old = counts.get(key, 0)
        counts[key] = old+1
        total = 0.0
        for (dx,dy), pr in zip(STEPS, probs(model, old+old_left*(x<0)+1)):
            xx, yy = x+dx, y+dy
            total += pr*rec(xx, yy, n+1, n+1 if xx == 0 else last_zero)
        if old:
            counts[key] = old
        else:
            del counts[key]
        return total
    return rec(0,0,0,0)


def prefixes(model, c, old_left):
    for length in range(c+1):
        for directions in itertools.product(range(4), repeat=length):
            x = y = 0
            counts = {}
            weight = 1.0
            for direction in directions:
                old = counts.get((x,y),0)
                weight *= probs(model, old+old_left*(x<0)+1)[direction]
                counts[x,y] = old+1
                dx,dy = STEPS[direction]
                x, y = x+dx, y+dy
            if x == 0:
                yield length, (x,y), counts, weight


def future(model, start, consumed, horizon, level):
    counts = dict(consumed)
    def rec(x,y,n):
        if x == level:
            return 1.0
        if n > 0 and x <= 0:
            return 0.0
        if n == horizon:
            return 0.0
        old = counts.get((x,y),0)
        counts[x,y] = old+1
        total = sum(pr*rec(x+dx,y+dy,n+1)
                    for (dx,dy),pr in zip(STEPS,probs(model,old+1)))
        if old:
            counts[x,y] = old
        else:
            del counts[x,y]
        return total
    return rec(*start,0)


def main():
    started = time.monotonic()
    rows = []
    for model in ["finite_two", "periodic", "blocks"]:
        for old_left in [0,17]:
            for c in [0,1,2]:
                horizon, level = 8, 3
                direct = actual(model,horizon,level,c,old_left)
                factorized = bound = 0.0
                for length,start,consumed,weight in prefixes(model,c,old_left):
                    factorized += weight*future(model,start,consumed,horizon-length,level)
                    bound += future(model,start,consumed,horizon,level)
                assert abs(direct-factorized) < 1e-12, (model,c,old_left,direct,factorized)
                assert direct <= bound+1e-12
                rows.append(dict(model=model, old_left_departures=old_left,c=c,
                    horizon=horizon,level=level,direct_probability=direct,
                    factorized_probability=factorized,unweighted_prefix_bound=bound))
    result = {"cases":rows,"all_passed":True,"elapsed_seconds":time.monotonic()-started,
              "note":"Finite-horizon identities only; the general statement is Lemma 3.2 of the paper."}
    (ROOT/"data/decomposition_checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print(len(rows),"cases passed;",result["elapsed_seconds"],"seconds")


if __name__ == "__main__":
    main()
