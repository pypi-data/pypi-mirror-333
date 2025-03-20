import unittest

from core.base.runnable import Job
from core.scheduler.job_queue import JobQueueInMemory


class MyTestCase(unittest.TestCase):
    def test_job_queue(self):
        jq = JobQueueInMemory()
        job = Job()
        thread_id = job.thread_id
        print('new job ---- %s' % thread_id)

        print('#####enqueue')
        jq.enqueue(thread_id, job)
        jq.dump()

        print('#####start')
        jq.start(thread_id)
        jq.dump()

        print('#####suspend')
        jq.suspend(thread_id)
        jq.dump()

        print('#####resume')
        jq.resume(thread_id)
        jq.dump()

        print('#####terminate')
        jq.terminate(thread_id)
        jq.dump()


if __name__ == '__main__':
    unittest.main()
