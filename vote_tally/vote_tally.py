#! usr/bin/env python 
"""
Determine a board for a committee from a set of votes
"""
import pandas as pd
import numpy as np

def winner(total_votes,min_votes_req):
    for candidate in total_votes:
        if total_votes[candidate] >= min_votes_req:
            return candidate
    return False

def remove_lowest(total_votes,votes):
    lowest_votes = 999
    lowest_candidate = 'Nobody'
    for candidate in total_votes:
        if total_votes[candidate] < lowest_votes and total_votes[candidate] > 0:
            lowest_candidate = candidate
    votes[votes[lowest_candidate]==1]-=1
    return votes

def count_total_votes(votes):
    total_votes = {}
    for candidate in list(votes.columns):
        total_votes.update({candidate:len(votes[votes[candidate]==1])})
    return total_votes

def first_algorithm(votes,people=1):
    people=1

    n_voters = len(votes)
    min_votes_req = int(np.floor(n_voters/(people+1))+1)
    total_votes = count_total_votes(votes)

    while not winner(total_votes,min_votes_req):
        votes = remove_lowest(total_votes,votes)
        total_votes = count_total_votes(votes)
    return winner(total_votes,min_votes_req)

def read_votes():
    """
    Read votes in from a csv file into a data frame
    """
    
    votes_df = pd.read_csv ('data/test_votes.csv')

    return votes_df

def main():
    votes_df = read_votes()
    output = first_algorithm(votes_df)
    print(output)

if __name__ == "__main__":
    main()

