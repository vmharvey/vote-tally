#! usr/bin/env python 
"""
Create a random, valid group of candidates and ballots
in to a csv
"""
import random
import argparse
import logging
import pandas as pd

def generate_ballots(n_candidates,n_voters,output):
    """
    Creates a csv of randomised candidates and votes

    Parameters
    ----------
    n_candidates : int
        Number of candidates to generate (alphabetically)
    n_voters : int
        Number of voter ballots to generate
    output : string
        Output location of the csv
    """
    candidates = []
    for cand_no in range(n_candidates):
        tmp_name = 'abcdefghijklmnopqrstuvwxyz'[cand_no]
        for _ in range(random.randint(3,10)):
            if random.random() > 0.7:
                tmp_name += random.choice('aeiouy')
            else:
                tmp_name += random.choice('bcdfghjklmnpqrstvwxz')
        candidates.append(tmp_name.title())
    votes = []
    for _ in range(n_voters):
        tmp_vote = list(range(1,n_candidates+1))
        random.shuffle(tmp_vote)
        votes.append(tmp_vote)

    ballots = pd.DataFrame(votes,columns=candidates)
    LOG.debug(str(ballots))
    ballots.to_csv(output,index=False)
    

def main():
    """
    # Reports the winner of the election from test data
    """
    parser = argparse.ArgumentParser(
            description='Create random votes')
    parser.add_argument('-o','--output',
        type=str,
        default='data/random_votes_1.csv',
        help='Output location of votes csv file')
    parser.add_argument('--cand',
        type=int,
        default=10,
        help='Number of random candidates')
    parser.add_argument('--voters',
        type=int,
        default=20,
        help='Number of voters')
    parser.add_argument('-v','--verbose',action='store_true',help='Enable debug logging')
    args = parser.parse_args()

    # configure logger
    loglevel = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        format="\x1b[33;20m[%(levelname)s] %(name)s:%(funcName)s:%(lineno)d\033[0m %(message)s",
        level=loglevel)
    global LOG
    LOG = logging.getLogger("vote)creator")
    
    generate_ballots(args.cand,args.voters,args.output)
    
if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
