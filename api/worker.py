from redis import StrictRedis
from rq import Connection, Worker
from config import REDIS_DB_JOBS

# Importing the top-level sub-package intializes and starts R embedded in the current Python process.
# By importing this here, we remove the need to initialize it for every job.
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

importr('WGCNA')


with Connection(StrictRedis(db=REDIS_DB_JOBS)):
    w = Worker('default')
    w.work()
