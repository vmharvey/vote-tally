#! usr/bin/env python 
"""
Determine a board for a committee from a set of votes
"""
import pandas as pd
import numpy as np
import sys

def winner(total_votes,min_votes_req):
    winners = total_votes[total_votes['votes']>=min_votes_req]['candidate'].values
    if len(winners) == 0:
        return False
    elif len(winners) == 1:
        return winners[0]
    else:
        sys.exit('You have two winners:'+str(winners))

def tidy(votes):
    for index, row in votes.iterrows():
        row_min = min(row[row>0])
        if row_min > 1:
            row-=row_min-1
    votes[votes<0] = 0
    return votes

def remove_lowest(votes):

    candidates = list(votes.columns)
    removable_candidates = candidates

    for rank in range(1,len(candidates)):
        
        total_votes = count_total_votes(votes[removable_candidates],rank=rank)
        lowest_votes = min(total_votes[total_votes['votes']>0]['votes'])
        lowest_candidates = total_votes[total_votes['votes']==lowest_votes]['candidate'].values

        if len(lowest_candidates) == 1:
            votes[votes[lowest_candidates[0]]==1]-=1
            votes[lowest_candidates[0]] = 0
            votes = tidy(votes)
            return votes

        removable_candidates = lowest_candidates
    sys.exit('No more votes to redistribute but no winners\nVote tally:\n'+str(count_total_votes(votes))+'\nBallot:\n'+str(votes))

def count_total_votes(votes,rank=1):
    candidates = list(votes.columns)
    votes_count = []
    for candidate in candidates:
        votes_count.append(len(votes[votes[candidate]==rank]))
    total_votes = pd.DataFrame({'candidate':candidates,'votes':votes_count})
    return total_votes

def first_algorithm(votes,people=1):
    n_voters = len(votes)
    min_votes_req = int(np.floor(n_voters/(people+1))+1)
    total_votes = count_total_votes(votes)

    while not winner(total_votes,min_votes_req):
        votes = remove_lowest(votes)
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

