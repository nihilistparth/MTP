import re

# Regular expression pattern to match the strace output format
pattern = re.compile(r"\[pid\s*(\d+)\]\s*(\d+:\d+:\d+)\s*([\w]+)\((.*?)\)\s*=\s*(.*)")

def parse_strace_line(line):
    match = pattern.match(line)
    if match:
        pid, timestamp, syscall, args, result = match.groups()
        return {
            "timestamp": timestamp,
            "pid": pid,
            "system_call": syscall,
            "arguments": args,
            "result": result
        }
    else:
        return None

# Path to the strace log file
log_file_path = "strace_logs/log1.txt"

# Parse each line in the log file and print the result
with open(log_file_path, "r") as log_file:
    for line in log_file:
        parsed_line = parse_strace_line(line)
        if parsed_line:
            print(parsed_line)
