from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
import configparser
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT / 'config.ini')

dbuser = config['DEFAULT']['DBUSER']
dbpassword = config['DEFAULT']['DBPASSWORD']
dbname = config['DEFAULT']['DBNAME']
dbport = config['DEFAULT']['DBPORT']
dbhost = config['DEFAULT']['DBHOST']

scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(
            url=f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}',
            ),
        'local': MemoryJobStore()
    })

scheduler.start()