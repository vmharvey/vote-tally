# vote-tally

Tally up votes for a university club, for a number of roles each with varable number of positions. The voting implements the Hare-Clark electoral system and declares the incoming committee.

Goals:
0. Funnier name
1. Decide on format of file that the votes are read from.
2. One person for one role (single transferrable vote).
3. Multiple people, one role (Hare-Clark)
4. Varying people, multiple roles
5. Bonus: Candidate preferences for roles
6. Pass pylint

## Installation for developers

Only Python 3.7.x is tested and supported.

1. Clone the repo
2. Run `pip install -e .` to install all dependencies with pip.

## Usage

`vtally [args]`
