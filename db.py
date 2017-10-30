##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : db.py                                                         ##
##  Project   : instacrawler                                                  ##
##  Date      : Sep 23, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2017                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

################################################################################
## Imports                                                                    ##
################################################################################
## Python
import sqlite3;
import pdb;
## instacrawler
from config import *;
from log    import *;


################################################################################
## Private Vars                                                               ##
################################################################################
_db_created = False;


################################################################################
## Public Functions                                                           ##
################################################################################
def db_exists_url(url):
    if(config.ignore_db):
        return False;

    log.D("[DB] Check if url exists\n\tURL: {0}", url);
    rows = _query("SELECT * FROM MediaPageUrls WHERE url = ?", url);

    return len(rows) != 0;

def db_insert_media_url(url):
    if(config.ignore_db):
        return;

    log.D("[DB] Inserting media.\n\tURL: {0}", url);
    _execute("INSERT INTO MediaPageUrls (url) VALUES (?)", url);


################################################################################
## Private Functions                                                          ##
################################################################################
def _open_db():
    if(config.ignore_db):
        return;

    con = sqlite3.connect(config.db_name);
    if(not _db_created):
        _create_db(con);

    return con;

def _create_db(con):
    global _db_created;

    if(_db_created):
        return;

    _db_created = True;
    try:
        log.D("[DB] Creating DB....");
        _execute("CREATE TABLE MediaPageUrls (id INTEGER PRIMARY KEY, url TEXT)");

    except:
        log.D("[DB] DB already exists - Skipping....");


def _query(stmt, *args):
    con = _open_db();
    with con:
        cur = con.cursor();
        cur.execute(stmt, args);
        rows = cur.fetchall();

        return rows;

def _execute(stmt, *args):
    con = _open_db();
    with con:
        cur = con.cursor();
        cur.execute(stmt, args);
        con.commit();


################################################################################
## "Test"                                                                     ##
################################################################################
if __name__ == '__main__':
    val = db_exists_url("my url");
    print(val);

    db_insert_media_url("my url");
    val = db_exists_url("my url");
    print(val);
