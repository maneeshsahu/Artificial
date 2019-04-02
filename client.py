"""
ARCHIVE - TO BE REMOVED
"""

import sys
import time
from time import sleep
from dateutil import parser
import rpyc

if len(sys.argv) < 2:
    print('Usage python at.py <TIME STRING>')
    exit(-1)

time_args = sys.argv[1:]
time_str = ' '.join(time_args)
dt = parser.parse(time_str).strftime('%s')
print("Epoch", dt)

commands = []
for line in sys.stdin:
    commands.append(line.strip())
if len(commands) < 1:
    print('Pass Unix commands in stdin or pipe it to the python program')
    exit(-1)

print(commands)

conn = rpyc.connect('localhost', 12345)
job = conn.root.add_job('server:exec_shell_cmd', 'date', args=[commands[0].split()], run_date=dt)
print(job.id)


sleep(10)
conn.root.remove_job(job.id)
