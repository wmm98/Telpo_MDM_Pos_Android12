from utils.base_web_driver import BaseWebDriver
from Common.check_yaml_file import CheckYaml
from utils.base_web_driver import BaseWebDriver
from Common import Shell
from Common import Log
import shutil
import time
import datetime
import allure
from Page.OTA_Page import OTAPage
from Page.Devices_Page import DevicesPage
from Page.Apps_Page import APPSPage
from Conf.Config import Config
from Common.DealAlert import AlertData
import pytest
from utils.client_connect import WIFIADBConnect
from Page.MDM_Page import MDMPage
from Page.Andriod_Aimdm_Page_WIFI import AndroidAimdmPageWiFi
from Page.Catch_Log_Page import CatchLogPage
from Page.Content_Page import ContentPage
from Common.Get_Lan_ips import GetLanIps
from Common.simply_case import Optimize_Case
import threading
from selenium.webdriver.support import expected_conditions as EC

yaml_data = Config().get_yaml_data()['MDMTestData']
user_info = {"username": yaml_data['website_info']['test_user'],
             "password": yaml_data['website_info']['test_password']}

lan_ips = GetLanIps()



