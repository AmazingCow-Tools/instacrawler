#!/usr/bin/python
# -*- coding: utf-8 -*-

## sudo apt-get -y install python3-pip python3-dev build-essential libssl-dev libffi-dev xvfb
## pip3 install --upgrade pip
## pip install selenium==3.0.0
## pip install pyvirtualdisplay==0.2.1

## wget "http://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip"
## unzip chromedriver_linux64.zip


################################################################################
## Imports                                                                    ##
################################################################################
## Python
import os.path;
import os;
import pdb;
import time
import urllib;
import threading;
## Selenium
from selenium import webdriver
## BS4
from bs4 import BeautifulSoup
## AmazingCow libs
import bs4_helpers;
import random;


################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    users     = [];
    threads   = [];
    threads_max_count = 8;


################################################################################
## Helper functions                                                           ##
################################################################################
def log(*args):
    print " ".join(map(str, args));


################################################################################
## Driver Functions                                                            ##
################################################################################
def driver_scroll_down(driver, delay=0.5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay);

def driver_get_doc_height(driver):
    return driver.execute_script("return document.body.scrollHeight")

def driver_load_main_page(driver):
    ## Reach the [Load More] Button and click it...
    driver_scroll_down(driver);

    load_more = driver.find_element_by_css_selector("._1cr2e._epyes");
    load_more.click();

    ## Keep going down to load all photos...
    height = driver_get_doc_height(driver);
    tries  = 2; ## COWTODO(n2omatt): This is ugly...
    while(tries >= 0):
        log("--> Scrolling down...");
        driver_scroll_down(driver, 0.5);

        curr_height = driver_get_doc_height(driver);
        if(curr_height != height):
            height = curr_height;
        else:
            tries -= 1;


def driver_navigate(driver, url):
    delay = random.uniform(0.5, 4);
    log("--> Sleeping: {0}".format(delay));

    time.sleep(delay);

    driver.get(url);

def driver_get_html(driver):
    element = driver.find_element_by_tag_name("html");
    return element.get_attribute("innerHTML");


################################################################################
## Download Funtions                                                          ##
################################################################################
def download_medias(username, url_list):
    error_urls = [];
    for i in xrange(len(url_list)):
        url = url_list[i];

        log("--> Downloading media {0} - {1}".format(i, len(url_list)));
        log("    URL: {0}".format(url));

        save_path = build_save_path(username, url);
        if(exists(save_path)):
            log("    Already saved  at: {0}".format(save_path));
            break;

        try:
            urllib.urlretrieve(url, save_path);
        except:
            log("[ERROR] Falied to download media.");
            error_urls.append(url);
            continue;

        log("    Saved at: {0}".format(save_path));

    return error_urls;


################################################################################
## Filesystem Functions                                                       ##
################################################################################
def create_output_dir(username):
    os.system("mkdir -p {0}".format(username));

def exists(path):
    return os.path.exists(path);

def build_save_path(name, src):
    if(src is None):
        return None;

    path = os.path.basename(src);
    path = os.path.join(name, path);

    return path;

def dump_errors(username, urls, download_urls):
    f = open(build_save_path(username, "errors.txt"), "a");
    for url in urls:
        f.write("Url: {0}\n".format(url));

    for url in download_urls:
        f.write("Media: {0}\n".format(url));

    f.close();


################################################################################
## Scrap Functions                                                            ##
################################################################################
def scrap_media_pages(driver, url_list):
    photo_urls = [];
    video_urls = [];

    error_urls = [];

    for i in xrange(len(url_list)):
        url = url_list[i];

        log("--> Scrapping media page ({0} - {1})".format(i+1, len(url_list)));
        log("    URL: {0}".format(url));

        driver_navigate(driver, url);

        html = driver_get_html(driver);
        soup = BeautifulSoup(html, "lxml");

        ## Check if it's a photo...
        tag = bs4_helpers.find_first_class(soup, "_2di5p");
        src = bs4_helpers.optional_attr(tag, "src");

        if(src is not None):
            photo_urls.append(src);
            log("-----> Found photo - Count({0})".format(len(photo_urls)));
            continue;

        ## If fails, check if it's video...
        tag = bs4_helpers.find_first_class(soup, "_l6uaz");
        src = bs4_helpers.optional_attr(tag, "src");

        if(src is not None):
            video_urls.append(src);
            log("-----> Found video - Count({0})".format(len(video_urls)));
            continue;

        ## If both tries failed, we have a "not expected" situation
        ## save it to debug later...
        error_urls.append(url);
        continue;

    return {
        "photos" : photo_urls,
        "videos" : video_urls,
        "errors" : error_urls
    };

def scrap_main_page(driver, username):
    log("Username: ", username);

    create_output_dir(username);

    driver_navigate(driver, "https://instagram.com/{0}".format(username));
    driver_load_main_page(driver);

    html = driver_get_html(driver);
    soup = BeautifulSoup(html, "lxml");

    urls_list = [];

    ## Get all media links on main page...
    log("--> Getting photos grid div.");

    media_divs = bs4_helpers.find_all_class(soup, "_mck9w _gvoze _f2mse");
    for media_div in media_divs:
        tag_a = bs4_helpers.find_first_tag(media_div, "a");
        url   = bs4_helpers.optional_attr (tag_a, "href");

        fullurl = "https://www.instagram.com" + url;
        if(db.exists_url(fullurl)):
            continue;

        urls_list.append(fullurl);

    log("    Found {0} urls...".format(len(urls_list)));

    return urls_list;


################################################################################
## Script                                                                     ##
################################################################################
def scrap(*args,  **kwargs):
    username = args[0];

    driver = webdriver.Chrome();
    driver.set_window_position(-1000, -1000);

    try:
        media_pages_urls = scrap_main_page(driver, username);
        media_urls_dict  = scrap_media_pages(driver,  media_pages_urls);

        download_medias(username, media_urls_dict["photos"]);

        download_errors = download_medias(username, media_urls_dict["videos"]);
        dump_errors(
            username,
            media_urls_dict["errors"],
            download_errors
        );

    except:
        pass;

    finally:
        driver.quit()


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
            ##t.join ();



def main():
    for item in open("list").readlines():
        Globals.users.append(item.replace("\n",""));


    while(True):
        make_threads();
        # t1 = make_thread();
        # t2 = make_thread();
        # t3 = make_thread();
        # t4 = make_thread();
        # t5 = make_thread();
        # t6 = make_thread();
        # t7 = make_thread();
        # t8 = make_thread();
        #
        # t1.start();
        #
        # if(t2 is not None): t2.start();
        # if(t3 is not None): t3.start();
        # if(t4 is not None): t4.start();
        # if(t5 is not None): t5.start();
        # if(t6 is not None): t6.start();
        # if(t7 is not None): t7.start();
        # if(t8 is not None): t8.start();
        #
        #
        # t1.join();
        #
        # if(t2 is not None): t2.join();
        # if(t3 is not None): t3.join();
        # if(t4 is not None): t4.join();
        # if(t5 is not None): t5.join();
        # if(t6 is not None): t6.join();
        # if(t7 is not None): t7.join();
        # if(t8 is not None): t8.join();

        if(len(Globals.users) == 0):
            break;



main();
