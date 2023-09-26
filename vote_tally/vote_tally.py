#! usr/bin/env python 
"""
Determine a board for a committee from a set of votes
"""

import pandas as pd

def read_votes():
    """
    Read votes in from a csv file into a data frame
    """
    
    votes_df = pd.read_csv ('data/test_votes.csv')

    return votes_df

def main():
    votes_df = read_votes()
    print(votes_df)
    print("test main")

if __name__ == "__main__":
    main()

