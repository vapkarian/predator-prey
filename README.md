Implementation of math game "Predator-prey"
=============

Program creates table with size M x N (parameters **M** and **N**) divided into cells. Each cell can be either empty or
occupied by predator or occupied by victim.

Cell-victim:
1. Victim appears after some cycles (parameter **VICTIM_RECYCLE**) in a random empty cell.
2. Victim does not change its position throughout the life.

Cell-predator:
1. Predator can move to an adjacent cell by one cycle.
2. Objective of the predator is eating victims, so if predator is near the victim, the predator can swallow victim by
moving into the cell. During one cycle predator can eat only one victim. If there are several victims near the
predator, predator can choose victim randomly.
3. Predator dies if he had several consecutive cycles without eating (parameter **PREDATOR_HUNGER_CYCLES**).
4. Reproduction of predators occurs in the case when predator had the opportunity to eat victims some consecutive
cycles (parameter **PREDATOR_REPRODUCTION_CYCLES**). When the specified number of cycles of bellyful is reached new
predator will be appear in the cell where parent was before moving. Number of cycles of bellyful will be reset to
the zero.

Additional features:
1. You can see graph of count of victims and predators depending on time (if you haven't matplotlib, statistics will be
outputted in text table format).
2. You can intervene in the process and remove predators and victims by clicking left mouse button.
3. You can pause live cycles by clicking "Space bar" key and continue it again.
