##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : bs4_helpers.py                                                ##
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
## BeautifulSoup Helpers                                                      ##
################################################################################
def find_all_class(soup, name):
    ret = soup.findAll(True, {"class" : name});
    return ret;

def find_first_class(soup, name):
    ret = soup.findAll(True, {"class": name});
    if(len(ret) != 0):
        return ret[0];
    return None;

def find_all_id(soup, name):
    ret = soup.findAll(True, {"id" : name});
    return ret;

def find_first_id(soup, name):
    ret = soup.findAll(True, {"id" : name });
    if(len(ret) != 0):
        return ret[0];
    return None;

def find_all_tags(soup, tag):
    ret = soup.find_all(tag);
    return ret;

def find_first_tag(soup, tag):
    ret = soup.findAll(tag);
    if (len(ret) != 0):
        return ret[0];
    return None;

def find_all_custom(soup, attr, value):
    return soup.findAll(True, { attr : value });

def find_first_custom(soup, attr, value):
    ret = soup.findAll(True, { attr : value });
    if (len(ret) != 0):
        return ret[0];
    return None;


def optional_text(soup):
    if(soup is not None):
        return soup.text;
    return None;

def optional_attr(soup, attr):
    if(soup is not None):
        return soup.attrs[attr];
    return None;
