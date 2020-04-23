#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    This file is part of chd-diagrams and is MIT-licensed.

import logging
import os
import urllib.request
import urllib.parse
import json

def get_dumped_json(dump_file):
    # Use a previously dumped file if it exists, to bypass the network transactions
    dumped_json = []
    if os.path.exists(dump_file):
        logging.debug("Using dumped JSON file %s" % dump_file)
        with open(dump_file) as in_file:
            dumped_json = json.load(in_file)
    else:
        logging.debug("No dumped JSON file %s" % dump_file)
    return dumped_json

def download_single_image(url, filepath):
    logging.debug("Downloading %s to %s" % (url, filepath))
    (filename, headers) = urllib.request.urlretrieve(url, filepath)
    if headers["Content-Type"] not in ("image/png", "application/postscript"):
        logging.error("Downloaded file is not an image: %s - %s - Content-Type %s" % (url, filepath, headers["Content-Type"]))
        os.remove(filepath)

def download_images(category, website_root, json_content):
    logging.debug("Downloading images for %s" % category)
    output_folder = "output/%s" % category
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # First key is different in the 2 data sets:
    # illustrationen vs. operationsIllustrationen
    for i in json_content[list(json_content)[0]]:
        name = i["name"]
        bw_img = "%s%s" % (website_root, i["illustration_bw"])
        ext = os.path.splitext(urllib.parse.urlparse(bw_img).path)[1]
        filepath = os.path.join(output_folder, name + ext)
        download_single_image(bw_img, filepath)
        # Some files are .ai files, but often the .png variant also exists, try downloading that as well
        if ext != ".png":
            bw_img_png = bw_img[:-len(ext)] + ".png"
            logging.debug("Source file is %s, also trying to download the .png file %s" % (ext, bw_img_png))
            filepath = os.path.join(output_folder, name + ".png")
            download_single_image(bw_img_png, filepath)

def download_json(url):
    filename = "output/%s.json" % url.split("/")[-1]
    json_content = get_dumped_json(filename)
    if not json_content:
        logging.debug("Downloading JSON file %s" % url)
        with urllib.request.urlopen(url) as urlreq:
            json_content = json.loads(urlreq.read().decode())
        if not os.path.exists("output"):
            os.mkdir("output")
        with open(filename, 'w') as out_file:
            json.dump(json_content, out_file)
            logging.debug("Downloaded JSON file saved in dump file %s" % filename)
    return json_content

def init():
    if __name__ == "__main__":
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Starting up")
        website_root = "http://www.chd-diagrams.com"
        for (category, url) in [("Heart Disease", "/backend/json/illustrationen"), ("Heart Operation", "/backend/json/opillustrationen")]:
            logging.debug("-"*32)
            logging.debug("Processing %s" % category)
            json_content = download_json("%s%s" % (website_root, url))
            download_images(category, website_root, json_content)

init()
