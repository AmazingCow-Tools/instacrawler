################################################################################
## Imports                                                                    ##
################################################################################
## Python
import sqlite3;


def _open_db():
    con = sqlite3.connect("DB2.db");
    try:
        cur = con.cursor();
        cur.execute("CREATE TABLE MediaPageUrls (id INTEGER PRIMARY KEY, url TEXT)");
        con.commit();
    except:
        pass;

    return con;


def db_exists_url(url):
    return False;

def db_insert_media_url(url):
    return None;

def db_insert_url(url):
    return None;
