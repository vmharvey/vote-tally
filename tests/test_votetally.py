def test_import():
    import vote_tally

def test_empty_vote():
    # Test invalid vote remotes
    from vote_tally import verify
    import pandas as pd
    
    # Empty Vote
    votes = {'Bella': [2], 'Tom': [1], 'Susie': ['NaN'], 'Ben': [3]}
    votes_empty_test = pd.DataFrame(votes)  
    votes_verify = verify(votes_empty_test)
    assert len(votes_verify) ==  0 # Verify should be empty 

def test_repeat_vote():
    # Test invalid vote remotes
    from vote_tally import verify
    import pandas as pd

    # Repeat values 
    votes = {'Bella': [3], 'Tom': [1], 'Susie': [2], 'Ben': [3]}
    votes_repeat_test = pd.DataFrame(votes)  
    votes_verify = verify(votes_repeat_test)
    assert len(votes_verify) ==  0 # Verify should be empty 

def test_num_vote():
    # Test invalid vote remotes
    from vote_tally import verify
    import pandas as pd

    # Invalid Number
    votes = {'Bella': [3], 'Tom': ['10'], 'Susie': [2], 'Ben': [4]}
    votes_num_test = pd.DataFrame(votes)  
    votes_verify = verify(votes_num_test)
    assert len(votes_verify) ==  0 # Verify should be empty 

def test_valid_vote():
    # Test invalid vote remotes
    from vote_tally import verify
    import pandas as pd

    # Valid vote
    votes = {'Bella': [3], 'Tom': [1], 'Susie': [2], 'Ben': [4]}
    votes_test = pd.DataFrame(votes)
    votes_ans = {'Bella': [3], 'Tom': [1], 'Susie': [2], 'Ben': [4]}
    votes_ans = pd.DataFrame(votes_ans)   
    votes_verify = verify(votes_test)
    assert (votes_verify.values[0] == votes_ans.values[0]).all()

def test_first_algorithm():
    # Test if the STV algorithm works
    from vote_tally import first_algorithm
    import pandas as pd
    
    votes = {'Bella': [1,1,2,2,2],
    'Tom': [4,3,1,4,3],
    'Susie': [3,2,3,1,4],
    'Ben': [2,4,4,3,1]}
    votes = pd.DataFrame(votes)
    assert first_algorithm(votes) == 'Bella'

def test_count_total_votes():
    # Test if counting the votes works
    from vote_tally import count_total_votes
    import pandas as pd
    
    votes = {'Bella': [1,1,2,2,2],
    'Tom': [4,3,1,4,3],
    'Susie': [3,2,3,1,4],
    'Ben': [2,4,4,3,1]}
    votes = pd.DataFrame(votes)
    
    total_votes = {'candidate':['Bella','Tom','Susie','Ben'],
    'votes':[2,1,1,1]}
    total_votes = pd.DataFrame(total_votes)
    
    assert count_total_votes(votes).equals(total_votes)

def test_remove_lowest():
    # Test if removing a candidate works
    from vote_tally import remove_lowest
    import pandas as pd
    
    votes = {'Bella': [1,1,2,2,2],
    'Tom': [4,3,1,4,3],
    'Susie': [3,2,3,1,4],
    'Ben': [2,4,4,3,1]}
    votes = pd.DataFrame(votes)

    votes_after = {'Bella': [1,1,1,2,2],
    'Tom': [0,0,0,0,0],
    'Susie': [3,2,2,1,3],
    'Ben': [2,3,3,3,1]}
    votes_after = pd.DataFrame(votes_after)

    assert remove_lowest(votes).equals(votes_after)

def test_tidy():
    # Test if dying a dataframe works
    from vote_tally import tidy
    import pandas as pd
    
    votes = {'Bella': [1,1,2,2,2],
    'Tom': [-1,-2,-3,-4,-5],
    'Susie': [3,2,3,1,4],
    'Ben': [2,4,4,3,1]}
    votes = pd.DataFrame(votes)

    votes_after = {'Bella': [1,1,1,2,2],
    'Tom': [0,0,0,0,0],
    'Susie': [3,2,2,1,3],
    'Ben': [2,3,3,3,1]}
    votes_after = pd.DataFrame(votes_after)

    assert tidy(votes).equals(votes_after)

def test_winner():
    # Test if the winner function works
    from vote_tally import winner
    import pandas as pd
    
    total_votes = {'candidate':['Bella','Tom','Susie','Ben'],
    'votes':[3,2,0,0]}
    total_votes = pd.DataFrame(total_votes)
    
    assert winner(total_votes,3) == 'Bella'
    
def test_read_votes():
    # Test if reading votes doesn't fail
    from vote_tally import read_votes
    read_votes('data/test_votes.csv')

def test_generator():
    # Test if the generator works
    from vote_tally.ballot_generator import generate_ballots
    ballots = generate_ballots(12,24)
    assert len(ballots) == 24
    assert len(ballots.columns) == 12
