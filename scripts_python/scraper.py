import os, sys, inspect

import numpy as np
import pandas as pd


import matplotlib
from matplotlib import pyplot as plt

import collections
import time
import datetime

import re
import hashlib

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
from selenium.webdriver.support.ui import WebDriverWait

working_dir = os.path.dirname(
    os.path.abspath(
        inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(working_dir)
sys.path.insert(0, parent_dir)

from scripts_python import scraper as scr


WAIT_TIME = 10


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
        ) -> selenium.webdriver.chrome.webdriver.WebDriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_driver_path = '../webdrivers/chromedriver'
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path=chrome_driver_path)
    driver.implicitly_wait(WAIT_TIME)
    return driver


def get_clickable_element(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        xpath: str):
    element = WebDriverWait(
        driver, WAIT_TIME).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)))
    return element


def get_element_when_present(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        xpath: str):
    try:
        element = WebDriverWait(
            driver, WAIT_TIME).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)))
    except TimeoutException:
        element = None
    return element


def get_element_text_when_present(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        xpath: str):
    element = get_element_when_present(driver=driver, xpath=xpath)
    if element is not None:
        text = element.text
    else:
        text = 'NA'
    return text


# SCRAPE GLASSDOOR ============================================================
def load_main_page(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        url: str = 'https://www.glassdoor.co.uk',
        ):

    print(url)
    driver.get(url)
    driver.implicitly_wait(10)


def accept_cookies(
        driver: selenium.webdriver.chrome.webdriver.WebDriver
        ):
    # Click 'Accept'.

    xpath = (
        f"//div[@id='_evidon_banner']"
        f"//button[@id='_evidon-accept-button']")
    element = get_clickable_element(
        driver=driver, xpath=xpath)

    element.click()
    driver.implicitly_wait(10)


def sign_in(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        e_mail: str,
        password: str,
        ):

    # Click 'Sign In'.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@class='locked-home-sign-in']"
        f"//a[@class='track-click gd-btn-locked-transparent susiLink sign-in strong nowrap']"
        )
    element = get_clickable_element(
        driver=driver, xpath=xpath)
    element.click()

    # Enter e-mail.
    xpath = (
        f"//div[@class='modal_content']"
        f"//input[@id='userEmail']"
        )
    element = get_clickable_element(
        driver=driver, xpath=xpath)
    element.click()
    element.send_keys(e_mail)

    # Enter password.
    xpath = (
        f"//div[@class='modal_content']"
        f"//input[@id='userPassword']"
        )
    element = get_clickable_element(
        driver=driver, xpath=xpath)
    element.click()
    element.send_keys(password)
    element.send_keys(u'\ue007')  # click 'Enter'


def do_search(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        keywords: str,
        location: str,
        ):
    # Enter 'Job Title, Keywords or Company'.
    xpath = (
        f"//div[@class='search-bar ']"
        f"//input[@class='keyword']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.clear()
    element.click()

    element.send_keys(keywords)

    # Enter 'Location'.
    xpath = (
        f"//div[@class='search-bar ']"
        f"//input[@class='loc']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.clear()
    element.click()
    driver.implicitly_wait(10)
    element.send_keys(location)

    # Click 'Search'.
    xpath = (
        f"//div[@class='search-bar ']"
        f"//button[@class='gd-btn-mkt']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()


def set_filters(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        jobtype: str,
        post_age: str,
        radius: str,
        ):

    # Set job type.
    xpath = (
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='JOBTYPE'][@id='filter_jobType']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()

    xpath = (
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{jobtype}']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()
    
    # Set date posted.
    xpath = (
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='DATEPOSTED'][@id='filter_fromAge']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()

    xpath = (
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{post_age}']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()

    # Set distance.
    xpath = (
        f"//div[@class='selectDynamicFilters']"
        f"//div[@data-test='DISTANCE'][@id='filter_radius']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()

    xpath = (
        f"//div[@id='JobSearch']"
        f"//div[@id='PrimaryDropdown']"
        f"//li[@value='{radius}']"
        )
    element = get_clickable_element(driver=driver, xpath=xpath)
    element.click()


def switch_to_next_page(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        ):
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='ResultsFooter']"
        f"//li[@class='next']"
        )
    try:
        element = get_clickable_element(driver=driver, xpath=xpath)
        element.click()
    except:
        pass


def get_company_name_and_rating(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:
    element = driver.find_element_by_xpath(
        f"//div[@id='PageContent']"
        f"//div[@id='JobResults']"
        f"//div[@class='employerName']"
        )
    try:
        name, rating = element.text.split('\n')
        rating = float(rating)
    except ValueError:
        name = element.text.split('\n')[0]
        rating = 'NA'
    return name, rating


def get_job_title_and_description(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:
    
    # Get job title.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='JobResults']"
        f"//div[@class='title']"
        )
    job_title = get_element_text_when_present(driver=driver, xpath=xpath)

    # Get job description.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='Details']"
        f"//div[@class='jobDescriptionContent desc']"
        )
    job_description = get_element_text_when_present(driver=driver, xpath=xpath)

    return job_title, job_description

def get_company_size_and_url(
        driver: selenium.webdriver.chrome.webdriver.WebDriver,
        ) -> tuple:

    # Switch to company data.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='JDCol']"
        f"//div[@class='scrollableTabs']"
        f"//div[@data-tab-type='overview']"
        )
    try:
        element = get_clickable_element(driver=driver, xpath=xpath)
    except:
        size = 'NA'
        url = 'NA'
        return size, url

    # Get company size.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='JDCol']"
        f"//div[@id='EmpBasicInfo']"
        f"//div[@class='infoEntity'][label='Size']"
        f"//span[@class='value']"
        )
    size = get_element_text_when_present(driver=driver, xpath=xpath)

    # Get company url.
    xpath = (
        f"//div[@id='PageContent']"
        f"//div[@id='JDCol']"
        f"//div[@class='noMarg padTopSm padBot']"
        f"//span[@class='value website']"
        f"//a[@class='link']"
        )
    element = get_element_when_present(driver=driver, xpath=xpath)
    if element is not None:
        url = element.get_attribute('href')
    else:
        url = 'NA'

    return size, url