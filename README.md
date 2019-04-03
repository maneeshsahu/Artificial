## Python AT Command

### Installation

Install the python packages - APScheduler and RPyC that are not part of the standard distribution

You can install from the frozen requirements.txt of this project.

`pip install -r requirements.txt`

### Usage

Run the background scheduler in a RPC server. Run this before running any of the clients

`python -m server`

Run the clients

#### AT Python
Schedules a job.

Similar to the Unix at command, pipe the command as stdin and read the time as a command-line argument as below:

`echo 'echo hello world' | python at.py 9:30 PM Tue`

#### ATQ Python
Lists all the scheduled jobs
`python atq.py`

#### ATRM Python

Removes the scheduled job
`python atrm.py <job_id>`

#### ATINFO Python

Lists the stdout, stderr and return code of the job
`python atinfo.py <job_id>`

### Approach
This project was implemented in Python 3 using some key third-party libraries:
- AP Scheduler:
  - Performs scheduled, interval actions. Using only scheduled events
  - Can persist events – SQL, Mongo,… Currently using In-Memory Store
  - Split into a Server for executing scheduled events and clients for sending
commands
- RPyC
  - Pythons RPC client and server implementation
  - Could have hardened it or used pipes
- Subprocess
  - Python’s inbuilt library for handling subprocesses
- Datetime Parser
  - Parses Datetime, converts to epoch and back

What could have been improved in the submission:
- More Python Unit Test Cases
- Dockerization




