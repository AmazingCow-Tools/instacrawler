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
import os.path;
import os;
import time
import urllib;
from selenium import webdriver


################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    Button_LoadMore       = "._1cr2e._epyes";
    Div_MainPagePhotoGrid = "_70iju";
    Div_MainPagePhoto     = "._mck9w._gvoze._f2mse";
    Div_Photo             = "_4rbun";
    Div_Video             = "_qzesf";


################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    driver    = None;
    users     = [];
    curr_user = None;


################################################################################
## Helper functions                                                           ##
################################################################################
def log(*args):
    print " ".join(map(str, args));

def scroll_down(delay=1.5):
    Globals.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(delay);

def get_doc_height():
    return Globals.driver.execute_script("return document.body.scrollHeight")

def build_save_path(src):
    if(src is None):
        return None;

    path = os.path.basename(src);
    path = os.path.join(Globals.curr_user, path);
    return path;

def exists(path):
    return os.path.exists(path);


################################################################################
## Downloaders                                                                ##
################################################################################
def get_photo_info():
    try:
        photo = Globals.driver.find_element_by_class_name(Constants.Div_Photo);
        img   = photo.find_element_by_tag_name("img");
        src   = img.get_attribute("src");

        return src;

    except:
        return None;

def get_video_info():
    try:
        movie = Globals.driver.find_element_by_class_name(Constants.Div_Video);
        video = movie.find_element_by_tag_name("video");
        src   = video.get_attribute("src");

        return src;

    except:
        return None;


################################################################################
## Script                                                                     ##
################################################################################
def scrap(username):
    Globals.curr_user = username;
    log("Username: ", username);

    Globals.driver.get("https://www.instagram.com/{0}/".format(username));
    os.system("mkdir -p {0}".format(username));

    ## Reach the [Load More] Button and click it...
    scroll_down();

    load_more = Globals.driver.find_element_by_css_selector(
        Constants.Button_LoadMore
    );
    load_more.click();

    ## Keep going down to load all photos...
    height = get_doc_height();
    tries  = 3; ## COWTODO(n2omatt): This is ugly...
    while(tries >= 0):
        log("--> Scrolling down...");
        scroll_down(0.5);

        curr_height = get_doc_height();
        if(curr_height != height):
            height = curr_height;
        else:
            tries -= 1;


    urls_list = [];

    ## Get all Photo grid divs...
    log("--> Getting photos grid div.");
    photo_grid_div = Globals.driver.find_elements_by_class_name(
        Constants.Div_MainPagePhotoGrid
    );
    time.sleep(2);

    ## Get all urls for individual photo pages...
    log("--> Getting photos divs.");
    for photo_grid_div in photo_grid_div:
        photo_divs = photo_grid_div.find_elements_by_css_selector(
            Constants.Div_MainPagePhoto
        );

        log("----> Getting photos url.");
        for photo_div in photo_divs:
            a   = photo_div.find_element_by_tag_name("a");
            url = a.get_attribute("href");

            urls_list.append(url);
            log("------> Urls count:", len(urls_list));


    ## Go to each photo page and download it...
    log("--> Downloading photos...");
    for url in urls_list:
        log("----> Url:", url);
        Globals.driver.get(url);

        photo_url = get_photo_info();
        video_url = get_video_info();
        download_url = None;

        photo_save_path    = build_save_path(photo_url);
        video_save_path    = build_save_path(video_url);
        download_save_path = None;

        ## Try to download the photo
        ##    If fail, means that we have a video instead
        if(photo_save_path is not None and not exists(photo_save_path)):
            download_url       = photo_url;
            download_save_path = photo_save_path;

        ## Try to download the video...
        ##    If it fails, something really bad happened...
        elif(video_save_path is not None and not exists(video_save_path)):
            download_url       = video_url;
            download_save_path = video_save_path;

        if(download_save_path is None):
            log("----> Stopping...");
            continue;

        try:
            urllib.urlretrieve(download_url, download_save_path);
        except:
            continue;
        time.sleep(4);


def main():
    Globals.driver = webdriver.Chrome('../ext/chromedriver');

    for item in open("list").readlines():
        Globals.users.append(item.replace("\n",""));

    print Globals.users;
    for username in Globals.users:
        scrap(username);
        time.sleep(20);

    Globals.driver.quit()

main();
