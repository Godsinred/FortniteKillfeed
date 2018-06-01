# #!/usr/bin/python
# import os
# import psycopg2
#
# hostname = 'localhost'
# username = 'test'
# password = 'test'
# database = 'postgres'
#
# # Simple routine to run a query on a database and print the results:
# def doQuery( conn ) :
#     cur = conn.cursor()
#
#     cur.execute( "SELECT * FROM dummy_table" )
#
#     for id, name in cur.fetchall() :
#         print(id, name)
#
#
# print("Using psycopg2…")
#
# myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
# cur = myConnection.cursor()
# cwd = os.getcwd()
# print(cwd)
# cur.execute("""INSERT INTO dummy_table VALUES(2, 'ken')""")
# cur.execute(r"""CREATE TABLESPACE fortnite_db LOCATION '{}';""".format(cwd))
# myConnection.commit()
# doQuery( myConnection )
#
# myConnection.close()

# !/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import sys
from pg import DB

db = DB(dbname='testdb', host='localhost', port=5432, user='scott', passwd='tiger')

db.query("""CREATE TABLE weather (
     city varchar(80),
     temp_lo int, temp_hi int,
     prcp float8,
     date date)""")

print(db.get_tables())