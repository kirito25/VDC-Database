#!/usr/bin/python
import sqlite3
try:
    import psycopg2
    SUPPORT_POSTGRES = True
except ImportError:
    print "No support for Postgres, install psycopg2"
    SUPPORT_POSTGRES = False
    
import sys, os
from utils import zinc15_filename, pdbqt, mol2
import subprocess


def file_exist(conn, filename, catalog):
    """
    Check the database for an entry with filename properties
    and return the fetchall()
    """
    values = zinc15_filename.parse_filename(filename)
    c = conn.cursor()
    statement = "select file_id from file where " + \
            "weight = %s and logP = %s and charge = %s and pH = \"%s\" and purchasability = \"%s\" and reactivity = \"%s\" and type  = \"%s\" and catalog = \"%s\""  % \
            (values['weight'], values['logP'], values['charge'],
             values['pH'], values['purchasability'], values['reactivity'], filename.split('.')[-1], catalog)
    c.execute(statement)
    result  = c.fetchall()
    c.close()
    return result


def insert_model_from_file(conn, filename, file_id):
    """
    Given the filename check that it is a supported type,
    currently on "mol2" and "pdbqt" files are supported.
    Parse the file using package in utils to get indivual
    ligands from the file and add them to the database.
    """
    SUPPORTED_TYPES = ["mol2", "pdbqt"]
    c = conn.cursor()
    # Check for supported types
    file_type = filename.split('.')[-1].strip().lower()
    if file_type not in SUPPORTED_TYPES:
        return
    if file_type == "pdbqt":
        parser = pdbqt.models
    elif file_type == "mol2":
        parser = mol2.molecules
    with open(filename, 'r') as f:
        for name, data in parser(f.read()):
            statement = "insert into model(name, file_id) values (\"%s\", %s)" % (name, file_id)
            c.execute(statement)
    conn.commit()
    c.close()


def insert_file(conn, filename, catalog):
    c = conn.cursor()
    file_id = -1

    if filename is None:
        print "No filename provided"
        sys.exit()
    elif not os.path.isfile(filename):
        print "filename is not a file"
        sys.exit()
    values = zinc15_filename.parse(filename)
    result = file_exist(conn, filename, catalog)
    # if there is no entry for this file already, base on zinc15 filename rules
    if result == []:
        statement = "insert into file(filename, weight, logP, charge, pH," + \
                "purchasability, reactivity, type, catalog) values " + \
                "(\"%s\", %s, %s, %s, \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % \
                (filename, values['weight'], values['logP'], values['charge'],
                 values['pH'], values['purchasability'], values['reactivity'], values['type'], catalog)
        
        c.execute(statement)
        file_id = c.lastrowid
        insert_model_from_file(conn, filename, file_id)
    else:
        print "File %s already in the database, not doing anything ..." % filename
    conn.commit()
    c.close()
    return file_id
    

def connect(db):
    if POSTGRES:
        conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % \
                        (HOST, DBNAME, USER, PASSWORD)
        conn = psycopg2.connect(conn_string)
        return conn
    else:
        if not os.path.isfile(db):
            print "Looked for sqlite3 databse at %s, not found" % db
            print "ABORTING"
            sys.exit(-1)
        else:
            conn = sqlite3.connect(db)
    return conn


def main(directory = 'ligands'):
    conn = connect(SQLITE3_DBNAME)
    try:
        os.chdir(directory)
    except IndexError:
        print "No directory provided"
        sys.exit()
    except OSError:
        print "Looking for ./%s, Directory does not exist" % (directory)
        sys.exit()

    for catalog in os.listdir('.'):
        os.chdir(catalog)
        for file_type in os.listdir('.'):
            os.chdir(file_type)
            for filename in os.listdir('.'):
                insert_file(conn, filename, catalog)
            os.chdir('..')
        os.chdir('..')
    conn.commit()
    conn.close()


def create_database(schema):
    import subprocess
    if POSTGRES:
        command = "psql -f %s" % schema
    else:
        command = "sqlite3 %s < %s" % (SQLITE3_DBNAME, schema)
    subprocess.call(command, shell=True)


if __name__ == '__main__':
    import argparse
    help_message = "Full path to ligands directory in the structure of " + \
                    "\'directory\'/catalog/type, where catalog is the source of the ligands and " + \
                    "where type is a directory name after the type of files " + \
                    "inside it such as \'mol2\'. (default \'ligands\')"
    parser = argparse.ArgumentParser(description="Lingand Databse loader")
    
    parser.add_argument('--postgres', dest='postgres', default=False,
                        action='store_true', help="Use postgres (default False)")
    
    parser.add_argument('--init', dest='init', default=False,
                        action='store_true', help="Initlize databse using schema file (default False)")

    parser.add_argument('--ligand-directory', dest='directory',
                        default='ligands', help=help_message)
    
    parser.add_argument('--host', dest='host', default='localhost',
                        help="Host that serves the database (default \'localhost\')")
    
    parser.add_argument('--dbname', dest='dbname', default='lingads',
                        help="Database name (default \'ligands\')")
    
    parser.add_argument('--user', dest='user', default='postgres',
                        help='User to log into the databse (default \'postgres\')')
    
    parser.add_argument('--password', dest='password', default='secret',
                        help="Postgres db password (default \'secret\')")
    
    parser.add_argument('--schema', dest='schema', default='schema.sql',
                        help='Schema to initlize the databse (default \'schema.sql\')')
    
    parser.add_argument('--sqlite3-name', dest='sqlite3_name', default='ligands.db',
                        help='The name of the SQLite3 Database (default \'ligands.db\')')

    args = parser.parse_args()
    POSTGRES = args.postgres and SUPPORT_POSTGRES
    HOST = args.host
    PASSWORD = args.password
    DBNAME = args.dbname
    USER = args.user
    SQLITE3_DBNAME = args.sqlite3_name 

    if args.init:
        if not os.path.isfile(args.schema):
            print "Schema file does not exist, looked at %s" % args.schema
            sys.exit(-1)
        create_database(args.schema)

    main(args.directory)

