from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dbuser = config['DEFAULT']['DBUSER']
dbpassword = config['DEFAULT']['DBPASSWORD']
dbname = config['DEFAULT']['DBNAME']
dbport = config['DEFAULT']['DBPORT']
dbhost = config['DEFAULT']['DBHOST']

scheduler = AsyncIOScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(
            url=f'postgresql://{dbuser}:{dbpassword}@{dbhost}:{dbport}/{dbname}',
            )
    })

scheduler.start()