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
def get_web_browser(
        ) -> selenium.webdriver.chrome.webdriver.WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver_path = '../webdrivers/chromedriver'
    browser = webdriver.Chrome(
        options=chrome_options,
        executable_path=chrome_driver_path)
    browser.implicitly_wait(10)
    return browser


# SCRAPE GLASSDOOR ============================================================
def load_main_page(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        url: str = 'https://www.glassdoor.co.uk',
        ):

    print(url)
    browser.get(url)
    browser.implicitly_wait(10)


def accept_cookies(
        browser: selenium.webdriver.chrome.webdriver.WebDriver
        ):
    # Click 'Accept'.
    element = browser.find_element_by_xpath(
        f"//div[@id='_evidon_banner']"
        f"//button[@id='_evidon-accept-button']"
        )
    element.click()
    browser.implicitly_wait(10)


def sign_in(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        e_mail: str,
        password: str,
        ):

    # Click 'Sign In'.
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@class='locked-home-sign-in']"
        f"//a[@class='track-click gd-btn-locked-transparent susiLink sign-in strong nowrap']"
        )
    element.click()
    browser.implicitly_wait(5)

    # Enter e-mail.
    element = browser.find_element_by_xpath(
        f"//div[@class='modal_content']"
        f"//input[@id='userEmail']"
        )
    element.click()
    element.send_keys(e_mail)
    browser.implicitly_wait(5)

    # Enter password.
    element = browser.find_element_by_xpath(
        f"//div[@class='modal_content']"
        f"//input[@id='userPassword']"
        )
    element.click()
    element.send_keys(password)
    browser.implicitly_wait(5)
    element.send_keys(u'\ue007')  # click 'Enter'


def do_search(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        keywords: str,
        location: str,
        ):
    # Enter 'Job Title, Keywords or Company'.
    element = browser.find_element_by_xpath(
        f"//div[@class='search-bar ']"
        f"//input[@class='keyword']"
        )
    element.clear()
    element.click()
    browser.implicitly_wait(5)

    element.send_keys(keywords)

    # Enter 'Location'.
    element = browser.find_element_by_xpath(
        f"//div[@class='search-bar ']"
        f"//input[@class='loc']"
        )
    element.clear()
    element.click()
    browser.implicitly_wait(5)
    element.send_keys(location)

    # Click 'Search'.
    element = browser.find_element_by_xpath(
        f"//div[@class='search-bar ']"
        f"//button[@class='gd-btn-mkt']"
        )
    element.click()


def set_filters(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        jobtype: str,
        post_age: str,
        radius: str,
        ):

    element = browser.find_element_by_xpath(
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='JOBTYPE'][@id='filter_jobType']"
        )
    element.click()
    browser.implicitly_wait(5)
    element = browser.find_element_by_xpath(
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{jobtype}']"
        )
    element.click()

    element = browser.find_element_by_xpath(
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='DATEPOSTED'][@id='filter_fromAge']"
        )
    element.click()
    browser.implicitly_wait(5)
    element = browser.find_element_by_xpath(
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{post_age}']"
        )
    element.click()

    element = browser.find_element_by_xpath(
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='DISTANCE'][@id='filter_radius']"
        )
    element.click()
    browser.implicitly_wait(5)
    element = browser.find_element_by_xpath(
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{radius}']"
        )
    element.click()


def switch_to_next_page(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        ):

    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='ResultsFooter']"
        f"//li[@class='next']"
        )
    element.click()
    browser.implicitly_wait(5)


def get_company_name_and_rating(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='JobResults']"
        f"//div[@class='employerName']"
        )
    name, rating = element.text.split('\n')
    rating = float(rating)
    return name, rating


def get_job_title_and_description(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:
    
    # Get job title.
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='JobResults']"
        f"//div[@class='title']"
        )
    job_title = element.text

    # Get job description.
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='Details']"
        f"//div[@class='jobDescriptionContent desc']"
        )
    job_description = element.text

    return job_title, job_description

def get_company_size_and_url(
        browser: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:

    # Switch to company data.
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='JDCol']"
        f"//div[@class='scrollableTabs']"
        f"//div[@data-tab-type='overview']"
        )
    element.click()
    browser.implicitly_wait(5)

    # Get company size.
    element = browser.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='JDCol']"
        f"//div[@id='EmpBasicInfo']"
        f"//div[@class='infoEntity'][label='Size']"
        f"//span[@class='value']"
        )
    size = element.text
    browser.implicitly_wait(5)

    # Get company url.
    try:
        element = browser.find_element_by_xpath(
            f"//div[@id='PageContent']"
            f"//div[@id='JDCol']"
            f"//div[@class='noMarg padTopSm padBot']"
            f"//span[@class='value website']"
            f"//a[@class='link']"
            )
        url = element.get_attribute('href')
    except NoSuchElementException:
        url = 'NA'
        pass
    browser.implicitly_wait(5)

    return size, url