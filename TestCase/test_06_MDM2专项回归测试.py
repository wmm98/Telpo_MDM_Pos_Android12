import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
usb_serial = case_pack.Serial()

package_infos = [{"package_name": test_yml['app_info']['low_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['high_version_app'], "file_category": "test",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app'], "file_category": "test01",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_A'], "file_category": "test01",
                  "developer": "engineer", "description": "test"},
                 {"package_name": test_yml['app_info']['other_app_limit_network_B'], "file_category": "test01",
                  "developer": "engineer", "description": "test"}
                 ]


class TestMDM2SpecialPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.content_page = case_pack.ContentPage(self.driver, 40)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_content_file()
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)
        self.content_page.refresh_page()
        self.silent_ota_upgrade_flag = 0

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_all_content_file()
        self.app_page.refresh_page()
        # self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('Special_Test-case0')
    @allure.title("public case-添加 content 种类--辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_add_content_category_MDM2(self, recover_and_login_mdm, go_to_content_page):
        while True:
            try:
                log.info("===================添加 content 种类--辅助测试用例开始==================")
                now_time = self.content_page.get_current_time()
                while True:
                    self.content_page.refresh_page()
                    if len(self.content_page.get_content_categories_list()) != 0:
                        break
                    self.content_page.new_content_category("test-debug")
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 300):
                        assert False, "@@@@无法创建新的分类， 请检查！！！"
                    self.content_page.time_sleep(3)
                log.info("===================添加 content 种类--辅助测试用例结束==================")
                break
            except Exception as e:
                if self.device_page.service_is_normal("content", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")

    @allure.feature('Special_Test-case0')
    @allure.title("public case-添加 content 文件--辅助测试用例")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_add_content_file_MDM2(self, recover_and_login_mdm, go_to_content_page):
        while True:
            try:
                log.info("public case-添加 content 文件--辅助测试用例开始")
                self.content_page.refresh_page()
                file_path = conf.project_path + "\\Param\\Content\\"
                # content_name_list = self.content_page.get_content_list()
                for test_file in test_yml["Content_info"].values():
                    for file_name in test_file:
                        # if file_name not in content_name_list:
                        if "file" in file_name:
                            # pass
                            now_time = self.content_page.get_current_time()
                            while True:
                                self.content_page.search_content('Normal Files', file_name)
                                self.content_page.time_sleep(5)
                                if len(self.content_page.get_content_list()) == 1:
                                    self.content_page.refresh_page()
                                    # print("11111111111111111111111111111")
                                    break
                                self.content_page.refresh_page()
                                self.content_page.time_sleep(3)
                                self.content_page.add_content_file("normal_file", file_path + file_name)
                                self.content_page.time_sleep(3)
                                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time,
                                                                                                            600):
                                    assert False, "@@@无法上传文件：%s" % file_name

                        elif "bootanimation" in file_name:
                            now_time = self.content_page.get_current_time()
                            while True:
                                self.content_page.search_content('Boot Animations', file_name)
                                self.content_page.time_sleep(5)
                                if len(self.content_page.get_content_list()) == 1:
                                    self.content_page.refresh_page()
                                    break
                                self.content_page.refresh_page()
                                self.content_page.time_sleep(3)
                                self.content_page.add_content_file("boot_animation", file_path + file_name, timeout=700)
                                self.content_page.time_sleep(2)
                                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time,
                                                                                                            600):
                                    assert False, "@@@无法上传文件：%s" % file_name

                        elif "background" in file_name:
                            now_time = self.content_page.get_current_time()
                            while True:
                                self.content_page.search_content('Wallpaper', file_name)
                                self.content_page.time_sleep(5)
                                if len(self.content_page.get_content_list()) == 1:
                                    self.content_page.refresh_page()
                                    break
                                self.content_page.refresh_page()
                                self.content_page.time_sleep(3)
                                self.content_page.add_content_file("wallpaper", file_path + file_name)
                                self.content_page.time_sleep(3)
                                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time,
                                                                                                            600):
                                    assert False, "@@@无法上传文件：%s" % file_name

                        elif "logo" in file_name:
                            now_time = self.content_page.get_current_time()
                            while True:
                                self.content_page.search_content('LOGO', file_name)
                                self.content_page.time_sleep(5)
                                if len(self.content_page.get_content_list()) == 1:
                                    self.content_page.refresh_page()
                                    break
                                self.content_page.refresh_page()
                                self.content_page.time_sleep(3)
                                self.content_page.add_content_file("logo", file_path + file_name)
                                self.content_page.time_sleep(3)
                                if self.content_page.get_current_time() > self.content_page.return_end_time(now_time,
                                                                                                            600):
                                    assert False, "@@@无法上传文件：%s" % file_name

                log.info("public case-添加 content 文件--辅助测试用例开始结束")
                break
            except Exception as e:
                if self.device_page.service_is_normal("content", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")

    @allure.feature('Special_Test-case1')
    @allure.title("需要测试时回归测试- 系统/应用日志的抓取")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_cat_logs_regression_MDM2(self, recover_and_login_mdm, go_to_and_return_device_page):
        # durations = [5, 10, 30]
        durations = [5]
        while True:
            try:
                log.info("*****************日志的抓取用例开始********************")
                opt_case.confirm_device_online(self.device_sn)
                for duration in durations:
                    exp_log_msg = "Device Debug Command sent"
                    sn = self.device_sn
                    # self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.device_page.refresh_page()
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(case_pack.time.time()))
                    opt_case.catch_logs(sn, duration, time_out=duration * 200)
                    log.info("捕捉%d分钟日志指令下达" % duration)
                    # check if device log generates and upload to allure report
                    self.android_mdm_page.generate_and_upload_log(send_time, "%dmin_" % duration)
                    log.info("***************日志的抓取用例结束******************")
                break
            except Exception as e:
                if self.device_page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.device_page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.device_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case2')
    @allure.story('MDM-Show')
    @allure.title("public case-应用满屏推送--请在附件查看满屏截图效果")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=100, reruns_delay=3)
    def test_release_app_full_screen_MDM2(self, recover_and_login_mdm, del_all_app_release_log,
                                          del_all_app_uninstall_release_log, go_to_app_page,
                                          uninstall_multi_apps):
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        while True:
            try:
                log.info("*******************应用满屏推送用例开始***************************")
                self.android_mdm_page.screen_keep_on()
                file_path = self.app_page.get_apk_path(release_info["package_name"])
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version
                # 压测添加的方法
                # self.app_page.delete_and_upload(release_info["package_name"], file_path)
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                self.app_page.go_to_new_address("devices")
                opt_case.confirm_device_online(self.device_sn)

                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % app_size)
                # check file hash value in directory Param/package
                act_apk_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"])
                log.info("原始包的MD5值为: %s" % act_apk_package_hash_value)
                # go to app page
                self.app_page.go_to_new_address("apps")
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info, kiosk_mode=True)

                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        log.info("存在app：%s的下载记录" % shell_app_apk_name)
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                print("**********************下载记录检测完毕*************************************")
                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原始包的MD5值为: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("设备下载ota 包的下载记录: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        log.info("终端检测到ota包下载完成")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        raise Exception("@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        # assert False, "@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(20)
                log.info("**********************终端下载完成检测完毕*************************************")

                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        raise Exception("@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        # assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                log.info("**********************终端安装完毕*************************************")

                self.app_page.time_sleep(5)
                self.app_page.go_to_new_address("apps/logs")
                report_now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的升级状态： %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            log.info("平台上报升级完成")
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 3):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            print("===================服务崩溃了==================================")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            print("===================服务器恢复了==================================")
                            report_now_time = self.app_page.get_current_time()

                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)

                log.info("*******************静默安装完成***************************")

                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                log.info("当前运行的app为： %s" % release_info["package_name"])
                base_directory = "APP_Full_Screen"
                image_before_reboot = "%s\\app_full_screen_before_reboot.jpg" % base_directory
                self.android_mdm_page.save_screenshot_to(image_before_reboot)
                self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_before_reboot,
                                                       "app_full_screen_before_reboot")
                log.info("重启设备")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("设备启动完成")
                self.android_mdm_page.confirm_app_start(release_info["package"])
                image_after_reboot = "%s\\app_full_screen_after_reboot.jpg" % base_directory
                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                log.info("当前运行的app为： %s" % release_info["package_name"])
                self.android_mdm_page.save_screenshot_to(image_after_reboot)
                self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_reboot,
                                                       "app_full_screen_after_reboot")
                self.android_mdm_page.stop_app(release_info["package"])
                log.info("*******************应用满屏推送用例结束***************************")
                assert False
            except Exception as e:
                if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.app_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case3')
    @allure.story('MDM-Show')
    @allure.title("public case-推送壁纸--请在附件查看壁纸截图效果")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_release_wallpaper_MDM2(self, recover_and_login_mdm, unlock_screen, del_all_content_release_logs):
        while True:
            try:
                log.info("*******************推送壁纸用例开始***************************")
                self.android_mdm_page.back_to_home()
                self.android_mdm_page.time_sleep(3)
                base_directory = "Wallpaper"
                org_wallpaper = "%s\\org_wallpaper.jpg" % base_directory
                self.android_mdm_page.save_screenshot_to(org_wallpaper)
                self.android_mdm_page.upload_image_JPG(
                    conf.project_path + "\\ScreenShot\\%s" % org_wallpaper, "original_wallpaper")
                wallpapers = test_yml["Content_info"]["wallpaper"]
                i = 0
                for paper in wallpapers:
                    i += 1
                    opt_case.confirm_device_online(self.device_sn)
                    self.content_page.go_to_new_address("content")
                    file_path = conf.project_path + "\\Param\\Content\\%s" % paper
                    file_size = self.content_page.get_file_size_in_windows(file_path)
                    log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                    file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s" % paper, directory="Content")
                    log.info("file_hash_value: %s" % str(file_hash_value))

                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(self.content_page.get_current_time()))
                    self.content_page.time_sleep(10)
                    self.content_page.search_content('Wallpaper', paper)
                    release_info = {"sn": self.device_sn, "content_name": paper}
                    self.content_page.time_sleep(3)
                    if len(self.content_page.get_content_list()) == 1:
                        self.content_page.release_content_file(self.device_sn)
                        log.info("推送指令下达成功")
                        # check release record in device
                        now_time = self.content_page.get_current_time()
                        while True:
                            if self.android_mdm_page.download_file_is_existed(paper):
                                log.info("终端存在壁纸：%s 的下载记录" % paper)
                                break
                            if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                                log.error("@@@@终端没有壁纸: %s的下载记录" % paper)
                                assert False, "@@@@终端没有壁纸: %s的下载记录" % paper
                            self.content_page.time_sleep(3)
                        log.info("检测upgrade log")
                        # check upgrade log
                        # check if the upgrade log appeared, if appeared, break
                        self.content_page.go_to_new_address("content/log")
                        # check the app action in app upgrade logs, if download complete or upgrade complete, break
                        download_time = self.content_page.get_current_time()
                        while True:
                            upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                            if len(upgrade_list) != 0:
                                action = upgrade_list[0]["Action"]
                                log.info("平台upgrade log状态： %s" % action)
                                if self.content_page.get_action_status(
                                        action) == 2 or self.content_page.get_action_status(
                                    action) == 7:
                                    # check the app size in device, check if app download fully
                                    size = self.android_mdm_page.get_file_size_in_device(paper)
                                    log.info("终端下载后的的size大小： %s" % str(size))
                                    assert file_size == size, "@@@@平台显示下载完成， 终端的包下载不完整，请检查！！！"
                                    log.info("壁纸前后对比大小一致")
                                    assert file_hash_value == self.android_mdm_page.calculate_sha256_in_device(paper)
                                    log.info("文件前后的hash256值一致")
                                    break
                            # wait 20 min
                            if self.content_page.get_current_time() > self.content_page.return_end_time(download_time,
                                                                                                        1200):
                                if self.content_page.service_is_normal("content/log", case_pack.user_info):
                                    log.error("@@@@20分钟还没有下载完相应的文件， 请检查！！！")
                                    assert False, "@@@@20分钟还没有下载完相应的文件， 请检查！！！"
                                else:
                                    self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                    download_time = self.content_page.get_current_time()
                            self.content_page.time_sleep(5)
                            self.content_page.refresh_page()
                        log.info("*************************壁纸：%s 下载完毕*****************************" % paper)
                        # check upgrade
                        report_time = self.content_page.get_current_time()
                        while True:
                            upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                            if len(upgrade_list) != 0:
                                action = upgrade_list[0]["Action"]
                                log.info("平台显示的状态： %s" % action)
                                if self.content_page.get_action_status(action) == 7:
                                    log.info("平台显示已经设置完成壁纸")
                                    break
                            # wait upgrade 3 min at most
                            if self.content_page.get_current_time() > self.content_page.return_end_time(report_time,
                                                                                                        180):
                                if self.content_page.service_is_normal("content/log", case_pack.user_info):
                                    log.error("@@@@3分钟还没有设置完相应的壁纸， 请检查！！！")
                                    assert False, "@@@@3分钟还没有设置完相应的壁纸， 请检查！！！"
                                else:
                                    self.content_page.recovery_after_service_unavailable("content/log",
                                                                                         case_pack.user_info)
                                    report_time = self.content_page.get_current_time()
                            self.content_page.time_sleep(5)
                            self.content_page.refresh_page()
                        log.info("*************壁纸：%s 平台显示已经设置完成***********" % paper)
                        wallpaper_before_reboot = "%s\\wallpaper.jpg" % base_directory
                        self.android_mdm_page.save_screenshot_to(wallpaper_before_reboot)
                        self.android_mdm_page.upload_image_JPG(
                            conf.project_path + "\\ScreenShot\\%s" % wallpaper_before_reboot,
                            "wallpaper_before_reboot-%s" % str(i))
                        # no test tomorrow to save time
                        self.android_mdm_page.reboot_device(self.wifi_ip)
                        wallpaper_after_reboot = "%s\\wallpaper_after_reboot.jpg" % base_directory
                        self.android_mdm_page.save_screenshot_to(wallpaper_after_reboot)
                        self.android_mdm_page.upload_image_JPG(
                            conf.project_path + "\\ScreenShot\\%s" % wallpaper_after_reboot,
                            "wallpaper_after_reboot-%s" % str(i))
                    else:
                        log.error("@@@@平台上没有该壁纸： %s, 请检查" % paper)
                        assert False, "@@@@平台上没有该壁纸： %s, 请检查" % paper
                log.info("*******************推送壁纸用例结束***************************")
                break
            except Exception as e:
                if self.device_page.service_is_normal("content", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.content_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.go_to_new_address("content")
                    self.content_page.delete_all_content_release_log()
                    self.android_mdm_page.del_all_content_file()
                    self.android_mdm_page.screen_keep_on()

    @allure.feature('Special_Test-case4')
    @allure.title("public case- 静默ota升级")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_silent_ota_upgrade_MDM2(self, recover_and_login_mdm, real_ota_package_operation, del_all_ota_release_log, delete_ota_package_relate):
        while True:
            try:
                log.info("*******************静默ota升级用例开始***************************")
                release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                                "silent": 0, "category": "NO Limit", "network": "NO Limit"}
                download_tips = "Foundanewfirmware,whethertoupgrade?"
                upgrade_tips = "whethertoupgradenow?"
                self.android_mdm_page.reboot_device(self.wifi_ip)
                opt_case.confirm_device_online(self.device_sn)
                self.ota_page.go_to_new_address("ota")
                self.android_mdm_page.del_updated_zip()
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                try:
                    assert self.ota_page.transfer_version_into_int(
                        current_firmware_version) < self.ota_page.transfer_version_into_int(
                        release_info["version"]), \
                        "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                except AttributeError as e:
                    log.info("*******************静默ota升级用例结束***************************")
                    if self.silent_ota_upgrade_flag == 1:
                        assert True
                    else:
                        assert False, e

                # reboot
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("成功重启设备")
                # search package
                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("设备当前固件版本：%s" % device_current_firmware_version)
                log.info("目标固件版本为 %s :" % release_info["version"])
                ota_package_size = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"])
                log.info("原始文件的hash值 ota_package_hash_value： %s" % str(act_ota_package_hash_value))
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_size)
                log.info("原始文件的大小（bytes）： %s" % str(act_ota_package_size))
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                self.ota_page.input_release_OTA_package(release_info, is_silent=True)
                log.info("推送ota package 指令下达成功")
                # check download record in device
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("终端检测到 %s 的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]
                    self.ota_page.time_sleep(10)

                self.silent_ota_upgrade_flag = 1

                self.ota_page.go_to_new_address("ota/log")
                upgrade_flag = 0
                download_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台upgrade log action: %s" % action)
                        if self.ota_page.get_action_status(action) in [2, 3, 4]:
                            log.info("*****************平台upgrade log显示ota安装包下载完成*****************")
                            if action == 4:
                                log.info("*****************平台upgrade log显示ota升级成功*****************")
                                upgrade_flag = 1
                            break
                    # wait upgrade 3 min at most
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(download_time, 1800):
                        self.silent_ota_upgrade_flag = 1
                        if self.ota_page.service_is_normal("ota/log", case_pack.user_info):
                            log.error("@@@@30分钟还没有下载完相应的固件， 请检查！！！")
                            assert False, "@@@@30分钟还没有下载完相应的固件， 请检查！！！"
                        else:
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            download_time = self.app_page.get_current_time()
                    self.ota_page.time_sleep(30)
                    self.ota_page.refresh_page()

                if upgrade_flag == 0:
                    self.ota_page.refresh_page()
                    report_time = self.ota_page.get_current_time()
                    while True:
                        info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                        if len(info) != 0:
                            action = info[0]["Action"]
                            log.info("平台upgrade log action: %s" % action)
                            if self.ota_page.get_action_status(action) == 4:
                                log.info("*****************平台upgrade log显示ota升级成功*****************")
                                break
                        # wait upgrade 3 min at most
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_time, 600):
                            if self.ota_page.service_is_normal("ota/log", case_pack.user_info):
                                log.error("@@@@30分钟还没有升级相应的ota包， 请检查！！！")
                                assert False, "@@@@30分钟还没有升级相应的ota包， 请检查！！！"
                            else:
                                self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                                report_time = self.ota_page.get_current_time()
                        self.ota_page.time_sleep(30)
                        self.ota_page.refresh_page()
                log.info("************************平台显示ota安装升级完成完成*************************************")
                self.android_mdm_page.time_sleep(5)
                self.android_mdm_page.device_boot(self.wifi_ip)
                log.info("设备启动成功")
                after_upgrade_version = self.android_mdm_page.check_firmware_version()
                log.info("设备升级后的固件版本：%s" % after_upgrade_version)
                # assert self.ota_page.transfer_version_into_int(
                #     device_current_firmware_version) != self.ota_page.transfer_version_into_int(after_upgrade_version), \
                #     "@@@@ota升级失败， 还是原来的版本%s！！" % device_current_firmware_version
                # assert self.ota_page.transfer_version_into_int(release_info["version"]) == \
                #        self.ota_page.transfer_version_into_int(
                #            after_upgrade_version), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
                assert self.ota_page.remove_space(str(after_upgrade_version)) == self.ota_page.remove_space(
                    release_info["version"]), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
                log.info("*******************静默ota升级用例结束***************************")
                break
            except Exception as e:
                if self.ota_page.service_is_normal("ota", case_pack.user_info):
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.content_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.ota_page.go_to_new_address("ota")
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()

    @allure.feature('Special_Test-case5')
    @allure.title("Apps-普通应用静默升级")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    # @pytest.mark.flaky(reruns=3, reruns_delay=1)
    def test_high_version_app_cover_low_version_app_MDM2(self, recover_and_login_mdm, del_app_install_uninstall_release_log, del_download_apk, uninstall_multi_apps,
                                                    go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        while True:
            try:
                log.info("*******************推送高版本APP覆盖安装用例开始***************************")
                self.android_mdm_page.confirm_app_installed(self.android_mdm_page.get_apk_path(test_yml['app_info']['low_version_app']))
                log.info("设备已经安装了低版本的app: %s" % test_yml['app_info']['low_version_app'])
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version
                # check if device is online
                # self.page.go_to_new_address("devices")
                opt_case.confirm_device_online(self.device_sn)
                # app_size_mdm = self.page.get_app_size()  for web
                # check app size(bytes) in windows
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % app_size)
                # go to app page
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info)

                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************终端检测到下载记录*************************************")

                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原文件的hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("shell_hash_value: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(60)
                log.info("**********************终端检测到下载完成*************************************")
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.app_page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.app_page.transfer_version_into_int(release_info["version"]):
                            break
                        else:
                            log.error("@@@@再一次安装后版本不一致， 请检查！！！！")
                            assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                self.app_page.time_sleep(5)
                log.info("**********************终端检测到成功安装app*************************************")

                self.app_page.go_to_new_address("apps/logs")
                self.app_page.refresh_page()
                now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示 upgrade action 为：%s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            log.info("平台显示覆盖安装升级完成")
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@5分钟平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            now_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(20)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)

                log.info("*********静默高版本覆盖低版本安装完成*********")

                log.info("*******低版本覆盖安装用例结束****************")
                break
            except Exception as e:
                if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.android_mdm_page.confirm_app_installed(
                        conf.project_path + "\\Param\\Package\\%s" % test_yml['app_info']['low_version_app'])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case6')
    @allure.title("public case- 系统应用静默升级/推送安装成功后自动运行app")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_upgrade_system_app_MDM2(self, recover_and_login_mdm, del_app_install_uninstall_release_log, del_download_apk, uninstall_system_app):
        while True:
            try:
                log.info("*******************静默升级系统app用例开始/推送安装成功后自动运行app***************************")

                release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                                "silent": "Yes", "download_network": "NO Limit", "auto_open": "YES"}
                # check if device is online
                # self.app_page.go_to_new_address("devices")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                opt_case.confirm_device_online(self.device_sn)
                log.info("检测到设备 %s 在线" % release_info["sn"])
                file_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                # # install low version system application
                # # set app as system app
                # self.android_mdm_page.wifi_adb_root(self.wifi_ip)
                self.android_mdm_page.open_root_auth_usb()
                # self.android_mdm_page.open_root_auth()
                assert not self.android_mdm_page.app_is_installed(
                    self.android_mdm_page.get_apk_package_name(file_path))
                # push file to system/app
                now_time = self.android_mdm_page.get_current_time()
                while True:
                    self.android_mdm_page.push_file_to_device(
                        self.android_mdm_page.get_apk_path(test_yml['app_info']['low_version_app']), "/system/app/")
                    if test_yml['app_info']['low_version_app'] in self.android_mdm_page.u2_send_command(
                            "ls /system/app"):
                        log.info(
                            "成功推送文件%s 到终端：%s, 标志为系统app" % (test_yml['app_info']['low_version_app'], "/system/app/"))
                        log.info(self.android_mdm_page.u2_send_command("ls /system/app"))
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 60):
                        log.error("无法推送文件%s 到终端：%s" % (test_yml['app_info']['low_version_app'], "/system/app/"))
                        assert False, "无法推送文件%s 到终端：%s" % (test_yml['app_info']['low_version_app'], "/system/app/")
                    self.android_mdm_page.time_sleep(2)
                log.info(self.android_mdm_page.u2_send_command("ls /system/app"))
                self.android_mdm_page.reboot_device_root(self.wifi_ip)
                log.info("重启")
                assert self.android_mdm_page.app_is_installed(
                    self.android_mdm_page.get_apk_package_name(file_path)), "@@@没有安装系统应用， 请检查！！！！"
                log.info("已经安装好了系统应用： %s" % self.android_mdm_page.get_apk_package_name(file_path))
                # release high version system app
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version

                # app_size_mdm = self.page.get_app_size()  for web
                # check app size(bytes) in windows
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))

                # go to app page
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@平台没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@平台没有 %s, 请检查！！！" % release_info["package_name"]
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.click_release_app_btn()
                try:
                    self.app_page.input_release_app_info(release_info)
                    log.info("app推送指令下达成功")
                except Exception as e:
                    pass
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        log.info("终端检测到 %s的 下载记录" % shell_app_apk_name)
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************检测到终端有下载记录*************************************")

                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原始app的 hash 值： %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("shell_hash_value: %s" % original_hash_value)
                    if original_hash_value == shell_hash_value:
                        log.info("检测到原始文件和终端下载后的文件内容一致性， 下载完成")
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        log.error("@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(60)
                log.info("***********************检测到终端下载完毕******************************")
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.app_page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        log.info("目标版本为：%s" % ".".join(str(version_installed)))
                        current_version = self.app_page.transfer_version_into_int(release_info["version"])
                        log.info("当前版本为： %s" % ".".join(str(current_version)))
                        if version_installed == current_version:
                            log.info("设备检测到系统app静默覆盖安装完成")
                            break
                        else:
                            log.error("@@@@覆盖安装后版本与木目标版本不一致， 请检查！！！！")
                            assert False, "@@@@覆盖安装后版本与木目标版本不一致， 请检查！！！！"
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(5)
                self.app_page.time_sleep(5)
                self.app_page.go_to_new_address("apps/logs")
                self.app_page.refresh_page()
                report_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的upgrade action为： %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            log.info("平台上报升级完成")
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 300):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@5分钟平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            report_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)
                log.info("**********************终端成功静默安装系统app*************************************")
                log.info("************************推送安装成功后自动运行app用例开始*****************************")
                try:
                    self.android_mdm_page.confirm_app_auto_running(release_info["package"], 120)
                except AttributeError:
                    log.error("app 推送选择了安装完成后自动运行app, app安装完后2分钟内还没自动运行")
                    assert False, "app 推送选择了安装完成后自动运行app, app安装完后2分钟内还没自动运行"
                try:
                    self.android_mdm_page.stop_app(release_info["package"])
                    self.android_mdm_page.rm_file("system/app/%s" % test_yml['app_info']['low_version_app'])
                except Exception as e:
                    pass
                log.info("************************推送安装成功后自动运行app成功*****************************")
                log.info("***************静默升级系统app/推送安装成功后自动运行app用例结束*********************")
                break
            except Exception as e:
                if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                    print(e)
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.confirm_system_app_uninstalled()
                    self.app_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case7')
    @allure.story('MDM-Show111')
    @allure.title("Apps-限定4G网络推送app")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=2)
    def test_release_app_limit_4G_MDM2(self, recover_and_login_mdm, connect_wifi_adb_USB, del_all_app_release_log,
                                  del_all_app_uninstall_release_log, uninstall_multi_apps, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "Sim Card"}
        # release_info = {"package_name": test_yml['app_info']['other_app_limit_network_A'], "sn": self.device_sn,
        #                 "silent": "Yes", "network": "Wifi/Ethernet"
        while True:
            try:
                log.info("*********限定4G网络推送app用例开始**************")
                # self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                # self.android_mdm_page.reboot_device(self.wifi_ip)
                self.android_mdm_page.confirm_wifi_status_open()
                log.info("成功连接wifi")
                # file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                file_path = self.app_page.get_apk_path(release_info["package_name"])
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version
                # check if device is online
                # self.page.go_to_new_address("devices")
                opt_case.confirm_device_online(self.device_sn)

                # check app size(bytes) in windows
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到 app的size: %s" % app_size)
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                # original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                #     "%s" % release_info["package_name"])
                # log.info("源文件的 hash 值： %s" % original_hash_value)
                log.info("原始文件的 hash value: %s" % original_hash_value)
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                # go to app page
                self.app_page.go_to_new_address("apps")

                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    err_msg = "没有相应的升级包 %s, 请检查！！！" % release_info["package_name"]
                    log.error(err_msg)
                    assert False, err_msg
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info)
                log.info("推送app： %s" % release_info["package_name"])

                # check if no upgrade log in wifi network environment
                # check the app action in app upgrade logs, if download complete or upgrade complete, break
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        err_msg = "@@@@在非4G网络可以下载app， 请检查！！！！"
                        log.error(err_msg)
                        assert False, err_msg
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 60):
                        break

                log.info("1分钟内在非4G网络1分钟没检测到有下载记录")

                # disconnect wifi
                self.android_mdm_page.disconnect_ip(self.wifi_ip)
                self.android_mdm_page.confirm_wifi_btn_close()
                log.info("成功断开wifi")
                self.app_page.time_sleep(3)
                log.info("打开流量数据")
                self.android_mdm_page.open_mobile_data()

                self.android_mdm_page.ping_network(timeout=300)

                log.info("成功过打开流量数据")
                # check if app download in 4G environment

                # check download record in device
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                print(shell_app_apk_name)
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**************设备中检测到下载记录*********************")
                now_time = self.app_page.get_current_time()
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device_USB(shell_app_apk_name)
                    log.info("终端检测到下载后的hash 值为： %s" % shell_hash_value)
                    # shell_size_value = self.android_mdm_page.cal
                    if original_hash_value == shell_hash_value:
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        log.error("@@@@30分钟内检测到原始文件和下载文件的不一致,应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(10)

                log.info("设备中检测到app下载完成")
                # connect wifi
                self.android_mdm_page.open_wifi_btn()
                log.info("打开wifi按钮")
                self.android_mdm_page.confirm_wifi_status_open()
                # self.android_mdm_page.connect_ip(self.wifi_ip)
                # self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                log.info("连接上wifi adb ")

                self.app_page.go_to_new_address("apps/logs")
                report_now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        self.app_page.time_sleep(5)
                        self.app_page.refresh_page()
                        upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台upgrade action为: %s" % action)
                            if self.app_page.get_action_status(action) == 4:
                                log.info("平台上报设备已经升级完毕")
                                break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 300):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                self.app_page.time_sleep(5)
                log.info("************************限定4G网络推送app用例运行成功***************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal("apps", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case8')
    @allure.title("Apps-限定WIFI网络推送app")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_release_app_limit_wifi_MDM2(self, recover_and_login_mdm, connect_wifi_adb_USB, del_all_app_release_log,
                                    del_all_app_uninstall_release_log,
                                    go_to_app_page):
        while True:
            try:
                log.info("*********************限定wifi/eth0网络推送app用例开始***************************")
                release_info = {"package_name": test_yml['app_info']['other_app_limit_network_B'], "sn": self.device_sn,
                                "silent": "Yes", "download_network": "Wifi/Ethernet"}
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                # self.page.go_to_new_address("devices")
                # opt_case.check_single_device(release_info["sn"])
                opt_case.confirm_device_online(release_info["sn"])
                log.info("准备断开wifi")
                # disconnect wifi, open data
                self.android_mdm_page.disconnect_ip(self.wifi_ip)
                self.android_mdm_page.close_wifi_btn()
                self.android_mdm_page.confirm_wifi_btn_close()
                log.info("成功断开wifi")
                self.app_page.time_sleep(3)
                log.info("准备打开流量数据")
                self.android_mdm_page.open_mobile_data()
                log.info("成功打开流量数据")

                file_path = self.app_page.get_apk_path(release_info["package_name"])
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
                release_info["version"] = version

                # check app size(bytes) in windows
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("电脑端获取到app的size : %s" % str(app_size))
                # go to app page
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])
                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    err_msg = "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                    log.error(err_msg)

                    assert False, err_msg
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info)

                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.download_file_is_existed_USB(shell_app_apk_name):
                        err_msg = "@@@@在非wifi/eth0网络可以下载app， 请检查！！！！"
                        log.error(err_msg)
                        assert False, err_msg
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 60):
                        log.info("在wifi/eth0网络1分钟没检测到有下载记录")
                        break
                log.info("准备连接wifi/eth0")
                # connect wifi
                self.android_mdm_page.close_mobile_data()
                self.android_mdm_page.open_wifi_btn()
                self.android_mdm_page.confirm_wifi_btn_open()
                # self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                log.info("成功连接到wifi")

                # check download record in device
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************终端检测到下载记录*************************************")

                # check if app download in 4G environment
                # check the app action in app upgrade logs, if download complete or upgrade complete, break
                log.info("准备检查平台app的下载记录以及终端的下载记录")

                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("源文件的 hash 值： %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("终端显示的MD5值为：%s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(20)
                log.info("终端下载完成")

                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 mins at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(5)
                self.app_page.time_sleep(5)
                log.info("**********************终端检测到app安装完成********************")

                self.app_page.go_to_new_address("apps/logs")
                report_now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade log action显示：%s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 300):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                    self.ota_page.refresh_page()

                log.info("*******************限制wifi网络下载安装完成***************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal("apps", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.app_page.recovery_after_service_unavailable("apps", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.app_page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('Special_Test-case9')
    @allure.title("stability case-文件文件推送成功率-请在报告右侧log文件查看文件文件推送成功率")
    def test_multi_release_content_MDM2(self, del_all_content_release_logs, del_all_content_file):
        # 设置断店续传重启得次数
        reboot_times = 5
        while True:
            try:
                log.info("**********文件文件推送成功率用例开始****************")
                opt_case.confirm_device_online(self.device_sn)
                content_page = self.content_page
                stability_files = test_yml["Content_info"]["stability_test_file"]

                release_to_path = "%s/aimdm" % self.android_mdm_page.get_internal_storage_directory()
                grep_cmd = "ls %s" % release_to_path
                release_flag = 0

                # start to release file one by one
                for file in stability_files:
                    self.content_page.go_to_new_address("content")
                    file_path = conf.project_path + "\\Param\\Content\\%s" % file
                    file_size = self.content_page.get_file_size_in_windows(file_path)
                    log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                    file_hash_value = self.android_mdm_page.calculate_sha256_in_windows(file, directory="Content")
                    log.info("获取到文件 的hash value: %s" % str(file_hash_value))
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                 case_pack.time.localtime(self.content_page.get_current_time()))
                    self.content_page.time_sleep(15)
                    self.content_page.search_content('Normal Files', file)
                    release_info = {"sn": self.device_sn, "content_name": file}
                    self.content_page.time_sleep(4)
                    assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有相关文件： %s, 请检查" % file
                    self.content_page.release_content_file(release_info["sn"], file_path=release_to_path)
                    log.info("释放文件: %s 到 %s" % (file, self.device_sn))
                    # check release log
                    # self.content_page.go_to_new_address("content/release")
                    # self.content_page.time_sleep(3)
                    # now_time = self.content_page.get_current_time()
                    # while True:
                    #     release_len = self.content_page.get_current_content_release_log_total()
                    #     if release_len == len(release_info["sn"]) + release_flag:
                    #         break
                    #     if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                    #         if content_page.service_unavailable_list():
                    #             log.error("@@@@没有相应的文件 release log， 请检查！！！")
                    #             assert False, "@@@@没有相应的文件 release log， 请检查！！！"
                    #         else:
                    #             self.content_page.recovery_after_service_unavailable("content/release", case_pack.user_info)
                    #             now_time = self.content_page.get_current_time()
                    #     self.content_page.time_sleep(5)
                    #     self.content_page.refresh_page()
                    #
                    # log.info("************释放log检测完毕*****************")

                    self.android_mdm_page.screen_keep_on()
                    # check the content download record in device
                    now_time = content_page.get_current_time()
                    while True:
                        if self.android_mdm_page.download_file_is_existed(file):
                            break
                        if content_page.get_current_time() > content_page.return_end_time(now_time, 1800):
                            assert False, "@@@@应用推送中超过30分钟还没有%s的下载记录" % file
                        content_page.time_sleep(3)

                    log.info("*********%s : %s下载记录检测完毕**********" % (self.device_sn, file))

                    before_reboot_file_size = self.android_mdm_page.get_file_size_in_device(file)
                    log.info("%s: 第一次下载的的file size: %s" % (self.device_sn, before_reboot_file_size))
                    for i in range(reboot_times):
                        self.android_mdm_page.reboot_device(self.wifi_ip)
                        log.info("%s 完成第 %d 重启" % (self.wifi_ip, (i + 1)))
                        self.android_mdm_page.ping_network()
                        log.info("确定注册上网络")
                        now_time = content_page.get_current_time()
                        while True:
                            current_size = self.android_mdm_page.get_file_size_in_device(file)
                            log.info("%s: 重启%s次之后当前file 的size: %s" % (self.device_sn, str(i + 1), current_size))
                            if current_size == file_size:
                                log.error("文件附件太小， 请重新上传大附件！！！！")
                                assert False, "@@@@文件太小，请上传大附件！！！！"
                            if current_size > before_reboot_file_size:
                                before_reboot_file_size = current_size
                                break
                            if content_page.get_current_time() > content_page.return_end_time(now_time, 300):
                                log.error("@@@@%s: 确认下载文件： %s， 5分钟内ota升级包没有大小没变， 没在下载" % (self.device_sn, file))
                                assert False, "@@@@确认下载提示后， 5分钟内ota升级包没有大小没变， 没在下载"
                            content_page.time_sleep(1)
                    log.info("*****%s : %s完成%d次重启断点续传******" % (self.device_sn, file, reboot_times))
                    # check if app download completed in the settings time
                    now_time_d = content_page.get_current_time()
                    expired_time = test_yml["Multi_devices_download_time_settings"]["stability_file_download_time"]
                    while True:
                        shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(file)
                        log.info("设备 %s 中下载的文件：%s 的hash value为： %s" % (self.device_sn, file, shell_hash_value))
                        if file_hash_value == shell_hash_value:
                            break
                        if content_page.get_current_time() > content_page.return_end_time(now_time_d, expired_time):
                            log.error("@@@@推送设备： %s中超过%d分钟还没有完成%s的下载" % (self.device_sn, expired_time, file))
                            assert False, "@@@@推送设备： %s中超过%d分钟还没有完成%s的下载" % (self.device_sn, expired_time, file)
                        content_page.time_sleep(20)
                    log.info("***********%s : %s下载完成检测完毕**************" % (self.device_sn, file))
                    setting_time = content_page.get_current_time()
                    while True:
                        if file in self.android_mdm_page.u2_send_command(grep_cmd):
                            break
                        if content_page.get_current_time() > content_page.return_end_time(setting_time):
                            assert False, "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path

                    log.info("*************设备%s：指定的路径已存在%s**************" % (self.device_sn, file))

                    self.content_page.go_to_new_address("content/log")
                    report_now_time = self.content_page.get_current_time()
                    while True:
                        upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                        if len(upgrade_list) != 0:
                            action = upgrade_list[0]["Action"]
                            log.info("平台检测到upgrade log 的action: %s" % action)
                            if self.content_page.get_action_status(action) == 7:
                                log.info("平台显示文件设置完毕")
                                break
                        # wait upgrade 3 min at most
                        if self.content_page.get_current_time() > self.content_page.return_end_time(report_now_time, 180):
                            print(upgrade_list)
                            if self.content_page.service_is_normal("content/log", case_pack.user_info):
                                log.error("@@@@3分钟平台还没有设置完相应的文件， 请检查！！！")
                                assert False, "@@@@3分钟平台还没有设置完相应的文件， 请检查！！！"
                            else:
                                self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                                report_now_time = self.content_page.get_current_time()
                        self.content_page.time_sleep(3)
                        self.content_page.refresh_page()
                    self.content_page.time_sleep(5)
                    assert file in self.android_mdm_page.u2_send_command(
                        grep_cmd), "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path
                    log.info("终端检测到文件已经推送到指定的路径： %s" % release_to_path)
                    log.info("推送文件：%s 结束" % file)
                log.info("**************多设备推送文件用例断点续传结束************************")
                break
            except Exception as e:
                if self.app_page.service_is_normal("content", case_pack.user_info):
                    assert False, e
                else:
                    self.app_page.recovery_after_service_unavailable("content", case_pack.user_info)

    @allure.feature('Special_Test-case10')
    @allure.title("public case-文件推送-网络恢复断点续传")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_release_normal_files_MDM2(self, recover_and_login_mdm, del_all_content_release_logs, del_all_content_file):
        # "All Files" "Normal Files" "Boot Animations" "Wallpaper" "LOGO"
        times = 1
        while True:
            try:
                log.info("***********文件推送-网络恢复断点续传******************")
                release_to_path = "%s/aimdm" % self.android_mdm_page.get_internal_storage_directory()
                grep_cmd = "ls %s" % release_to_path
                self.android_mdm_page.del_file_in_setting_path(release_to_path)
                self.android_mdm_page.reboot_device(self.wifi_ip)
                self.android_mdm_page.screen_keep_on()
                animation = test_yml["Content_info"]["stability_test_file"][0]

                # if the file is existed, delete it
                if animation in self.android_mdm_page.u2_send_command(grep_cmd):
                    self.android_mdm_page.rm_file("%s/%s" % (release_to_path, animation))
                opt_case.confirm_device_online(self.device_sn)
                self.content_page.go_to_new_address("content")
                file_path = conf.project_path + "\\Param\\Content\\%s" % animation
                file_size = self.content_page.get_file_size_in_windows(file_path)
                log.info("获取到的文件 的size(bytes): %s" % str(file_size))
                file_hash_value = self.android_mdm_page.calculate_sha256_in_windows("%s " % animation,
                                                                                    directory="Content")
                log.info("文件的hash_value: %s" % str(file_hash_value))
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.content_page.get_current_time()))
                self.content_page.time_sleep(4)
                self.content_page.search_content('Normal Files', animation)
                release_info = {"sn": self.device_sn, "content_name": animation}
                self.content_page.time_sleep(3)
                assert len(self.content_page.get_content_list()) == 1, "@@@@平台上没有相关文件： %s, 请检查" % animation
                self.content_page.release_content_file(self.device_sn, file_path=release_to_path)
                log.info("@@@@推送文件指令下达成功")
                now_time = self.content_page.get_current_time()
                while True:
                    if self.android_mdm_page.download_file_is_existed(animation):
                        log.info("终端检测到文件：%s的下载记录" % animation)
                        break
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time):
                        log.error("@@@@终端检测不到到文件：%s的下载记录" % animation)
                        assert False, "@@@@终端检测不到到文件：%s的下载记录" % animation
                    self.content_page.time_sleep(5)
                log.info("*************************************文件下载记录检测完毕**************************************")
                package_size = self.android_mdm_page.calculate_sha256_in_device(animation)
                # 断网恢复
                for i in range(times):
                    self.android_mdm_page.disconnect_ip(self.wifi_ip)
                    self.android_mdm_page.close_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_close()
                    self.android_mdm_page.no_network()
                    log.info("确认断开网络，终端无法上网")
                    self.ota_page.time_sleep(5)
                    log.info("等待...")
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.ping_network(timeout=300)
                    log.info("打开wifi开关并且确认可以上网")
                    opt_case.confirm_device_online(self.device_sn)
                    log.info("平台显示设备在线")
                    while True:
                        current_size = self.android_mdm_page.calculate_sha256_in_device(animation)
                        log.info("断网%s次之后当前文件 的size: %s" % (str(i + 1), current_size))
                        if current_size == file_hash_value:
                            err_info = "@@@@升级包下载完成, 请检查文件的大小是否适合！！！！"
                            log.error(err_info)
                            assert False, err_info
                        if current_size > package_size:
                            package_size = current_size
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                            err_msg = "@@@@确认下载提示后， 2分钟内文件大小没变， 没在下载， 请检查！！！"
                            print(err_msg)
                            log.error(err_msg)
                            assert False, err_msg
                        self.ota_page.time_sleep(3)

                log.info("*******************完成%d次断网操作*********************************" % (times + 1))

                now_time = self.content_page.get_current_time()
                while True:
                    shell_file_hash_value = self.android_mdm_page.calculate_sha256_in_device(animation)
                    log.info("终端检测到文件的hash 值为： %s" % shell_file_hash_value)
                    if file_hash_value == shell_file_hash_value:
                        log.info("终端检测到文件的hash值与原来的一致")
                        break
                    if self.content_page.get_current_time() > self.content_page.return_end_time(now_time, 1200):
                        log.error("超过20分钟终端检测到文件的hash值与原来的不一致")
                        assert False, "超过20分钟终端检测到文件的hash值与原来的不一致"
                    self.content_page.time_sleep(10)
                log.info("*************************************终端检测到文件下载完毕**************************************")
                self.content_page.go_to_new_address("content/log")
                report_now_time = self.content_page.get_current_time()
                while True:
                    upgrade_list = self.content_page.get_content_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台检测到upgrade log 的action: %s" % action)
                        if self.content_page.get_action_status(action) == 7:
                            log.info("平台显示文件设置完毕")
                            break
                    # wait upgrade 3 min at most
                    if self.content_page.get_current_time() > self.content_page.return_end_time(report_now_time,
                                                                                                180):
                        print(upgrade_list)
                        if self.content_page.service_is_normal("content/log", case_pack.user_info):
                            log.error("@@@@3分钟平台还没有设置完相应的文件， 请检查！！！")
                            assert False, "@@@@3分钟平台还没有设置完相应的文件， 请检查！！！"
                        else:
                            self.content_page.recovery_after_service_unavailable("content/log", case_pack.user_info)
                            report_now_time = self.content_page.get_current_time()
                    self.content_page.time_sleep(3)
                    self.content_page.refresh_page()
                self.content_page.time_sleep(5)
                assert animation in self.android_mdm_page.u2_send_command(
                    grep_cmd), "@@@@文件没有释放到设备指定的路径%s, 请检查！！！" % release_to_path
                log.info("终端检测到文件已经推送到指定的路径： %s" % release_to_path)
                log.info("*******************推送文件用例结束***************************")
                break
            except Exception as e:
                if self.content_page.service_is_normal("content", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.app_page.recovery_after_service_unavailable("content", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.content_page.delete_all_content_release_log()
                    self.android_mdm_page.del_all_content_file()
                    self.android_mdm_page.screen_keep_on()








