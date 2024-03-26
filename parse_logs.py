
import os
import csv
import re
from datetime import datetime

# Define a function to parse a single line of strace log
def parse_strace_line(line):
    regex = r'(\d+\.\d+) (\w+)\((.*)\) = (.*)'
    match = re.match(regex, line)
    if match:
        timestamp, system_call, arguments, result = match.groups()
        timestamp = datetime.fromtimestamp(float(timestamp))
        return (timestamp, system_call, arguments)
    return None

# Define a function to extract process_id from the filename
def extract_process_id(filename):
    # Assuming the format is 'strace_output.<process_id>'
    return filename.split('.')[-1]

# Define a function to process log files from a directory
def process_log_files(log_directory, machine_id):
    log_files = [os.path.join(log_directory, f) for f in os.listdir(log_directory) if f.startswith('strace_output')]
    data = []
    for log_file in log_files:
        process_id = extract_process_id(os.path.basename(log_file))
        with open(log_file, 'r') as file:
            for line in file:
                parsed_line = parse_strace_line(line)
                if parsed_line:
                    timestamp, system_call, arguments = parsed_line
                    data.append({
                        'timestamp': timestamp,
                        'machine_id': machine_id,
                        'container_id': 1,  # Assuming container_id is the same as machine_id
                        'process_id': process_id,
                        'parent_process_id': 1,  # As instructed
                        'user_id': 1,  # User ID is 1 for all entries
                        'system_call': system_call,
                        'arguments': arguments
                    })
    return data

# Path to the directories containing strace logs
path_to_db_logs = 'strace_logs_db'  
path_to_server_logs = 'strace_logs_server'  

# Process the logs from both directories
db_data = process_log_files(path_to_db_logs, machine_id=2)
server_data = process_log_files(path_to_server_logs, machine_id=1)

# Combine the data from both sources
combined_data = db_data + server_data

# Sort the combined



combined_data.sort(key=lambda x: x['timestamp'])

# Now let's write the sorted data to a CSV file
csv_columns = ['timestamp', 'machine_id', 'container_id', 'process_id', 'parent_process_id', 'user_id', 'system_call', 'arguments']
csv_file_path = 'combined_logs.csv' 
with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for data in combined_data:
        # Formatting the timestamp to string for the CSV
        data['timestamp'] = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S.%f')
        writer.writerow(data)

# Print a message when done
print(f"Combined logs written to {csv_file_path}")














# # Regular expression pattern to match the strace output format
# pattern = re.compile(r"\[pid\s*(\d+)\]\s*(\d+:\d+:\d+)\s*([\w]+)\((.*?)\)\s*=\s*(.*)")

# def parse_strace_line(line):
#     match = pattern.match(line)
#     if match:
#         pid, timestamp, syscall, args, result = match.groups()
#         return {
#             "timestamp": timestamp,
#             "pid": pid,
#             "system_call": syscall,
#             "arguments": args,
#             "result": result
#         }
#     else:
#         return None

# # Path to the strace log file
# log_file_path = "strace_logs/log1.txt"

# # Parse each line in the log file and print the result
# with open(log_file_path, "r") as log_file:
#     for line in log_file:
#         parsed_line = parse_strace_line(line)
#         if parsed_line:
#             print(parsed_line)
