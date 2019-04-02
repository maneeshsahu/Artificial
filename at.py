"""
RPyC client that sends the exec_shell_cmd to the server to add the job with the scheduler.
Usage:
   python at.py <TIME STRING>

   example:
      python at.py 9:30 PM Tue
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
#dt = parser.parse(time_str).strftime('%s')
dt = parser.parse(time_str)
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
print('Job added with ID',job.id)

sleep(10)

