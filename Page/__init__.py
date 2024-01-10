from selenium.common import TimeoutException, StaleElementReferenceException, ElementNotInteractableException, UnexpectedAlertPresentException
from datetime import datetime
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Conf.Config import Config
from Common.Log import MyLog
import time as t_time
import os
import re
from Common import Shell
import requests
from androguard.core.bytecodes.apk import APK
import uiautomator2 as u2
from uiautomator2.exceptions import UiaError
import allure
import hashlib
from PIL import Image
from Common.DealAlert import AlertData
import socket
from ping3 import ping
import threading
from Common.Serial import Serial
from adbutils import AdbError
import shutil


yaml_data = Config().get_yaml_data()['MDMTestData']


js_telpo_support = "document.getElementsByClassName(\"globalClass_f38a\")[0].style.display=\"none\""
js_load_status = 'return document.readyState;'
js_release_tips = "$('.introjs-overlay').click()"


