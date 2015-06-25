#!/usr/bin/env python
"""
utils helper library
   Called by flask dubweb app
   for loading data, etc.
"""

from app import app
import MySQLdb
import json

def load_json_definition_file(filename):
    """
    Load definition file (json).
    """
    mydict = {}

    try:
        with open(filename, 'r') as settingsfile:
            mydict = json.load(settingsfile)
            settingsfile.close()
    except IOError:
        app.logger.error("Couldn't load filename: %s", filename)

    return mydict


def open_monitoring_db(db_host, db_user, db_pass, db_database):
    """
    Open MySQL monitoring DB
    """
    returnval = 1
    conn = None

    try:
        conn = MySQLdb.connect(host=db_host,
                              user=db_user,
                              passwd=db_pass,
                              db=db_database)

    except MySQLdb.Error, err:
        app.logger.error("mysql exception: [%d]:  %s", err.args[0],
                                 err.args[1])
        returnval = 0

    return returnval, conn


def get_from_db(query, query_params, dub_conn):
    """
    Given a query and optional parameters...
    Return the results
    """

    dblist = []

    cursor = dub_conn.cursor()
    try:
        if query_params:
            cursor.execute(query, query_params)
        else:
            cursor.execute(query)
        dblist = cursor.fetchall()
    except Exception, err:
        app.logger.error("mysql exception: [%d]:  %s", err.args[0],
                                 err.args[1])
        app.logger.error("generated by: %s", query)
    finally:
        cursor.close()

    return dblist
