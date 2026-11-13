# Zero speed for excited random walks on the event of non-transience

Yitzchak Shmalo

Paper: [paper/main.pdf](paper/main.pdf) (source [paper/main.tex](paper/main.tex)).

## Summary

An excited random walk on Z^d uses, on its i-th visit to a site, the i-th transition probability in a stack
attached to that site; the stacks are i.i.d. over the sites. Kosygina and Zerner (Problem 4.7 of their 2013 survey)
asked whether X_n/n tends to 0 almost surely on the event that |X_n| does not tend to infinity, assuming only that
the stacks are i.i.d. and every transition probability is positive. The paper proves that it does, in every dimension d >= 2
(the case d = 1 is due to Amir, Berger and Orenshtein), with no further restriction on the stacks: they may differ from the simple random walk at infinitely many visits and may push in any direction. If that event has
positive probability, then X_n/n tends to 0 almost surely. The paper also proves the excited random walk form of Zerner's
theorem, the law of large numbers for random walk in i.i.d. random environment (Electron. Commun. Probab. 7, 2002): if, for a coordinate
direction e, the events X_n.e -> +infinity and X_n.e -> -infinity both have probability zero, then X_n.e/n tends to 0
almost surely. With the directional law of large numbers of the survey this gives the almost sure convergence of X_n/n
under the same two assumptions (Corollary 1.4), and the limit lies in {v, -cv} for some vector v and c >= 0 with no
assumption on a basis of directions (Corollary 1.5).

Zerner applies the strong Markov property at the first visit of the walk to each hyperplane {x : x.e = m}. For an
excited random walk the law after such a visit depends on which entries of the stacks have been used, and the paper
replaces that step by a sum over the paths of bounded length the walk can follow from that first visit to its last
visit to the same hyperplane.

## Code

Python 3, standard library only. Run from the repository root.

* `code/check_decomposition.py` checks, exactly and on finite horizons, the sum over the paths of Pi_c in the proof of
  Lemma 3.2 for three stacks on Z^2, and writes `data/decomposition_checks.json`.
* `code/check_counting_and_trap.py` checks the two averages bounded in the proof of Zerner's lemma
  (Lemma 2.2 of the paper, Lemma 3 of Zerner 2002) on random paths, and
  simulates the two-site trapping example of Remark 5.1; it writes `data/counting_and_trap.json`.

`SHA256SUMS` lists the checksums of every file in the repository.

## License

The text is released under CC BY 4.0 and the code under the MIT license.
