#! usr/bin/env python 
"""
Determine a board for a committee from a set of votes
"""
import pandas as pd
import numpy as np

def winner(total_votes,min_votes_req):
    """
    # Tells you the elected candidate for a role

    This gives the name of the candidate who reached the minimum
    number of votes necessary to be elected, or the bool False
    if nobody has won yet.

    Parameters
    ----------
    total_votes : dict
        Dictionary of candidates and the amount of votes they have
    min_votes_req : int
        The minimum number of votes required to be elected

    Returns
    -------
    candidate : string
        The name of the elected candidate.
        Returns with the bool False if there is not yet a winner.
    """

    for candidate in total_votes:
        if total_votes[candidate] >= min_votes_req:
            return candidate
    return False

def remove_lowest(total_votes,votes):
    """
    # Removes the least-votes candidate and redistributes

    Using the single-transferrable-vote method, the candidate
    with the fewest first-place votes is removed from the
    election and the votes for them redistributed.

    We find those ballots which list said candidate
    first, then redistribute those votes by subtracting 1 from
    every element in the vote order.

    Thus, for those affected ballots, their no. 2 choice
    becomes their no. 1 choice, and so on.

    Parameters
    ----------

    total_votes : dict
        Dictionary of candidates and the amount of votes they have
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.
    """

    lowest_votes = 999
    lowest_candidate = 'Nobody'
    for candidate in total_votes:
        if total_votes[candidate] < lowest_votes and total_votes[candidate] > 0:
            lowest_candidate = candidate
    votes[votes[lowest_candidate]==1]-=1
    return votes

def count_total_votes(votes):
    """
    # Count how many votes each candidate has

    Parameters
    ----------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    total_votes : dict
        Dictionary of candidates and the amount of votes they have
    """

    total_votes = {}
    for candidate in list(votes.columns):
        total_votes.update({candidate:len(votes[votes[candidate]==1])})
    return total_votes

def first_algorithm(votes,people=1):
    """
    # Calculates the elected candidate for a role

    Parameters
    ----------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    winner : string
        The succesfully elected candidate
    """

    n_voters = len(votes)
    min_votes_req = int(np.floor(n_voters/(people+1))+1)
    total_votes = count_total_votes(votes)

    while not winner(total_votes,min_votes_req):
        votes = remove_lowest(total_votes,votes)
        total_votes = count_total_votes(votes)
    return winner(total_votes,min_votes_req)

def read_votes():
    """
    # Read votes in from a csv file into a data frame
    """
    
    votes_df = pd.read_csv ('data/test_votes.csv')

    return votes_df

def main():
    """
    # Prints the winner of the election from test data
    """
    votes_df = read_votes()
    output = first_algorithm(votes_df)
    print(output)

if __name__ == "__main__":
    main()

