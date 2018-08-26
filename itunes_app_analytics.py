## Itunes App Analytics Data Fetcher
## Authord: D.Kisler <admin@dkisler.de>

import time
import os
import sys
dir_mod = os.path.dirname(__file__)
if dir_mod not in sys.path:
    sys.path.insert(0, dir_mod)
from selenium_chrome_driver import browser

# appstore analytics metrics
class Params:
    """Class with the inputs for the Itunes Analytics App"""
    measure = {'impressions': 'impressionsTotalUnique', 
               'views':'pageViewUnique', 
               'downloads':'units', 
               'installs':'installs', 
               'sessions':'sessions', 
               'ad':'activeDevices', 
               'crash':'crashes',
               'purchases':'iap', 
               'bookings':'sales', 
               'pu':'payingUsers'}
    # time window - interval
    interval = {'day':'d', 'week':'w', 'month': 'm'}
    # zoom
    zoom = {'day':'day', 'week':'week', 'month': 'month'}
    # view by
    viewby = {
        'device':2,
        'os_ver':4,
        'region':7,
        'territory':1,
        'traffic_source':12,
        'app_referrar':13,
        'web_referrar':6
    }
    
## login
class Login:
    """Login into appstore connect"""
    ## button on login page
    def __login_button(self):
        """Function to trigger apply button on the login page, https://appstoreconnect.apple.com/login
        ___
        Required:
        browser - selenium browser
        """
        button = browser.find_element_by_id('sign-in')
        button.click()
        time.sleep(.5)

    ## login into apple itunes analytics
    def __init__(self, user, password):
        """
        Required:
        user, password - credentials for itunes analytics app
        """
        browser.get('https://appstoreconnect.apple.com')
        time.sleep(5)
        browser.switch_to_frame('aid-auth-widget-iFrame')
        # enter login
        appleID = browser.find_element_by_id('account_name_text_field')
        appleID.send_keys(user)
        time.sleep(.5)
        self.__login_button()
        # enter password
        passwd = browser.find_element_by_id('password_text_field')
        passwd.send_keys(password)
        time.sleep(.5)
        self.__login_button()
        
class DataFetcher:
    """CSV Files Fetcher from  Itunes Analytics App"""
    def output_dir(download_dir = '/tmp'):
        """Method to enable headless files download by google chrome into selected directory
        ___
        Required:
        download_dir - dir to save files into
        """
        browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = browser.execute("send_command", params)

    def download(app_id, measure, interval, zoom, date, viewby = None):
        """Method to start downloading data
        ___
        Required:
        app_id - itunes app ID
        measure - analytics metric: AppAnalyticsParams.measure
        interval - time window: AppAnalyticsParams.interval, e.g. 'd'
        zoom - time zoom: AppAnalyticsParams.zoom, e.g. 'day'
        date - date to fetch data for, e.g. '201801'
        viewby - metric broken down by some meta data, AppAnalyticsParams.viewby, e.g. OS version
        """
        if viewby is None:
            url = 'https://analytics.itunes.apple.com/#/metrics?interval={}&datesel={}&zoom={}&measure={}&type=line&app={}'.format(interval, date, zoom, measure, app_id)
        else:
            url = 'https://analytics.itunes.apple.com/#/metrics?interval={}&datesel={}&zoom={}&measure={}&type=line&app={}&view_by={}'.format(interval, date, zoom, measure, app_id, viewby)
        # access analytics app
        browser.get(url)
        time.sleep(10)
        # click download data
        downloadData = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[3]')
        downloadData.click()
