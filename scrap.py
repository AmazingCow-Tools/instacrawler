################################################################################
## Imports                                                                    ##
################################################################################
## Python
import os;
import urllib;
import pdb;
## BS4
from bs4 import BeautifulSoup
## instacrawler
import bs4_helpers;

from db      import *;
from driver  import *;
from fs      import *;
from helpers import *;
from log     import *;


################################################################################
## Public Functions                                                           ##
################################################################################
def scrap_scrap(*args, **kwargs):
    username = args[0];

    try:
        driver = driver_create();
        ## First scrap the main (the user) page and fetch all the media urls.
        ## With the all the media urls at hand start scraping each media
        ## page to retrieve the actual media (photo | video) link.
        media_pages_urls = _scrap_main_page  (driver, username);
        media_urls_dict  = _scrap_media_pages(driver, media_pages_urls);

        _download_medias(username, media_urls_dict["photos"]);
        _download_medias(username, media_urls_dict["videos"]);

    except:
        ## COWTODO(n2omatt): What we gonna do to handle errors???
        raise;

    finally:
        driver_close(driver);


################################################################################
## Private Functions                                                          ##
################################################################################
def _scrap_main_page(driver, username):
    log.I("[SCRAP] Main page username: ({0})", username);

    fs_create_user_dir(username);

    driver_navigate(driver, "https://instagram.com/{0}".format(username));
    driver_load_main_page(driver);

    html = driver_get_html(driver);
    soup = BeautifulSoup(html, "lxml");

    urls_list = [];

    ## Get all media links on main page...
    log.D("[SCRAP] Getting photos grid div.");

    media_divs = bs4_helpers.find_all_class(soup, "_mck9w _gvoze _f2mse");
    log.D("[SCRAP] Found {0} media divs", len(media_divs));

    for media_div in media_divs:
        tag_a = bs4_helpers.find_first_tag(media_div, "a");
        url   = bs4_helpers.optional_attr (tag_a, "href");

        fullurl = "https://www.instagram.com" + url;
        if(db_exists_url(fullurl)):
            log.I(
                "[SCRAP] Media page url already exists - Skipping\n\tURL:{0}",
                fullurl
            );
            continue;

        urls_list.append(fullurl);

    log.I("[SCRAP] Found ({0}) media urls...", len(urls_list));
    return urls_list;


def _scrap_media_pages(driver, url_list):
    photo_urls = [];
    video_urls = [];
    error_urls = [];

    for i in xrange(len(url_list)):
        url = url_list[i];

        log.I(
            "[SCRAP] Scrapping media page ({0} of {1})\n\tURL: {2}",
            i+1,
            len(url_list),
            url
        );

        ## Go to page and gets it's content.
        driver_navigate(driver, url);
        html = driver_get_html(driver);
        soup = BeautifulSoup(html, "lxml");

        ## Check if it's a photo...
        tag = bs4_helpers.find_first_class(soup, "_2di5p");
        src = bs4_helpers.optional_attr   (tag,     "src");

        if(src is not None):
            log.I(
                "[SCRAP] Found photo\n\tP:({0}) V:({1}) E:({2})",
                len(photo_urls),
                len(video_urls),
                len(error_urls)
            );

            photo_urls.append({"media_url" : url, "src_url": src});
            continue;

        ## If fails, check if it's video...
        tag = bs4_helpers.find_first_class(soup, "_l6uaz");
        src = bs4_helpers.optional_attr   (tag,     "src");

        if(src is not None):
            log.I(
                "[SCRAP] Found video\n\tP:({0}) V:({1}) E:({2})",
                len(photo_urls),
                len(video_urls),
                len(error_urls)
            );

            video_urls.append({"media_url" : url, "src_url": src});
            continue;

        ## If both tries failed, we have a "not expected" situation
        ## save it to debug later...
        log.W("[SCRAP] Failed to scrap page: {0}", url);
        errors_urls.append({"media_url" : url, "src_url": src});
        continue;

    return {
        "photos" : photo_urls,
        "videos" : video_urls,
        "errors" : error_urls
    };


def _download_medias(username, url_list):
    error_urls = [];
    for i in xrange(len(url_list)):
        try:
            url       = url_list[i];
            media_url = url["media_url"];
            src_url   = url["src_url"  ];

            log.I("[SCRAP] Downloading media {0} of {1}", i+1, len(url_list));
            log.I("[SCRAP] URL: {0}\n\tSRC: {1}", media_url, src_url);

            save_path = fs_build_save_path(username, src_url);
            if(fs_exists(save_path)):
                log.I("[SCRAP] Already media saved at: {0}", save_path);
                continue;

            urllib.urlretrieve(src_url, save_path);
            db_insert_media_url(media_url);
            log.D("[SCRAP] Success...");

        except Exception as e:
            log.E("[SCRAP] Failed to download media.\n\tException: {0}", e);
            error_urls.append(url_list[i]);
            continue;

    ## COWTODO(n2omatt): Dump media errors...
