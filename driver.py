##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : driver.py                                                     ##
##  Project   : instacrawler                                                  ##
##  Date      : Oct 28, 2017                                                  ##
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
import time;
## Selenium
from selenium import webdriver
## instacrawler
from config  import *;
from helpers import *;
from log     import *;


################################################################################
## Public Functions                                                           ##
################################################################################
def driver_create():
    driver =  webdriver.Chrome();
    ## COWTODO(n2omatt): Set driver position based on options...
    ## driver.set_window_position(-1000, -1000);
    return driver

def driver_close(driver):
    driver.close();

def driver_scroll_down(driver, delay=0.5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    helper_wait_random_delay(delay);

def driver_get_doc_height(driver):
    return driver.execute_script("return document.body.scrollHeight")

def driver_load_main_page(driver):
    ## Reach the [Load More] Button and click it...
    ##   This is need since instagram doesn't loads all
    ##   medias at once by default.
    driver_scroll_down(driver);

    load_more = driver.find_element_by_css_selector("._1cr2e._epyes");
    load_more.click();

    ## Keep going down to load all photos...
    if(config.load_all_medias):
        height = driver_get_doc_height(driver);
        tries  = 2; ## COWTODO(n2omatt): This is ugly...
        while(tries >= 0):
            log.D("[DRIVER] Scrolling down...");
            driver_scroll_down(driver, 0.5);

            curr_height = driver_get_doc_height(driver);
            if(curr_height != height):
                height = curr_height;
            else:
                tries -= 1;

def driver_navigate(driver, url):
    helper_wait_random_delay(1);
    driver.get(url);

def driver_get_html(driver):
    element = driver.find_element_by_tag_name("html");
    return element.get_attribute("innerHTML");
