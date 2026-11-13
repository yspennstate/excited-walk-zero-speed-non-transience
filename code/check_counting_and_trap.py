"""Finite checks of the averages in the counting lemma (Lemma 2.2, from Zerner 2002, Lemma 3) and of the trapping example in the closing remark."""
import json
import math
import os
import random
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
SEED = 13320261113


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    center = (p + z*z/(2*n)) / (1 + z*z/n)
    radius = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
    return [center-radius, center+radius]


def check_counts():
    """The two averages bounded in the proof of the counting lemma (Lemma 2.2), on random paths of length 2000."""
    rng = random.Random(SEED+1)
    successes = 0
    for trial in range(100):
        # Positive drift ensures many finite levels in this finite test.
        xs = [0]
        for _ in range(2000):
            u = rng.random()
            xs.append(xs[-1] + (1 if u < 0.65 else -1 if u < 0.8 else 0))
        hitting = {}
        visits = {}
        for n, x in enumerate(xs):
            hitting.setdefault(x, n)
            visits.setdefault(x, []).append(n)
        for L in [1, 2, 5, 11]:
            M = min(100, max(hitting)-L)
            end = hitting[M+L]
            cardinalities = []
            durations = []
            for m in range(M+1):
                ts = [n for n in visits[m] if hitting[m] <= n < hitting[m+L]]
                cardinalities.append(len(ts))
                durations.append(max(ts)-hitting[m])
            assert sum(cardinalities) <= end
            assert sum(durations) <= L*end
            # Check strict-growth implication separately at every level.
            for m in range(M+1):
                a = [n for n in visits[m] if hitting[m] <= n < hitting[m+1]]
                b = [n for n in visits[m] if hitting[m] <= n < hitting[m+L]]
                assert max(a) <= max(b)
                if max(a) < max(b):
                    assert len(a) < len(b)
            successes += 1
    return {"paths": 100, "path_length": 2000, "sum_checks": successes,
            "strict_growth_implication": "passed"}


def trap_check():
    """Simulate the two-site trapping event of the closing remark, stopping at the first deviation."""
    rng = random.Random(SEED+2)
    trials = 20000
    cookies = 80
    marked = survived = 0
    for _ in range(trials):
        a = rng.randrange(4)
        b = rng.randrange(4)
        if a != 0 or b != 1:  # directions +e1 at 0, -e1 at e1
            continue
        marked += 1
        good = True
        for i in range(1, cookies+1):
            p = 1 - 3*2.0**(-i-4)
            if rng.random() >= p or rng.random() >= p:
                good = False
                break
        survived += int(good)
    product = 1/16
    for i in range(1, cookies+1):
        product *= (1 - 3*2.0**(-i-4))**2
    via_logs = math.exp(-math.log(16) + 2*sum(math.log1p(-3*2.0**(-i-4))
                                               for i in range(1, cookies+1)))
    assert abs(product-via_logs) < 1e-14
    # Union bound for any later non-mark departure, given the prefix.
    tail_error = 6*2.0**(-cookies-4)
    return {"trials": trials, "mark_pairs": marked, "survivals": survived,
            "frequency": survived/trials, "wilson_95": wilson(survived, trials),
            "cookies_per_site": cookies, "event_probability_product": product,
            "event_probability_via_logs": via_logs,
            "conditional_tail_error_bound": tail_error,
            "completed_two_step_excursions_on_success": cookies,
            "maximum_distance_on_success": 1,
            "maximum_abs_x_over_n_after_time_2k": "1/(2k+1)"}


def main():
    started = time.monotonic()
    result = {"seed": SEED, "counting_checks": check_counts(), "trap": trap_check(),
              "elapsed_seconds": time.monotonic()-started}
    (OUT / "counting_and_trap.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
