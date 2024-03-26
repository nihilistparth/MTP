import sys
from parse_logs import parse_log
'''
[mid, cid, pid, ppid, uid, type, args]
mid: machine ID 
cid: container ID
pid: process ID
ppid: parent process ID
uid: user ID
type: the system call type (e.g., rename, execve, etc.)
args: arguments with which this system call was invoked.

log = [logs combined]
log_vector = [[lm1],[lm2],[lm3]]
'''
def parse_logs():
    pass
def initialize_pi():
    pass
def count_log():
    pass

'''
Example usage
log = ['A', 'B', 'C', 'A', 'B', 'A', 'C', 'D', 'A', 'B', 'C']
s = 'A'
s_prime = 'C'
l = 2
'''
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
    
def initialize_vertibi_mat():
    pass
def populate_vertibi_matrix():
    pass
def trace_path():
    pass
if __name__ == "__main__":
    
    
    parse_log(file_path="")
    # Get the arguments passed to the script
    arguments = sys.argv[1:]
    
    # Process the arguments
    event_1 = arguments[0]
    event_2 = arguments[1]
    num_states = count_log()
    initialize_pi()
    