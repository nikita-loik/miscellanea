import os, sys, inspect

import numpy as np
import pandas as pd


import matplotlib
from matplotlib import pyplot as plt

import collections
import time
import datetime

import re

import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

working_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(working_dir)
sys.path.insert(0, parent_dir)

from scripts_python import scraper as scr



# https://github.com/MatthewChatham/glassdoor-review-scraper
# https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
# SET UP LOGGER ===============================================================
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(filename)s: %(lineno)s:\n%(message)s')
logger = logging.getLogger(__name__)


# UTILITY FUNCTIONS ============================================================
def get_web_driver(
        ):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver_path = '../web_drivers/chromedriver'
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path=chrome_driver_path)
    driver.implicitly_wait(10)
    return driver


# SCRAPE GLASSDOOR ============================================================
