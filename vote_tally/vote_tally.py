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
        if total_votes[candidate] < lowest_votes:
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
    tmp_list = [[1,2,3],[1,3,2],[2,1,3],[3,2,1],[3,1,2]]
    votes = pd.DataFrame(tmp_list,columns=['Alpha','Beta','Gamma'])

    n_voters = len(votes)
    min_votes_req = int(np.floor(n_voters/(people+1))+1)
    total_votes = count_total_votes(votes)

    while not winner(total_votes,min_votes_req):
        votes = remove_lowest(total_votes,votes)
        total_votes = count_total_votes(votes)
    return winner(total_votes,min_votes_req)

def main():
    print("test main")
