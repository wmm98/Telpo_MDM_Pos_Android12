import TestCase
import allure
import pytest

log = TestCase.MyLog()
test_yaml = TestCase.yaml_data
conf = TestCase.Config()
opt_case = TestCase.Optimize_Case()


class TestLogin:

    def setup_class(self):
        self.api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yaml["work_app"]["api_txt"]
        self.driver = TestCase.test_driver
        self.mdm_page = TestCase.MDMPage(self.driver, 40)
        self.app_page = TestCase.APPSPage(self.driver, 40)
        self.ota_page = TestCase.OTAPage(self.driver, 40)
        self.device_page = TestCase.DevicesPage(self.driver, 40)
        self.android_mdm_page = TestCase.AndroidAimdmPage(TestCase.device_data, 5)
        self.android_mdm_page.open_usb_debug_btn()
        self.android_mdm_page.open_usb_debug_btn()
        self.android_mdm_page.screen_keep_on()
        self.android_mdm_page.rotation_freeze(freeze=True)
        self.wifi_ip = TestCase.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.back_to_home()
        self.wait_times = 10
        self.wifi_flag = 0

    def teardown_class(self):
        pass
        # self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('MDM_test02_login')
    @allure.title("连接上wifi/登录--辅助测试用例")  # 设置case的名字
    @pytest.mark.dependency(name="test_login_ok", scope='package')
    @pytest.mark.flaky(reruns=2, reruns_delay=3)
    def test_connect_wifi_and_login_ok(self):
        while True:
            try:
                self.android_mdm_page.screen_keep_on()
                if self.android_mdm_page.get_current_wlan() is None:
                    self.android_mdm_page.clear_recent_app_USB()
                    self.android_mdm_page.open_wifi_btn()
                    # self.android_mdm_page.time_sleep(5)
                    self.android_mdm_page.confirm_open_wifi_page()
                    self.android_mdm_page.confirm_wifi_switch_open()
                    self.android_mdm_page.time_sleep(5)
                    if self.android_mdm_page.get_current_wlan() is None:
                        wifi_available = test_yaml["android_device_info"]["available_wifi"]
                        wifi_list = []
                        for wifi in wifi_available:
                            wifi_list.append(wifi_available[wifi])

                        self.android_mdm_page.connect_available_wifi(wifi_list)
                        self.android_mdm_page.clear_recent_app_USB()
                self.android_mdm_page.ping_network(timeout=180)

                username = test_yaml['website_info']['test_user']
                password = test_yaml['website_info']['test_password']
                #
                self.mdm_page.login_ok(username, password)

                self.device_page.go_to_new_address("devices")
                # devices_sn = [device["SN"] for device in self.device_page.get_dev_info_list()]
                device_sn = self.android_mdm_page.get_device_sn()
                self.device_page.search_device_by_sn(device_sn)
                device_info = self.device_page.get_dev_info_list()
                device_sn = self.android_mdm_page.get_device_sn()
                devices_list = {"SN": device_sn, "name": "aut" + device_sn}
                # if device_sn not in devices_sn:
                if len(device_info) == 0:
                    # check if device model is existed, if not, add model
                    now_time = self.device_page.get_current_time()
                    while True:
                        if "automation_debug" not in self.device_page.get_models_list():
                            self.device_page.click_model()
                            self.device_page.add_model("automation_debug")
                            self.device_page.refresh_page()
                        else:
                            break
                        if self.device_page.get_current_time() > self.device_page.return_end_time(now_time, 600):
                            assert False, "@@@@无法创建分类，请检查！！！"
                        self.device_page.refresh_page()
                        self.device_page.time_sleep(2)
                    # check if device category is existed, if not, add category
                    now_time = self.device_page.get_current_time()
                    while True:
                        if not self.device_page.category_is_existed("test_debug"):
                            self.device_page.click_category()
                            self.device_page.add_category("test_debug")
                            self.device_page.refresh_page()
                        else:
                            break
                        if self.device_page.get_current_time() > self.device_page.return_end_time(now_time, 600):
                            assert False, "@@@@无法创建模型，请检查！！！"
                        self.device_page.refresh_page()
                        self.device_page.time_sleep(2)

                    now_time = self.device_page.get_current_time()
                    while True:
                        if len(self.device_page.get_dev_info_list()) == 1:
                            break
                        self.device_page.click_new_btn()
                        self.device_page.add_devices_info(devices_list, cate_model=False)
                        self.device_page.refresh_page()
                        # self.android_mdm_page.reboot_device(self.wifi_ip)
                        # self.device_page.refresh_page()
                        if self.device_page.get_current_time() > self.device_page.return_end_time(now_time, 600):
                            assert False, "@@@@无法添加设备: %s，请检查！！！" % devices_list["SN"]
                        self.device_page.refresh_page()
                        self.device_page.time_sleep(2)

                if test_yaml["android_device_info"]["install_aimdm"]:
                    self.android_mdm_page.confirm_app_installed(
                        conf.project_path + "\\Param\\Work_APP\\%s" % test_yaml["work_app"]["aidmd_apk"])
                self.android_mdm_page.push_file_to_device(self.api_path,
                                                          self.android_mdm_page.get_internal_storage_directory() + "/")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                opt_case.confirm_device_online(device_sn)
                break
            except Exception as e:
                if self.ota_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("devices", TestCase.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.go_to_new_address("devices")

    @allure.feature('MDM_test02_login1111')
    @allure.title("OTA-添加ota升级包-- 辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_add_OTA_package_and_cate(self, go_to_ota_page):
        exp_existed_text = "ota already existed"
        exp_success_text = "success"
        package_info = {"package_name": test_yaml['ota_packages_info']['package_name'], "file_category": "test",
                        "plat_form": test_yaml['ota_packages_info']['platform']}
        file_path = conf.project_path + "\\Param\\Package\\%s" % package_info["package_name"]
        ota_info = {"file_name": file_path, "file_category": package_info["file_category"],
                    "plat_form": package_info["plat_form"]}
        # check if category is existed
        while True:
            try:
                now_time = self.ota_page.get_current_time()
                while True:
                    if len(self.ota_page.get_ota_categories_list()) == 0:
                        self.ota_page.add_ota_category("test")
                        self.ota_page.refresh_page()
                    else:
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        assert False, "@@@@创建种类失败，请检查！！！！"
                    self.ota_page.time_sleep(3)
                # check if ota package is existed, if not, add package, else skip
                now_time = self.ota_page.get_current_time()
                while True:
                    self.ota_page.search_device_by_pack_name(package_info["package_name"])
                    if len(self.ota_page.get_ota_package_list()) == 0:
                        self.ota_page.click_add_btn()
                        self.ota_page.input_ota_package_info(ota_info)
                        self.ota_page.click_save_add_ota_pack(timeout=1800)
                        self.ota_page.refresh_page()
                        self.ota_page.time_sleep(5)
                        self.ota_page.search_device_by_pack_name(package_info["package_name"])
                    else:
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 3600):
                        assert False, "@@@@无法上传Ota包：%s, 请检查！！！！" % package_info["package_name"]
                    self.ota_page.refresh_page()
                    self.ota_page.time_sleep(3)
                break
            except Exception as e:
                if self.ota_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("ota", TestCase.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('MDM_test02_login1111')
    @allure.title("Apps-添加APK包--辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    # @pytest.mark.parametrize('package_info', package_infos)
    def test_add_cate_and_apps(self, go_to_app_page):
        exp_success_text = "Success"
        # package_info = {"package_name": "Bus_Recharge_System_1.0.1_20220615.apk", "file_category": "test",
        #                 "developer": "engineer", "description": "test"}
        apks = test_yaml["app_info"]
        # apks.update(test_yml["system_app"])
        # print(apks)
        while True:
            try:
                for apk in list(apks.values()):
                    file_path = conf.project_path + "\\Param\\Package\\%s" % apk
                    now_time = self.app_page.get_current_time()
                    while True:
                        if self.app_page.get_app_categories_list() == 0:
                            self.app_page.add_app_category("test")
                        else:
                            break
                        if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 600):
                            assert False, "@@@@无法创建分类，请检查！！！！"
                        self.app_page.refresh_page()
                        self.app_page.time_sleep(3)

                    now_time = self.app_page.get_current_time()
                    while True:
                        self.app_page.search_app_by_name(apk)
                        if len(self.app_page.get_apps_text_list()) == 0:
                            self.app_page.click_add_btn()
                            self.app_page.input_app_info(file_path)
                            self.app_page.refresh_page()
                        else:
                            break
                        if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 600):
                            assert False, "@@@@无法上传 app：%s，请检查！！！！" % apk
                        self.app_page.time_sleep(3)
                break
            except Exception as e:
                if self.ota_page.service_is_normal():
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps", TestCase.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.go_to_new_address("apps")
