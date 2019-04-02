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
from rpyc.utils.server import ThreadedServer
from apscheduler.schedulers.background import BackgroundScheduler


def print_text(text):
    print(text)

def exec_shell_cmd(args):
    print('Executing', args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    code = process.returncode

    print('Code', code)
    print('Stdout', out)
    print('Stderr', err)
    #return code    


class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        print(func)
        job_id = str(uuid.uuid4())
        kwargs['run_date'] = datetime.datetime.now()
        kwargs['id'] = job_id
        
        #datetime.datetime.fromtimestamp(kwargs['run_date']) 
        print(kwargs)
        ret_val =  scheduler.add_job(func, *args, **kwargs)
        print(ret_val)
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


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    protocol_config = {'allow_all_attrs': True}
    server = ThreadedServer(SchedulerService, port=12345, protocol_config=protocol_config)
    try:
        server.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()