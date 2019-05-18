# Instant-Insanity
An attempt to find the minimal obstacle of any Instant Insanity puzzle size 30 or less.

## About
The Instant Insanity puzzle consists of n cubes with m colors total. The objective of the puzzle is to stack these cubes in a column so that each side (front, back, left, and right) of the stack shows no repeating colors.

### What is an obstacle?
An obstacle is a subset of cubes such that no matter how these cubes are stacked, it will result in color collisions (i.e.duplications) on any of the sides.



## Prerequisites
* Must have Python 3.0 or higher installed

## Design
The implementation is a simple brute-force approach that checks for half solutions and tries to see if any of the half solutions found match with another half solution. The program iterates through n choose k combinations of the puzzle (it starts off as n = k) and tries to look for any obstacle for the puzzles of size k. If it finds an obstacle, k is decremented and the next puzzle size down is checked for obstacles. The program stops when for every combination of puzzles size k, a full solution is found for each one. This means that the minimal obstacle size is k - 1 and the minimal obstacle is the most recent obstacle found. 
