#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is part of chd-diagrams and is MIT-licensed.

import logging

def download_images(category, website_root, json):
    logging.debug("Downloading images for %s" % category)

def download_json(url):
    logging.debug("Downloading JSON file %s" % url)

def init():
    if __name__ == "__main__":
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Starting up")
        website_root = "http://www.chd-diagrams.com"
        for (category, url) in [("Heart Disease", "/backend/json/illustrationen"), ("Heart Operation", "/backend/json/opillustrationen")]:
            logging.debug("Processing %s" % category)
            json = download_json("%s%s" % (website_root, url))
            download_images(category, website_root, json)

init()
