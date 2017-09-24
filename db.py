
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


def exists_url(url):
    con = _open_db();
    cur = con.cursor();

    cur.execute("SELECT url FROM MediaPageUrls WHERE url = '{0}'".format(url));
    data = cur.fetchall();

    con.close();

    return len(data) != 0;


def insert_url(url):
    if(exists_url(url)):
        return;

    con = _open_db();
    cur = con.cursor();

    cur.execute("INSERT INTO MediaPageUrls (url) VALUES ('{0}')".format(url));

    con.commit();
    con.close ();
