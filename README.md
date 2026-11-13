# Zero speed for excited random walks on the event of non-transience

Yitzchak Shmalo

Paper: [paper/main.pdf](paper/main.pdf) (source [paper/main.tex](paper/main.tex)).

## Summary

An excited (cookie) random walk on Z^d uses, on its i-th visit to a site, the i-th transition probability in a stack
attached to that site; the stacks are i.i.d. over the sites. Kosygina and Zerner (Problem 4.7 of their 2013 survey)
asked whether X_n/n tends to 0 almost surely on the event that |X_n| does not tend to infinity, assuming only that
the stacks are i.i.d. and every transition probability is positive. The paper proves that it does, in every dimension,
with no further restriction on the stacks: they may be infinite and may push in any direction. If that event has
positive probability, then X_n/n tends to 0 almost surely. The paper also proves the excited-walk form of Zerner's law
of large numbers for random walk in i.i.d. random environment (Electron. Commun. Probab. 7, 2002): if, for a coordinate
direction e, the walk tends to +infinity and to -infinity in direction e with probability zero, then X_n.e/n tends to 0
almost surely.

The strong Markov restart in Zerner's argument, which fails for an excited walk, is replaced by a sum over the
finitely many paths the walk can follow between its first and last visits to a level.

## Code

Python 3, standard library only. Run from the repository root.

* `code/check_decomposition.py` checks, exactly and on finite horizons, the decomposition over short paths in
  Lemma 3.2 for three cookie stacks on Z^2, and writes `data/decomposition_checks.json`.
* `code/check_counting_and_trap.py` checks the two averages bounded in the proof of Zerner's counting lemma
  (Lemma 2.2 of the paper, Lemma 3 of Zerner 2002) on random paths, and
  simulates the two-site trapping example of the closing remark; it writes `data/counting_and_trap.json`.

`SHA256SUMS` lists the checksums of every file in the repository.

## License

The text is released under CC BY 4.0 and the code under the MIT license.
