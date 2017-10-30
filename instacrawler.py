#!/usr/bin/python
# -*- coding: utf-8 -*-
##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : instacrawler.py                                               ##
##  Project   : instacrawler                                                  ##
##  Date      : Sep 21, 2017                                                  ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2017                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

## sudo apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev xvfb
## pip3 install --upgrade pip
## pip install selenium==3.0.0
## pip install pyvirtualdisplay==0.2.1

## wget "http://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip"
## unzip chromedriver_linux64.zip


################################################################################
## Imports                                                                    ##
################################################################################
import threading;

import random;
## instacrawler
from scrap import *;

################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    users     = [];
    threads   = [];
    threads_max_count = 8;



################################################################################
## Download Funtions                                                          ##
################################################################################


################################################################################
## Thread Functions                                                           ##
################################################################################
def make_thread():
    # lock = threading.Lock();
    # with lock:
    if(len(Globals.users) == 0):
        return None;

    name = Globals.users[0];
    del Globals.users[0];

    return threading.Thread(
        name   =  name,
        target = scrap,
        args   = (name,)
    );

def make_threads():
    ## COWNOTE(n2omatt): As we can see... I don't "know" multi thread stuff yet..
    lock = threading.Lock();
    with lock:
        to_delete = [];
        for i in range(len(Globals.threads)):
            t = Globals.threads[i];

            if(not t.is_alive()):
                to_delete.append(i);

        for i in to_delete:
            del Globals.threads[i];

        for i in range(Globals.threads_max_count - len(Globals.threads)):
            t = make_thread();
            if(t is None):
                break;

            Globals.threads.append(t);

            t.start();


################################################################################
## Script                                                                     ##
################################################################################
def main():
    scrap_scrap("n2omatt");

main();
