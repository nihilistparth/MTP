import pandas as pd
import numpy as np
# from parse_logs import parse_logs
def overlap(a, b, theta, dmin, dmax):
    amin = a - theta
    amax = a + theta
    bmin = b - theta
    bmax = b + theta
    alpha_min = amin + dmin
    alpha_max = amax + dmax

    if alpha_min <= bmax and bmin <= alpha_max:
        return True
    else:
        return False

def co_occur(log, s, s_prime, l):
    count = 0
    for i in range(len(log)):
        if log[i] == s:
            for j in range(i+1, min(i+l+1, len(log))):
                if log[j] == s_prime:
                    count += 1
                    break
    return count

def count(log, s):
    return log.count(s)

def viterbi(observed_states):
    """
    Simplified Viterbi algorithm for root cause analysis.
    observed_states: List of observed states (as indices)
    """
    V = np.zeros((len(state_index), len(observed_states)))
    path = np.zeros((len(state_index), len(observed_states)), dtype=int)

    # initialization
    V[:, 0] = initial_state_prob * transition_matrix[:, observed_states[0]]

    for t in range(1, len(observed_states)):
        for s in range(len(state_index)):
            prob = V[:, t-1] * transition_matrix[:, s]
            V[s, t] = np.max(prob)
            path[s, t] = np.argmax(prob)

    # backtracking
    best_path = [np.argmax(V[:, -1])]
    for t in range(len(observed_states)-1, 0, -1):
        best_path.insert(0, path[best_path[0], t])

    print("best_path",best_path,"")
    return [states.iloc[i] for i in best_path]


if __name__ == "__main__":
    # parse log data
    # parse_logs()
    
    log_data = pd.read_csv('combined_logs.csv')

    # states based on unique combinations \
    columns_for_state = ['machine_id', 'container_id', 'process_id', 'parent_process_id', 'user_id', 'system_call', 'arguments']
    states = log_data.drop_duplicates(subset=columns_for_state).reset_index(drop=True)
    # mp each state to an index
    # state_index = {state: index for index, state in enumerate(states.itertuples(index=False))}
    state_index = {tuple(state): index for index, state in enumerate(states[columns_for_state].values)}

    output_file = 'state_space.txt'
    # print(state_index)
    # Open the file in write mode and write each key-value pair
    # with open(output_file, 'w') as file:
    #     for key, value in state_index.items():
    #         file.write(f"{key}: {value}\n")
    
    
    # initial state vector
    initial_state_prob = np.zeros(len(state_index))
    initial_state_prob[0] = 0.5  # Assuming the first state is the starting point mid1
    initial_state_prob[305] = 0.5  # Assuming the first state is the starting point mid2
    # assign 1/n to machine 2's first even as well 

    # transition probability matrix
    transition_matrix = np.zeros((len(state_index), len(state_index)))

    # Populate the transition matrix based on log data (simplified approach)
    for i in range(len(log_data) - 1):
        current_state = log_data.iloc[i]
        next_state = log_data.iloc[i + 1]
        
     
        current_state_key = tuple(current_state[col] for col in columns_for_state)
        next_state_key = tuple(next_state[col] for col in columns_for_state)
        # print(current_state_key,next_state_key)
        # Check if the current state key is in the state index
        if current_state_key not in state_index:
            # print(current_state_key)
            print("yes")
            continue 

        if next_state_key not in state_index:
            # Handle the missing key, 
            print("no")
            continue  
        
        # print(("found"))
        current_index = state_index[current_state_key]
        next_index = state_index[next_state_key]
        
        #if both on same machine

        #different machines
        
        
    # Normalize the transition matrix
    row_sums = transition_matrix.sum(axis=1, keepdims=True)
    transition_matrix = np.divide(transition_matrix, row_sums, out=np.zeros_like(transition_matrix), where=row_sums != 0)
    # can be used like this
    observed_states =  [30,45]  # examples of observed states
    root_cause_path = viterbi(observed_states)
    print("Most likely path of states leading to the issue: \n", root_cause_path,"\n")


'''
take 2 apps (consult chatgpt)
http server need some iteraction from outside, talk to the database , get some stored data and modify web page, client to talk to server
client is outside (local machine) , hence expose port 
comm btw mysql and server (no need to expose they have their own virtual network)
access service from outside (expose docker port to the rest of the world) no need for exposing 
github samples of two different dockers (simple docker compose) host! (anything would work) mysql
modify time in those two dockers (not host system time, manually skew) modify using time command at the entry point)
test with static delay difference (first do it with this only)
again issue time command (iteratively)
logs generated are input to the algorithm!

'''