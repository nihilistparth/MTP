import pandas as pd
import numpy as np
# time complexity O(TS^2)
def viterbi():
    """
    Simplified Viterbi algorithm for root cause analysis using vectorized operations.
    observed_states: List of observed state indices.
    """

    smal = final_state
    num_states = len(state_index)
    T = 5
    V = np.zeros((num_states, T))
    path = np.zeros((num_states, T), dtype=int)
    
    # Initialize the Viterbi matrix with initial probabilities
    for i in range(num_states):
        V[i, 0] = initial_state_prob[i] * transition_matrix[i, smal]

    # Populate the Viterbi matrix
    for t in range(1, T):
        for j in range(num_states):
            seq_probs = V[:, t-1] * transition_matrix[:, j]
            V[j, t] = np.max(seq_probs)
            path[j, t] = np.argmax(seq_probs)

    # Trace back the most likely path
    most_likely_path = [smal]
    previous_state = smal

    for t in range(T - 1, 0, -1):
        previous_state = path[previous_state, t]
        most_likely_path.insert(0, previous_state)

    # Convert indices back to state tuples using index_to_state mapping
    index_to_state = {index: state for state, index in state_index.items()}
    most_likely_path_tuples = [index_to_state[state] for state in most_likely_path]

    # Assuming `states` is a DataFrame that contains all the states and can be indexed by the state tuples
    # return [states.iloc[state] for state in most_likely_path]
    return [[state] for state in most_likely_path]
    

# Assuming all necessary data and parameters like 'states', 'state_index', 'initial_state_prob', 
# 'transition_matrix', 'smal', etc., are defined above this function.

# The 'smal' variable is the index of the known malicious final state.
# The 'num_states' variable is the total number of unique states, and 'T' is the maximum number of steps.
# The 'initial_state_prob' is an array containing the initial probabilities of each state.
# The 'transition_matrix' is a matrix containing the probabilities of transitioning from each state to every other state.



def count_state(s, log_data, columns_for_state):
    return sum((log_data[columns_for_state] == s).all(axis=1))

# Function to count co-occurrences of s and s' within distance λ
# time complexity is O(log_len^2)
def co_occur(s, s_prime, log_data, columns_for_state, lambda_param):
    count = 0
    for i in range(len(log_data) - 1):
        if tuple(log_data.iloc[i][columns_for_state]) == s:
            for j in range(i + 1, min(i + 1 + lambda_param, len(log_data))):
                if tuple(log_data.iloc[j][columns_for_state]) == s_prime:
                    count += 1
                    break
    return count

# time complexity O(1)
#overlap function
def overlap(a, b, theta, dmin, dmax):
    amin = a - theta
    amax = a + theta
    bmin = b - theta
    bmax = b + theta
    alpha_min = amin + dmin
    alpha_max = amax + dmax
    return alpha_min <= bmax and bmin <= alpha_max

# debug this look into the time complexity(reduce)
def calculate_transition_probability(log_data, s, s_prime, columns_for_state, theta, dmin, dmax):
    ts = log_data[(log_data[columns_for_state] == s).all(axis=1)]['timestamp'].values
    ts_prime = log_data[(log_data[columns_for_state] == s_prime).all(axis=1)]['timestamp'].values
    count_overlap = 0
    for tsi in ts:
        for tsj in ts_prime:
            if overlap(tsi, tsj, theta, dmin, dmax):
                count_overlap += 1
    return count_overlap / (len(ts) * len(ts_prime)) if len(ts) > 0 and len(ts_prime) > 0 else 0

# Parameters for overlap function
theta = 5  # Maximum tolerable difference
dmin = 0   # Minimum network delay
dmax = 0   # Maximum network delay
# lambda: maximum distance between s and s'
lambda_param = 10
# Main code
log_data = pd.read_csv('combined_logs2.csv')
columns_for_state = ['machine_id', 'container_id', 'process_id', 'parent_process_id', 'user_id', 'system_call', 'arguments']
states = log_data.drop_duplicates(subset=columns_for_state).reset_index(drop=True) # unique states in my log ignore(ts)
# if there ts every ts is unique (variable)
state_index = {tuple(state): index for index, state in enumerate(states[columns_for_state].values)}

# Initial state vector
#initial_state_prob = np.zeros(len(state_index))
initial_state_prob = np.full(len(state_index), 0.1) # epsilon
initial_state_prob /= initial_state_prob.sum() # sum remains 1
initial_state_prob[0] = 1  # Assuming the first state is the starting point
# initial_state_prob[305] = 1  # Assuming the first state is the starting point
initial_state_prob /= initial_state_prob.sum()
#initial_state_prob[305] = 0.5  # Assuming another state as the starting point

# Transition probability matrix
transition_matrix = np.zeros((len(state_index), len(state_index)))

# Populate the transition matrix based on log data
# Assuming necessary imports and initializations are done above
for i in range(len(log_data) - 1):
    current_state = tuple(log_data.iloc[i][col] for col in columns_for_state)
    next_state = tuple(log_data.iloc[i + 1][col] for col in columns_for_state)
    
    if current_state in state_index and next_state in state_index:
        current_index = state_index[current_state]
        next_index = state_index[next_state]
        # only checking for logs same machine
        if current_state[1] == next_state[1]:  # with open("transition_matrix_debug.txt", "a") as file:
#     file.write(f"Iteration {i}, updating {current_index} -> {next_index}:\n")
#     file.write(f"{np.array2string(transition_matrix, separator=', ')}\n\n")Check if both events occur on the same machine
            cs = count_state(current_state, log_data, columns_for_state) 
            count_co_occur = co_occur(current_state, next_state, log_data, columns_for_state, lambda_param)
            probchange = transition_matrix[current_index, next_index]
            if probchange == 0.0: #update only once
                # print(i) # only one (4->6)*3, 4->7,  4->6 3/4 4->7 (1/4)
                transition_matrix[current_index, next_index] = count_co_occur / cs if cs > 0 else 0
                print(count_co_occur,cs)
                #if(transition_matrix[current_index, next_index]) 
        else:  # Events occur on different machines
            transition_probability = calculate_transition_probability(log_data, current_state, next_state, columns_for_state, theta, dmin, dmax)
            transition_matrix[current_index, next_index] = transition_probability
    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
  
    
# Normalize the transition matrix
row_sums = transition_matrix.sum(axis=1, keepdims=True)
transition_matrix = np.divide(transition_matrix, row_sums, out=np.zeros_like(transition_matrix), where=row_sums != 0)
# with open("transition_matrix_debug.txt", "a") as file:
#     file.write(f"Iteration {i}, updating {current_index} -> {next_index}:\n")
#     file.write(f"{np.array2string(transition_matrix, separator=', ')}\n\n")
######################################################
# our algorithms output
# Example usage
final_state = 4  # malicious observed states
root_cause_path = viterbi()
print("Most likely path of states leading to the issue: \n", root_cause_path, "\n")

'''
try the possibility of taking in time stammps to bound the overlap
better db statement 
**compute complexity and mention them above each function
 # Outputting the best path found
    # s5<-s4 k = 1 orginal log 4>x>y>z>5 multiple times
    # how many log entries are btw s4 and s5
    # if i get this edit distance (mean) is low then accuracy is high
    # ground truth are logs and string matching for accuracy
    # 
    
TESTING 
100 log lines dont consider last 20
we check the mean edit dis of our alogs output with the last 20 lines
takes stats in consideration
'''