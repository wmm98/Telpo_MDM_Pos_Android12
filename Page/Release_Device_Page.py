import Page as public_pack
from Page.Devices_Page import DevicesPage
from Page.MDM_Page import MDMPage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time

log = public_pack.MyLog()


class ReleaseDevicePage(DevicesPage, MDMPage):

    def __init__(self, driver, times):
        DevicesPage.__init__(self, driver, times)
        self.driver = driver

    def login_release_version(self, user_info, login_ok_title):
        # username = "ceshibu03"
        # password = "123456"

        # login_ok_title = "Telpo MDM"
        # login_ok_url = "http://test.telpoai.com/device/map"
        # now_time = self.get_current_time()
        # while True:
        #     self.input_user_name(user_info["username"])
        #     self.input_pwd_value(user_info["password"])
        #     self.choose_agree_btn()
        #     self.click_login_btn()
        #     text = self.get_alert_text()
        #     if "success" in text:
        #         break
        #     else:
        #         self.refresh_page()
        #     if self.get_current_time() > self.return_end_time(now_time):
        #         e = "@@@@ 3分钟内多次登录， 登录失败， 请检查！！！"
        #         log.error(e)
        #         assert False, e
        #     self.refresh_page()
        #     self.time_sleep(1)
        now_time = self.get_current_time()
        # while True:
        self.login_ok(user_info["username"], user_info["password"])
            # self.input_user_name(user_info["username"])
            # self.input_pwd_value(user_info["password"])
            # self.choose_agree_btn()
            # self.click_login_btn()
            # try:
            #     if self.web_driver_wait_until(public_pack.EC.url_contains("device"), 10):
            #         break
            # except Exception:
            #     if "device" in self.get_current_window_url():
            #         break
            # if self.get_current_time() > self.return_end_time(now_time, 180):
            #     assert False, "无法登录，请检查！！！"
            # self.time_sleep(1)
            # self.refresh_page()

    def go_to_device_page(self, top_title):
        self.click_devices_btn()
        now_time = self.get_current_time()
        while True:
            if top_title in self.get_loc_main_title():
                break
            else:
                self.click_devices_btn()
            if self.get_current_time() > self.return_end_time(now_time):
                e = "@@@@ 3分钟内多次加载页面， 加载失败， 请检查！！！"
                log.error(e)
                assert False, e
            self.time_sleep(1)

    def get_single_device_list_release(self, sn):
        self.search_device_by_sn(sn)
        devices_list = self.get_dev_info_list()
        return devices_list
