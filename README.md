# vote-tally

![build-badge](https://github.com/vmharvey/vote-tally/actions/workflows/python-build-test.yml/badge.svg?event=push)

Tally up votes cast in a single transferrable vote ranked choice ballot (eg, for a government election) and declare the winner.

Eventually it will be able to tally votes for a number of roles each with varable number of positions, eg for a university club. The voting will implement the Hare-Clark electoral system and declare the incoming committee.

[Click here to view the project documentation!](https://vmharvey.github.io/vote-tally/)

## Goals

- [ ] 0. Funnier name
- [x] 1. Decide on format of file that the votes are read from.
- [x] 2. One person for one role (single transferrable vote).
- [ ] 3. Multiple people, one role (Hare-Clark)
- [ ] 4. Varying people, multiple roles
- [ ] 5. Bonus: Candidate preferences for roles
- [ ] 6. Bonus: Pass pylint

## Installation for developers

Only Python 3.7.x is tested and supported.

1. Clone the repo
2. Run `pip install -e .` to install all dependencies with pip.

## Usage

`vtally [-v] [-i data/test_votes.csv]`

or use

`vtally --cite`

to print the citation info.
