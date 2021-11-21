from peewee import *

db = SqliteDatabase('db.sqlite3')


class UserProperties(Model):
    id = TextField(column_name='id', primary_key=True)
    state = TextField(column_name='state', default='start')
    context = TextField(column_name='context', null=True)
    long = FloatField(column_name='long', null=True)
    lat = FloatField(column_name='lat', null=True)

    class Meta:
        database = db


if __name__ == '__main__':
    db.connect()
    db.create_tables([UserProperties])
