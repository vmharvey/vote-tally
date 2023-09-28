#! usr/bin/env python 
"""
Determine a board for a committee from a set of votes
"""
import pandas as pd
from math import floor
import sys
import argparse
import logging

logging.basicConfig(
    format="\x1b[33;20m[%(levelname)s] %(name)s:%(funcName)s:%(lineno)d\033[0m %(message)s",
    level=logging.INFO)
LOG = logging.getLogger("vote_tally")

def winner(total_votes,min_votes_req,show_order=False):
    """
    # Tells you the elected candidate for a role

    This gives the name of the candidate who reached the minimum
    number of votes necessary to be elected, or the bool False
    if nobody has won yet.

    Parameters
    ----------
    total_votes : pandas dataframe
        Dataframe of candidates and the amount of votes they have
    min_votes_req : int
        The minimum number of votes required to be elected

    Returns
    -------
    candidate : string
        The name of the elected candidate.
        Returns with the bool False if there is not yet a winner.
    """
    winners = total_votes[total_votes['votes']>=min_votes_req]['candidate'].values
    if len(winners) == 0:
        return False
    elif len(winners) == 1:
        if show_order:
            LOG.info(f"Final candidates:\n{total_votes[total_votes['votes']>0]}")
        return winners[0]
    else:
        sys.exit('You have two winners:'+str(winners))

def tidy(votes):
    """
    # Tidies the ballots
    
    Ensures every ballot starts at 1 and goes up from there
    Also ensure no ranks are negative

    Parameters
    ----------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.
        Now all ballots should have a 
    """
    votes[votes<0] = 0
    for index, row in votes.iterrows():
        if max(row) > 1:
            row_values = list(row[row>0].values)
            row_values.sort()
            replacements = range(1,len(row_values)+1)
            for row_value, replacement in zip(row_values,replacements):
                row[row==row_value] = replacement
    votes[votes<0] = 0
    return votes

def remove_lowest(votes,show_order=False):
    """
    # Removes the least-votes candidate and redistributes

    Using the single-transferrable-vote method, the candidate
    with the fewest first-place votes is removed from the
    election and the votes for them redistributed.

    We find those ballots which list said candidate
    first, then redistribute those votes by subtracting 1 from
    every element in the vote order until there is a new 1st
    ranked vote per ballot. Also, all votes for the removed
    candidated are removed.

    Thus, for those affected ballots, their no. 2 choice
    becomes their no. 1 choice, and so on.

    Parameters
    ----------

    total_votes : pandas dataframe
        Dataframe of candidates and the amount of votes they have
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.
        Now the worst-performing candidate has been removed.

    """
    
    candidates = list(votes.columns)
    removable_candidates = candidates

    for rank in range(1,max(votes.values[0])+1):
        
        total_votes = count_total_votes(votes[removable_candidates],rank=rank)
        if max(total_votes['votes'])==0:
            continue
        
        lowest_votes = min(total_votes[total_votes['votes']>0]['votes'])
        lowest_candidates = total_votes[total_votes['votes']==lowest_votes]['candidate'].values

        if len(lowest_candidates) == 1:
            votes[votes[lowest_candidates[0]]==1]-=1
            votes[lowest_candidates[0]] = 0
            votes = tidy(votes)
            if show_order:
                LOG.info(f"Removed: {lowest_candidates[0]}")
            return votes

        removable_candidates = lowest_candidates
    if show_order:
        LOG.info(f"Final candidates:\n{total_votes[total_votes['votes']>0]}")
    sys.exit('No more votes to redistribute but no winners')

def count_total_votes(votes,rank=1):
    """
    # Count how many votes each candidate has

    Parameters
    ----------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    total_votes : pandas dataframe
        Dataframe of candidates and the amount of votes they have
    """
    candidates = list(votes.columns)
    votes_count = []
    for candidate in candidates:
        votes_count.append(len(votes[votes[candidate]==rank]))
    total_votes = pd.DataFrame({'candidate':candidates,'votes':votes_count})
    return total_votes

def first_algorithm(votes,show_order=False,people=1):
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

    votes = verify(votes) # remove invalid votes
    n_voters = len(votes)
    min_votes_req = int(floor(n_voters/(people+1))+1)
    total_votes = count_total_votes(votes)

    LOG.debug(f"initial votes = \n{votes}")
    LOG.debug(f"initial total_votes = \n{total_votes}")

    while not winner(total_votes,min_votes_req,show_order=show_order):
        votes = remove_lowest(votes,show_order=show_order)
        total_votes = count_total_votes(votes)
        LOG.debug(f"current votes = \n{votes}")
        LOG.debug(f"current total_votes = \n{total_votes}")
    return winner(total_votes,min_votes_req)

def read_votes(input_file):
    """
    # Read votes in from a csv file into a data frame
    """
    
    votes_df = pd.read_csv(input_file, dtype=float)

    return votes_df

def verify(votes):
    """
    Removes any invalid votes from the collected votes. 
    Valid votes include every number is sequential, 
    between 1 and number of votes, no repeated numbers and 
    a vote made for every candidate.

    Parameters
    ----------
    votes : pandas dataframe
        Every column is a candidate. Every row is one ballot and
        the preferential order for their votes.

    Returns
    -------
    verified_votes : pandas dataframe
        Dataframe of only votes which are valid
    """

    n_votes = votes.shape[0] # Number of votes
    n_candids = votes.shape[1] # Number of candiates 
    idx_drop = [] # Indices that are invalid and will be dropped

    for i in range(n_votes):
        # Votes for voter i
        v_i = votes[i:i+1].values[0]
  
        # Check that voter has voted for each candidate
        # Each vote must be unique
        for j in range(1,n_candids+1):
            # Vote is invalid, break 
            if ((j in v_i) == False):
                idx_drop.append(i)

    # Drop invalid votes and return only valid votes
    verified_votes = votes.drop(index=(idx_drop))
    verified_votes = verified_votes.astype(int)
    LOG.info("Dropped "+str(len(idx_drop))+" invalid ballot(s)")
    LOG.debug("ID(s) of Invalid ballots are: "+str(idx_drop))

    return verified_votes

def main():
    """
    # Reports the winner of the election from test data
    """
    parser = argparse.ArgumentParser(
            description='Determine the winner of an election')
    parser.add_argument('-i','--input',
        type=str,
        default='data/test_votes.csv',
        help='Input location of votes csv file')
    parser.add_argument('-v','--verbose',action='store_true',help='Enable debug logging')
    parser.add_argument('--order',action='store_true',help='Show candidate order')
    args = parser.parse_args()

    # configure logger
    if args.verbose:
        LOG.setLevel(logging.DEBUG)

    votes_df = read_votes(args.input)
    output = first_algorithm(votes_df,show_order=args.order)
    LOG.info(f"The winner is: {output}")

if __name__ == "__main__":
    main()
