#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from peewee import *
from datetime import date, datetime, timedelta


mysql_db = MySQLDatabase(host = '127.0.0.1', user = 'root', passwd = 'spwx', database = 'test')

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

class Info(BaseModel):
    url = CharField(unique=True)
    name = CharField()
    location = CharField()
    education = CharField()
    employment = CharField()
    bio = CharField()
    content = CharField()
    avatar = CharField()
    ask = CharField()
    answer = CharField()
    agree = CharField()
    thanks = CharField()
    # etc, etc



mysql_db.connect()
# Create the tables.
# mysql_db.create_tables([Info])

