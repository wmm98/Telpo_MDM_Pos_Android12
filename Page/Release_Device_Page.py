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

    def login_release_version(self, user_info):
        self.login_ok(user_info["username"], user_info["password"])

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
