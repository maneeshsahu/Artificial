"""
RPyC client that removes a listed Job
Usage:
   python atrm.py <job_id>
"""

import sys
import time
from time import sleep
from dateutil import parser
import rpyc

if len(sys.argv) < 2:
    print('Usage python atrm.py <job_id>')
    exit(-1)

job_id = sys.argv[1]
print('Removing Job', job_id)

conn = rpyc.connect('localhost', 12345)
ret_val = conn.root.remove_job(job_id)
print('Removed', ret_val)