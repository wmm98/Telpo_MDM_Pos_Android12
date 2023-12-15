from utils.base_web_driver import BaseWebDriver
from selenium.webdriver.support import expected_conditions as EC
from Page.MDM_Page import MDMPage
from Common.Log import MyLog
from Common import Log
from Page.OTA_Page import OTAPage
from Page.Devices_Page import DevicesPage
from Page.Message_Page import MessagePage
from Page.Telpo_MDM_Page import TelpoMDMPage
from Common.excel_data import ExcelData
from Conf.Config import Config
from Common.simply_case import Optimize_Case
from Common.DealAlert import AlertData
from Page.Release_Device_Page import ReleaseDevicePage
from Page.System_Page import SystemPage
from Page.Apps_Page import APPSPage
import time
from Page.Android_Aimdm_Page import AndroidAimdmPage
from Page.Andriod_Aimdm_Page_WIFI import AndroidAimdmPageWiFi
from Page.Catch_Log_Page import CatchLogPage
from Page.Content_Page import ContentPage
from utils.client_connect import ClientConnect
from Common.Serial import Serial
from Common.Shell import Shell
from Page.Android_Page_USB import AndroidBasePageUSB

yaml_data = Config().get_yaml_data()['MDMTestData']

client = ClientConnect().get_device()
usb_device_info = {"device": client, "serial": client.serial}
# connect wifi adb
connect = ClientConnect()
# connect.wifi_connect_device()
serial_no = client.serial
# wifi_client = connect.get_wifi_device()
# wifi_ip = connect.get_wifi_ip()
wifi_ip = serial_no
# wifi_device_info = {"device": wifi_client, "ip": wifi_ip}
wifi_device_info = {"device": client, "ip": wifi_ip}
device_data = {"usb_device_info": usb_device_info, "wifi_device_info": wifi_device_info}

user_info = {"username": yaml_data['website_info']['test_user'],
             "password": yaml_data['website_info']['test_password']}

#
chrome_driver = BaseWebDriver()
test_driver = chrome_driver.get_web_driver()

# check if exist sim card
# android_usb = AndroidBasePageUSB(client, 5, usb_device_info["serial"])
# android_usb.open_mobile_data()
# android_usb.confirm_wifi_status_close()
# # time.sleep(5)
# try:
#     android_usb.ping_network(timeout=180)
#
# except AssertionError as e:
#     raise Exception("没有流量卡，请插上流量卡！！！")
# android_usb.confirm_wifi_status_open()


