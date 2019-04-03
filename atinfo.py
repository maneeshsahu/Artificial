"""
RPyC client that returns extra information about a completed job
Usage:
   python atinfo.py <job_id>
"""

import sys
import time
from time import sleep
from dateutil import parser
import rpyc

if len(sys.argv) < 2:
    print('Usage python atinfo.py <job_id>')
    exit(-1)

job_id = sys.argv[1]
print('Looking up Job info', job_id)

conn = rpyc.connect('localhost', 12345)
ret_val = conn.root.get_jobinfo(job_id)
values = ret_val.split("\t")
print('Std Output', values[0])
print('Std Error', values[1])
print('Return Code', values[2])