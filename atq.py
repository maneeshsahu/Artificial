"""
RPC client lists the jobs scheduled.
"""

import sys
import time
from time import sleep
from dateutil import parser
import rpyc

conn = rpyc.connect('localhost', 12345)
jobs = conn.root.get_jobs()
print(jobs)