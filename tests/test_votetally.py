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