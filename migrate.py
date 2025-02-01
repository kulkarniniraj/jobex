import json
from peewee import *
from playhouse.migrate import *

db = SqliteDatabase('people.db')

def migrate_db_1():
    """
    Add a job_link field to the Position table
    """
    db.connect()
    migrator = SqliteMigrator(db)
    migrate(
        migrator.add_column('position', 'job_link', CharField(null=True))
    )
    db.close()

if __name__ == '__main__':
    migrate_db_1()
    