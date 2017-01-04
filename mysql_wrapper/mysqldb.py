#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from six import itervalues
import mysql.connector
from datetime import date, datetime, timedelta

class SQL:

        username = 'root'
        password = 'spwx'
        database = 'test'
        host = 'localhost'
        connection = ''
        connect = True
	placeholder = '%s'

        def __init__(self):
                if self.connect:
                        SQL.connect(self)
	def escape(self,string):
		return '`%s`' % string
        def connect(self):
        	config = {
        		'user':SQL.username,
        		'password':SQL.password,
        		'host':SQL.host
        	}
        	if SQL.database != None:
        		config['database'] = SQL.database

        	try:
        		cnx = mysql.connector.connect(**config)
        		SQL.connection = cnx
        		return True
        	except mysql.connector.Error as err:

			if (err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
				print "The credentials you provided are not correct."
			elif (err.errno == errorcode.ER_BAD_DB_ERROR):
				print "The database you provided does not exist."
			else:
				print "Something went wrong: " , err
			return False


	def replace(self,tablename=None,**values):
		if SQL.connection == '':
                	print "Please connect first"
                	return False

                tablename = self.escape(tablename )
                if values:
                        _keys = ", ".join(self.escape(k) for k in values)
                        _values = ", ".join([self.placeholder, ] * len(values))
                        sql_query = "REPLACE INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
                else:
                        sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename

				
		cur = SQL.connection.cursor()
            	try:
                	if values:
                    		cur.execute(sql_query, list(itervalues(values)))
                	else:
                    		cur.execute(sql_query)
                	SQL.connection.commit()
                	return True
            	except mysql.connector.Error as err:
                	print ("An error occured: {}".format(err))
                	return False