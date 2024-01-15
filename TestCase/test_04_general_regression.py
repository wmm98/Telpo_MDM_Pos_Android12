import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
test_yml = case_pack.yaml_data


class TestGeneralRegressionTesting:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.cat_log_page = case_pack.CatchLogPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.page.delete_app_install_and_uninstall_logs()
        self.ota_page.delete_all_ota_release_log()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.device_sn = self.android_mdm_page.get_device_sn()

    def teardown_class(self):
        # pass
        self.page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('GeneralRegressionTesting')
    @allure.title("OTA-OTA断网重连5次断点续传")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_OTA_package_general_regression_01(self, recover_and_login_mdm, fake_ota_package_operation,
                                                          connect_wifi_adb_USB, del_all_ota_release_log,
                                                          delete_ota_package_relate):
        while True:
            try:
                log.info("*******************OTA断网重连断点续传用例开始***************************")
                download_tips = "Foundanewfirmware,whethertoupgrade?"
                upgrade_tips = "whethertoupgradenow?"
                exp_success_text = "success"
                exp_existed_text = "ota release already existed"
                release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                                "category": "NO Limit", "network": "NO Limit"}
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                opt_case.confirm_device_online(release_info["sn"])
                times = 5
                self.page.go_to_new_address("ota")
                self.android_mdm_page.screen_keep_on()
                # close mobile data first
                log.info("先关闭流量数据")
                self.android_mdm_page.close_mobile_data()
                # get release ota package version
                release_info["version"] = self.page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                err_info = "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                assert self.page.transfer_version_into_int(
                    current_firmware_version) < self.page.transfer_version_into_int(
                    release_info["version"]), err_info

                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("固件升级的目标版本%s" % release_info["version"])
                # check file size and hash value in directory Param/package
                # ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                ota_package_path = conf.project_path + '\\Public_Package\\new\\%s' % release_info["package_name"]
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
                log.info("原ota升级包的大小: %s" % str(act_ota_package_size))
                # check file hash value in directory Param/package
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"], directory="Public_Package")
                log.info("ota升级包的md5值: %s" % str(act_ota_package_hash_value))
                # search package
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.page.get_current_time()))
                self.page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                # nolimit  simcard  wifiethernet
                self.ota_page.input_release_OTA_package(release_info)
                log.info("平台释放ota升级包指令下达成功")
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("终端弹出下载提示框并且点击确认下载")
                # flag = 0
                # for i in range(5):
                #     try:
                #         self.android_mdm_page.confirm_received_alert(download_tips)
                #         log.info("终端弹出下载提示框并且点击确认下载")
                #     except Exception as e:
                #         flag += 1
                #     if flag == 0:
                #         break
                #     if flag == 5:
                #         assert False, "@@@@无法接收到下载提示框， 请检查！！！！"

                # check download record in device
                # now_time = self.page.get_current_time()
                # while True:
                #     # check if app in download list
                #     if self.android_mdm_page.download_file_is_existed_USB(release_info["package_name"]):
                #         break
                #     if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                #         log.error("@@@@推送中超过5分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                #         assert False, "@@@@推送中超过5分钟还没有升级包: %s的下载记录" % release_info["package_name"]
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("存在： %s的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]

                log.info("****************终端检测到下载记录*******************")

                package_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
                log.info("断网前下载的的ota package size: %s" % str(package_size))
                for i in range(times):
                    self.android_mdm_page.disconnect_ip(self.wifi_ip)
                    self.android_mdm_page.close_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_close()
                    self.android_mdm_page.no_network()
                    log.info("确认断开网络，终端无法上网")
                    self.page.time_sleep(5)
                    log.info("等待...")
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.ping_network(timeout=300)
                    log.info("打开wifi开关并且确认可以上网")
                    # need to release again, skip below steps
                    # self.ota_page.go_to_new_address("ota/release")
                    # self.ota_page.select_release_log()
                    # self.ota_page.release_again()
                    # try:
                    #     self.android_mdm_page.confirm_received_alert(download_tips)
                    # except Exception:
                    #     assert False, "@@@@断网重连后一段时间内没有接受到下载的提示， 请检查！！！！"
                    # now_time = self.ota_page.get_current_time()
                    while True:
                        current_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
                        log.info("断网%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                        if current_size == act_ota_package_hash_value:
                            err_info = "@@@@升级包下载完成, 请检查ota 升级包大小是否适合！！！！"
                            log.error(err_info)
                            assert False, err_info
                        if current_size > package_size:
                            package_size = current_size
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                            err_msg = "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载， 请检查！！！"
                            print(err_msg)
                            log.error(err_msg)
                            assert False, err_msg
                        self.ota_page.time_sleep(3)

                log.info("*******************完成%d次断网操作*********************************" % (times + 1))
                # 防止滑动解锁点击取消按钮
                self.android_mdm_page.screen_keep_on()
                now_time = self.ota_page.get_current_time()
                while True:
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                        log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                        log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                        break

                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 1800):
                        err_msg = "@@@@断网重连%d次， 30分钟后还没有下载完相应的ota package， 请检查！！！" % times
                        log.error(err_msg)
                        assert False, err_msg
                    self.ota_page.time_sleep(10)
                log.info("*******************ota包下载完成**************************")
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台upgrade action: %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.page.get_action_status(action) == 4 \
                                or self.page.get_action_status(action) == 3:
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_now_time, 180):
                        if self.ota_page.service_is_normal("ota/log", case_pack.user_info):
                            err_msg = "@@@@终端下载完升级包后， 平台3分钟还没有下载完相应的ota package， 请检查！！！"
                            log.error(err_msg)
                            assert False, err_msg
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.ota_page.get_current_time()
                    self.ota_page.time_sleep(5)
                    self.ota_page.refresh_page()
                log.info("****************************ota升级升级包下载完成***************************")
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show(timeout=300)
                log.info("*****************检测到有升级提示框********************")
                try:
                    self.android_mdm_page.click_cancel_btn()
                except Exception as e:
                    pass
                log.info("*******************OTA断网重连断点续传用例结束***************************")
                break
            except Exception as e:
                if self.ota_page.service_is_normal("ota", case_pack.user_info):
                    assert False, e
                else:
                    self.android_mdm_page.confirm_wifi_status_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    log.info("**********************检测到服务器503***********************")
                    self.ota_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('GeneralRegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("OTA-OTA重启5次断点续传")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_OTA_package_general_regression_02(self, recover_and_login_mdm, fake_ota_package_operation,
                                               del_all_ota_release_log, delete_ota_package_relate):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        while True:
            try:
                log.info("*******************OTA重启5次断点续传用例开始***************************")
                # get release ota package version
                self.android_mdm_page.reboot_device(self.wifi_ip)
                times = 2
                opt_case.confirm_device_online(self.device_sn)
                self.ota_page.go_to_new_address("ota")
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                assert self.ota_page.transfer_version_into_int(
                    current_firmware_version) < self.ota_page.transfer_version_into_int(
                    release_info["version"]), \
                    "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                # reboot and sync data with platform
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # search package
                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("当前版本为： %s" % device_current_firmware_version)
                log.info("目的版本为: %s" % release_info["version"])
                # check file size and hash value in directory Param/package
                # ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                ota_package_path = conf.project_path + '\\Public_Package\\new\\%s' % release_info["package_name"]
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
                log.info("act_ota_package_size: %s" % act_ota_package_size)
                # check file hash value in directory Param/package
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"], directory="Public_Package")
                log.info("ota 包的md5值为: %s" % act_ota_package_hash_value)
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                self.ota_page.input_release_OTA_package(release_info)
                log.info("推送ota包： %s指令下达成功" % release_info["package_name"])
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("设备点击确认下载")
                # check download record in device
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("存在： %s的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]

                log.info("检测到下载记录")
                # check the app action in ota upgrade logs, if download complete or upgrade complete, break
                self.ota_page.go_to_new_address("ota/log")

                package_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                log.info("第一次下载的的ota package size: %s" % str(package_size))
                for i in range(times):
                    self.android_mdm_page.reboot_devices_no_back(self.wifi_ip)
                    log.info("***********第%d次重启************" % (i + 1))
                    self.android_mdm_page.ping_network(timeout=180)
                    try:
                        self.android_mdm_page.confirm_received_alert(download_tips)
                        log.info("设备显示下载提示并且确认下载")
                    except Exception:
                        log.error("@@@@开机恢复网络后一段时间内没有接受到下载的提示， 请检查！！！！")
                        assert "@@@@开机恢复网络后一段时间内没有接受到下载的提示， 请检查！！！！"
                    now_time = self.ota_page.get_current_time()
                    while True:
                        current_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                        log.info("重启%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                        if current_size == act_ota_package_size:
                            log.error("@@@@请检查ota 升级包大小是否适合！！！！")
                            assert False, "@@@@请检查ota 升级包大小是否适合！！！！"
                        if current_size > package_size:
                            package_size = current_size
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                            log.error("@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载")
                            assert False, "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载"
                        self.ota_page.time_sleep(1)
                log.info("*******************完成%d次重启*********************************" % (times + 1))
                # 防止滑动解锁点击取消按钮
                self.android_mdm_page.screen_keep_on()
                now_time = self.ota_page.get_current_time()
                while True:
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                        log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                        log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                        break

                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 1200):
                        err_msg = "@@@@重启%d次， 20分钟后还没有下载完相应的ota package， 请检查！！！" % (times + 1)
                        log.error(err_msg)
                        assert False, err_msg
                    self.ota_page.time_sleep(10)
                log.info("***************终端下载完ota升级包*************************")
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台显示的升级状态： %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.ota_page.get_action_status(action) == 4 \
                                or self.ota_page.get_action_status(action) == 3:
                            log.info("***************下载完ota升级包*************************")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_now_time, 120):
                        if self.ota_page.service_is_normal("ota/log", case_pack.user_info):
                            err_msg = "@@@@终端下载完升级包后， 平台3分钟还没有下载完相应的ota package， 请检查！！！"
                            log.error(err_msg)
                            assert False, err_msg
                        else:
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            report_now_time = self.ota_page.get_current_time()
                    self.ota_page.time_sleep(5)
                    self.ota_page.refresh_page()
                self.android_mdm_page.screen_keep_on_no_back()
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show(timeout=300)
                self.android_mdm_page.back_to_home()
                log.info("检测到有升级提示框")
                try:
                    self.android_mdm_page.click_cancel_btn()
                except Exception as e:
                    pass
                log.info("*******************OTA重启%d次断点续传用例结束***************************" % (times + 1))
                break
            except Exception as e:
                if self.ota_page.service_is_normal("ota", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.ota_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('GeneralRegressionTesting-test')
    @allure.story('MDM-Show')
    @allure.title("OTA-OTA升级")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_OTA_package_general_regression_03(self, recover_and_login_mdm, real_ota_package_operation,
                                               del_all_ota_release_log, delete_ota_package_relate):
        download_tips = "Foundanewfirmware,whethertoupgrade?"
        upgrade_tips = "whethertoupgradenow?"
        release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                        "silent": 0, "category": "NO Limit", "network": "NO Limit"}
        while True:
            try:
                log.info("*******************OTA重启5次断点续传用例开始***************************")
                # get release ota package version
                self.android_mdm_page.reboot_device(self.wifi_ip)
                times = 2
                opt_case.confirm_device_online(self.device_sn)
                self.ota_page.go_to_new_address("ota")
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                assert self.ota_page.transfer_version_into_int(
                    current_firmware_version) < self.ota_page.transfer_version_into_int(
                    release_info["version"]), \
                    "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                # reboot and sync data with platform
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # search package
                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("当前版本为： %s" % device_current_firmware_version)
                log.info("目的版本为: %s" % release_info["version"])
                # check file size and hash value in directory Param/package
                # ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                ota_package_path = conf.project_path + '\\Param\\Package\\%s' % release_info["package_name"]
                act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
                log.info("act_ota_package_size: %s" % act_ota_package_size)
                # check file hash value in directory Param/package
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"])
                log.info("ota 包的md5值为: %s" % act_ota_package_hash_value)
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                self.ota_page.input_release_OTA_package(release_info)
                log.info("推送ota包： %s指令下达成功" % release_info["package_name"])
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("设备点击确认下载")
                # check download record in device
                now_time = self.ota_page.get_current_time()
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(release_info["package_name"]):
                        log.info("存在： %s的下载记录" % release_info["package_name"])
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                        log.error("@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@推送中超过3分钟还没有升级包: %s的下载记录" % release_info["package_name"]

                log.info("**********检测到下载记录**************")

                # 防止滑动解锁点击取消按钮
                self.android_mdm_page.screen_keep_on()
                now_time = self.ota_page.get_current_time()
                while True:
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                        log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                        log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                        break

                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 1200):
                        err_msg = "@@@@20分钟后还没有下载完相应的ota package， 请检查！！！"
                        log.error(err_msg)
                        assert False, err_msg
                    self.ota_page.time_sleep(10)
                log.info("***************终端下载完ota升级包*************************")
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台显示的升级状态： %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.ota_page.get_action_status(action) == 4 \
                                or self.ota_page.get_action_status(action) == 3:
                            log.info("***************下载完ota升级包*************************")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(report_now_time, 120):
                        if self.ota_page.service_is_normal("ota/log", case_pack.user_info):
                            err_msg = "@@@@终端下载完升级包后， 平台3分钟还没有下载完相应的ota package， 请检查！！！"
                            log.error(err_msg)
                            assert False, err_msg
                        else:
                            self.ota_page.recovery_after_service_unavailable("ota/log", case_pack.user_info)
                            report_now_time = self.ota_page.get_current_time()
                    self.ota_page.time_sleep(5)
                    self.ota_page.refresh_page()
                log.info("*********平台显示下载完ota升级包*************")
                self.android_mdm_page.screen_keep_on_no_back()
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show(timeout=300)
                self.android_mdm_page.confirm_received_alert(upgrade_tips)
                self.android_mdm_page.back_to_home()
                log.info("确认升级")
                self.android_mdm_page.time_sleep(5)
                self.android_mdm_page.device_boot(self.wifi_ip)
                log.info("设备启动成功")
                after_upgrade_version = self.android_mdm_page.check_firmware_version()
                log.info("设备升级后的固件版本：%s" % after_upgrade_version)
                assert self.ota_page.remove_space(str(after_upgrade_version)) == self.ota_page.remove_space(
                    release_info["version"]), "@@@@升级后的固件版本为%s, ota升级失败， 请检查！！！" % after_upgrade_version
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
                log.info("**************平台显示ota安装升级完成完成******************")
                log.info("***********OTA重启%d次断点续传用例结束*****************")
                break
            except Exception as e:
                if self.ota_page.service_is_normal("ota", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.ota_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('GeneralRegressionTesting')
    @allure.title("Apps-推送低版本的APP/卸载后重新安装")
    @pytest.mark.dependency(name="test_release_app_ok", scope='package')
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_release_low_version_app(self, recover_and_login_mdm, del_all_app_release_log,
                                     del_all_app_uninstall_release_log, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['low_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}

        while True:
            try:
                log.info("*******************Apps-推送低版本的APP/卸载后重新安装用例开始*****************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                package = self.page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.page.get_apk_package_version(file_path)
                release_info["version"] = version
                # check if device is online
                # self.page.go_to_new_address("devices")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                opt_case.confirm_device_online(self.device_sn)

                # check if the app is existed, if existed, uninstall, else push
                # if self.android_mdm_page.app_is_installed(release_info["package"]):
                #     self.android_mdm_page.uninstall_app(release_info["package"])

                # app_size_mdm = self.page.get_app_size()  for web
                # check app size(bytes) in windows
                app_size = self.page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))
                # self.android_mdm_page.start_app()
                # go to app page
                self.page.go_to_new_address("apps")
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.page.get_current_time()))
                self.page.time_sleep(10)
                self.page.search_app_by_name(release_info["package_name"])
                app_list = self.page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                self.page.click_release_app_btn()
                self.page.input_release_app_info(release_info)
                log.info("平台成功推送app: %s" % release_info["package_name"])
                now_time = self.page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************终端中检测到下载记录**********************************")

                # check if download completed
                now_time = self.page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原包的 hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("终端中下载中app 的hash_value: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                        log.info("@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.page.time_sleep(10)
                log.info("**********************检测到终端下载完毕*************************************")

                # # check install

                # check upgrade
                now_time = self.page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.page.time_sleep(1)
                log.info("***********************检测到终端安装完毕*****************************")

                self.page.time_sleep(5)

                self.page.go_to_new_address("apps/logs")
                now_time = self.page.get_current_time()
                while True:
                    upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade action为： %s" % action)
                        if self.page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.page.time_sleep(20)
                    self.page.refresh_page()
                self.page.time_sleep(5)

                log.info("******************低版本静默安装用例结束*********************")
                log.info("****************卸载后重新安装成功用例开始***********************")
                send_time_final = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                          case_pack.time.localtime(self.page.get_current_time()))
                self.page.time_sleep(10)
                # uninstall app and check if app would be installed again in 10min
                self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
                # disconnect wifi
                self.android_mdm_page.disconnect_ip(self.wifi_ip)
                self.android_mdm_page.confirm_wifi_btn_close()
                self.page.time_sleep(3)
                self.android_mdm_page.open_mobile_data()
                self.android_mdm_page.confirm_wifi_btn_open()
                self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                # check upgrade
                now_time = self.page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有终端没显示安装完相应的app， 请检查！！！"
                    self.page.time_sleep(1)
                self.page.time_sleep(5)
                log.info("*******************设备中检测安装成功***************************")
                self.page.refresh_page()
                report_now_time = self.page.get_current_time()
                while True:
                    upgrade_list = self.page.get_app_latest_upgrade_log(send_time_final, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade action为： %s" % action)
                        if self.page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(report_now_time, 180):
                        if self.page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.page.get_current_time()
                    self.page.time_sleep(5)
                    self.page.refresh_page()
                log.info("****************卸载后重新安装成功用例结束***********************")
                log.info("*******************Apps-推送低版本的APP/卸载后重新安装用例开始*****************")
                break
            except Exception as e:
                if self.page.service_is_normal("apps/logs", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.page.go_to_new_address("apps")

    @allure.feature('GeneralRegressionTesting')
    @allure.title("Apps-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装")
    @pytest.mark.dependency(depends=["test_release_app_ok"], scope='package')
    # @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_high_version_app_cover_low_version_app(self, recover_and_login_mdm, del_all_app_release_log,
                                                    del_all_app_uninstall_release_log,
                                                    go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        while True:
            try:
                log.info("Apps-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装")
                log.info("*******************推送高版本APP覆盖安装用例开始***************************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                package = self.page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.page.get_apk_package_version(file_path)
                release_info["version"] = version
                # check if device is online
                # self.page.go_to_new_address("devices")
                opt_case.confirm_device_online(self.device_sn)
                # app_size_mdm = self.page.get_app_size()  for web
                # check app size(bytes) in windows
                app_size = self.page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % app_size)
                # go to app page
                self.page.go_to_new_address("apps")
                self.page.search_app_by_name(release_info["package_name"])
                app_list = self.page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.page.get_current_time()))
                self.page.time_sleep(10)
                self.page.click_release_app_btn()
                self.page.input_release_app_info(release_info)

                now_time = self.page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        log.error("@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************终端检测到下载记录*************************************")

                # check if download completed
                now_time = self.page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原文件的hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("shell_hash_value: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 1800):
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.page.time_sleep(60)
                log.info("**********************终端检测到下载完成*************************************")
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                            break
                        else:
                            log.error("@@@@再一次安装后版本不一致， 请检查！！！！")
                            assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.page.time_sleep(1)
                self.page.time_sleep(5)
                log.info("**********************终端检测到成功安装app*************************************")

                self.page.go_to_new_address("apps/logs")
                self.page.refresh_page()
                now_time = self.page.get_current_time()
                while True:
                    upgrade_list = self.page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示 upgrade action 为：%s" % action)
                        if self.page.get_action_status(action) == 4:
                            log.info("平台显示覆盖安装升级完成")
                            break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                        if self.page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@5分钟平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@5分钟平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            now_time = self.page.get_current_time()
                    self.page.time_sleep(20)
                    self.page.refresh_page()
                self.page.time_sleep(5)

                self.android_mdm_page.start_app(release_info["package"])
                log.info("app：%s 可以正常运行" % release_info["package"])
                self.android_mdm_page.stop_app(release_info["package"])
                log.info("app：%s 可以正常停止运行" % release_info["package"])

                log.info("*******************静默高版本覆盖低版本安装完成***************************")
                log.info("*******************卸载并重启后重新安装用例开始***************************")
                # uninstall app and reboot, check if app would be reinstalled again
                now_time = self.page.get_current_time()
                send_time_again = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                          case_pack.time.localtime(self.page.get_current_time()))
                self.page.time_sleep(10)
                self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
                log.info("终端确认已经卸载app")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.page.transfer_version_into_int(release_info["version"]):
                            log.info("再次安装后版本一致")
                            break
                        else:
                            log.error("@@@@再一次安装后版本不一致， 请检查！！！！")
                            assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 300):
                        log.info("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.page.time_sleep(1)
                self.page.time_sleep(5)
                log.info("**************卸载并重启后检测到终端再次安装了app*******************")

                self.page.refresh_page()
                report_now_time = self.page.get_current_time()
                while True:
                    upgrade_list = self.page.get_app_latest_upgrade_log(send_time_again, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的upgrade action为: %s" % action)
                        if self.page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.page.get_current_time() > self.page.return_end_time(report_now_time, 180):
                        if self.page.service_is_normal("apps/logs", case_pack.user_info):
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.page.get_current_time()
                    self.page.time_sleep(5)
                    self.page.refresh_page()
                self.page.time_sleep(5)
                log.info("*******************卸载并重启后重新安装用例结束*******************")
                log.info("*******************同版本覆盖安装用例开始***************************")

                # keep test environment clean
                log.info("开始删除install and uninstall log, 删除相关的下载文件")
                self.page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.del_all_downloaded_apk()
                log.info("成功删除install and uninstall log, 删除相关的下载文件")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                self.page.go_to_new_address("apps")
                self.page.search_app_by_name(release_info["package_name"])
                self.page.click_release_app_btn()
                self.page.input_release_app_info(release_info)
                log.info("推送同版本app指令下达")
                now_time = self.page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@有检测到同版本app: %s的下载记录, 请检查！！！！" % release_info["package_name"]
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        break
                    self.page.time_sleep(3)
                log.info("**************没有检测到同版本app的下载记录******************")
                log.info("*******************同版本覆盖安装用例结束**************************")
                log.info("*******************低版本静默覆盖安装开始***************************")
                # keep test environment clean
                log.info("开始删除install and uninstall log, 删除相关的下载文件")
                self.page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.del_all_downloaded_apk()
                log.info("成功删除install and uninstall log, 删除相关的下载文件")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                self.page.go_to_new_address("apps")
                self.page.search_app_by_name(test_yml['app_info']['low_version_app'])
                self.page.click_release_app_btn()
                self.page.input_release_app_info(release_info)

                now_time = self.page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % test_yml['app_info']['low_version_app']
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@有检测到同版本app: %s的下载记录, 请检查！！！！" % release_info["package_name"]
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                        break
                    self.page.time_sleep(3)

                log.info("***没有检测到低版本app的下载记录*****")
                log.info("***********低版本覆盖安装用例结束**********************")
                break
            except Exception as e:
                if self.page.service_is_normal("apps/logs", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.delete_app_install_and_uninstall_logs()
                    self.android_mdm_page.del_all_downloaded_apk()
                    self.android_mdm_page.uninstall_multi_apps(test_yml["app_info"])
                    self.android_mdm_page.confirm_app_installed(
                        conf.project_path + "\\Param\\Package\\%s" % test_yml['app_info']['low_version_app'])
                    self.page.go_to_new_address("apps")
