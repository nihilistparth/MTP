import pandas as pd
import numpy as np
from parse_logs import parse_logs

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
    parse_logs()
    
    log_data = pd.read_csv('log.csv')

    # states based on unique combinations of the relevant fields
    states = log_data.drop_duplicates(subset=['machine_id', 'container_id', 'process_id', 'parent_process_id', 'user_id', 'system_call', 'arguments'])

    # map each state to an index
    state_index = {state: index for index, state in enumerate(states.itertuples(index=False))}
    print(states)
    # initial state vector
    initial_state_prob = np.zeros(len(state_index))
    initial_state_prob[0] = 1  # Assuming the first state is the starting point

      # transition probability matrix
    transition_matrix = np.zeros((len(state_index), len(state_index)))

    # Populate the transition matrix based on log data (simplified approach)
    for i in range(len(log_data) - 1):
        current_state = log_data.iloc[i]
        next_state = log_data.iloc[i + 1]
        current_index = state_index[(current_state.machine_id, current_state.container_id, current_state.process_id, current_state.parent_process_id, current_state.user_id, current_state.system_call, current_state.arguments)]
        next_index = state_index[(next_state.machine_id, next_state.container_id, next_state.process_id, next_state.parent_process_id, next_state.user_id, next_state.system_call, next_state.arguments)]
        transition_matrix[current_index, next_index] += 1

    # Normalize the transition matrix
    transition_matrix = transition_matrix / transition_matrix.sum(axis=1, keepdims=True)
# can be used like this
observed_states =  [0,2]  # examples of observed states
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