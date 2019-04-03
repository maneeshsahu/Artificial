"""
This is an example showing how to make the scheduler into a remotely accessible service.
It uses RPyC to set up a service through which the scheduler can be made to add, modify and remove
jobs.

To run, first install RPyC using pip. Then change the working directory to the ``rpc`` directory
and run it with ``python -m server``.
"""

import subprocess
import rpyc
import time
import datetime
import uuid
import os
from rpyc.utils.server import ThreadedServer
from apscheduler import events
from apscheduler.schedulers.background import BackgroundScheduler

log_dir='logs'

def set_up_logfiles():
    try:
        os.mkdir(os.getcwd() + '/' + log_dir)
    except Exception:
        pass

def print_text(text):
    print(text)

def exec_shell_cmd(args):
    job_id = args[-1]

    print('Executing {0} {1}'.format(job_id, args[:-1]))
    process = subprocess.Popen(args[:-1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    code = process.returncode

    print('Stdout', out)
    print('Stderr', err)
    print('Code', code)

    store_info(job_id, out, err, code)

def store_info(job_id, out, err, code):
    # Store info as in a file
    #job_info[job_id] = (out, err, code)
    with open(os.getcwd() + '/' + log_dir + '/' + job_id + '.log', 'w') as fp:
        fp.write("{0}\t{1}\t{2}".format(out, err, code))

class SchedulerService(rpyc.Service):
    #def exposed_add_job(self, func, *args, **kwargs):
    def exposed_add_job(self, func, sch_type, args, run_date):        
        print(func)
        # Create the unique job ID instead of relying on APScheduler to create one
        job_id = str(uuid.uuid4())
        newargs = list(args[0])
        newargs.append(job_id)
        ret_val = scheduler.add_job(func, sch_type, [newargs], run_date=datetime.datetime.now(), id=job_id)
        return ret_val

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

    def exposed_get_jobinfo(self, job_id):
        with open(os.getcwd() + '/' + log_dir + '/' + job_id + '.log', 'r') as fp:
            indata = fp.read()
            print(indata)
            return indata

def my_listener(event):
    print('')

    #if event.exception:
    #    print('The job crashed :(')
    #else:
    #    print('The job worked :)')

if __name__ == '__main__':
    set_up_logfiles()
    scheduler = BackgroundScheduler()
    scheduler.add_listener(my_listener, events.EVENT_JOB_EXECUTED | events.EVENT_JOB_ERROR)
    scheduler.start()
    protocol_config = {'allow_all_attrs': True}
    server = ThreadedServer(SchedulerService, port=12345, protocol_config=protocol_config)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()