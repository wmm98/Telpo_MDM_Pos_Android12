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
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.ota_page = case_pack.OTAPage(self.driver, 40)
        self.device_page = case_pack.DevicesPage(self.driver, 40)
        self.system_page = case_pack.SystemPage(self.driver, 40)
        self.cat_log_page = case_pack.CatchLogPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.app_page.delete_app_install_and_uninstall_logs()
        self.ota_page.delete_all_ota_release_log()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.device_sn = self.android_mdm_page.get_device_sn()

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('GeneralRegressionTesting-chenr-test')
    @allure.title("OTA-OTA 下载拷贝校验完整性")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=20, reruns_delay=3)
    def test_OTA_package_general_regression_01(self, recover_and_login_mdm, real_ota_package_operation,
                                                          connect_wifi_adb_USB, del_all_ota_release_log,
                                                          delete_ota_package_relate):
        while True:
            try:
                log.info("*******************OTAOTA-OTA 下载拷贝校验完整性开始***************************")
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
                self.ota_page.go_to_new_address("ota")
                self.android_mdm_page.screen_keep_on()
                # get release ota package version
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                err_info = "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                assert self.ota_page.transfer_version_into_int(
                    current_firmware_version) < self.ota_page.transfer_version_into_int(
                    release_info["version"]), err_info

                device_current_firmware_version = self.android_mdm_page.check_firmware_version()
                log.info("固件升级的目标版本%s" % release_info["version"])
                # check file size and hash value in directory Param/package
                ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                # ota_package_path = conf.project_path + '\\Public_Package\\new\\%s' % release_info["package_name"]

                act_ota_package_size = self.ota_page.get_zip_size(ota_package_path)
                log.info("原ota升级包的大小: %s" % str(act_ota_package_size))
                # check file hash value in directory Param/package
                act_ota_package_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    release_info["package_name"])
                log.info("ota升级包的md5值: %s" % str(act_ota_package_hash_value))
                # search package
                self.ota_page.search_device_by_pack_name(release_info["package_name"])
                # ele = self.Page.get_package_ele(release_info["package_name"])
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                # nolimit  simcard  wifiethernet
                self.ota_page.input_release_OTA_package(release_info)
                log.info("平台释放ota升级包指令下达成功")
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("终端弹出下载提示框并且点击确认下载")

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

                # package_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
                # log.info("断网前下载的的ota package size: %s" % str(package_size))
                # # for i in range(times):
                #     self.android_mdm_page.disconnect_ip(self.wifi_ip)
                #     self.android_mdm_page.close_wifi_btn()
                #     self.android_mdm_page.confirm_wifi_btn_close()
                #     self.android_mdm_page.no_network()
                #     log.info("确认断开网络，终端无法上网")
                #     self.ota_page.time_sleep(5)
                #     log.info("等待...")
                #     self.android_mdm_page.open_wifi_btn()
                #     self.android_mdm_page.confirm_wifi_btn_open()
                #     self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                #     self.android_mdm_page.ping_network(timeout=300)
                #     log.info("打开wifi开关并且确认可以上网")

                    # while True:
                    #     current_size = self.android_mdm_page.get_file_size_in_device_USB(release_info["package_name"])
                    #     log.info("断网%s次之后当前ota package 的size: %s" % (str(i + 1), current_size))
                    #     if current_size == act_ota_package_hash_value:
                    #         err_info = "@@@@升级包下载完成, 请检查ota 升级包大小是否适合！！！！"
                    #         log.error(err_info)
                    #         assert False, err_info
                    #     if current_size > package_size:
                    #         package_size = current_size
                    #         break
                    #     if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 120):
                    #         err_msg = "@@@@确认下载提示后， 2分钟内ota升级包没有大小没变， 没在下载， 请检查！！！"
                    #         print(err_msg)
                    #         log.error(err_msg)
                    #         assert False, err_msg
                    #     self.ota_page.time_sleep(3)

                # log.info("*******************完成%d次断网操作*********************************" % (times + 1))
                # 防止滑动解锁点击取消按钮
                # self.android_mdm_page.screen_keep_on()
                now_time = self.ota_page.get_current_time()
                while True:
                    download_file_size = self.android_mdm_page.get_file_size_in_device(release_info["package_name"])
                    package_hash_value = self.android_mdm_page.calculate_sha256_in_device(release_info["package_name"])
                    if download_file_size == act_ota_package_size and package_hash_value == act_ota_package_hash_value:
                        log.info("原来升级包的 package_hash_value：%s" % str(package_hash_value))
                        log.info("下载完成后的 package_hash_value：%s" % str(package_hash_value))
                        break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        err_msg = "@@@@30分钟后还没有下载完相应的ota package， 请检查！！！"
                        log.error(err_msg)
                        # assert False, err_msg
                        raise Exception(err_msg)
                    self.ota_page.time_sleep(10)
                log.info("*******************ota包下载完成**************************")
                # 对比 update包
                now_time = self.ota_page.get_current_time()
                while True:
                    if "update.zip" in self.android_mdm_page.u2_send_command("ls %s/" % self.android_mdm_page.get_internal_storage_directory()):
                        updated_hash_value = self.android_mdm_page.calculate_updated_sha256_in_device()
                        log.info("update.zip 包的md5值为： %s" % updated_hash_value)
                        if updated_hash_value == act_ota_package_hash_value:
                            log.info("拷贝的update 包完整性一致")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        err_msg = "@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包， 请检查！！！"
                        log.error(err_msg)
                        # assert False, err_msg
                        raise Exception(err_msg)
                    self.ota_page.time_sleep(3)

                log.info("*******************根目录ota包拷贝完成完成**************************")

                # 检测copy update包是否完整
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台upgrade action: %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.ota_page.get_action_status(action) == 4 \
                                or self.ota_page.get_action_status(action) == 3:
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
                self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show(timeout=300)
                log.info("*****************检测到有升级提示框********************")
                try:
                    self.android_mdm_page.click_cancel_btn()
                except Exception as e:
                    pass
                log.info("*******************OTA-OTA 下载拷贝校验完整性用例结束***************************")
                assert False, "000000000000000000000000000"
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
    @allure.title("一般性回归测试-OTA重启断点续传")
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

    @allure.feature('GeneralRegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("一般性回归测试-OTA升级")
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
    @allure.title("一般性回归测试-推送低版本的APP/卸载后重新安装")
    @pytest.mark.dependency(name="test_release_app_ok", scope='package')
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_release_low_version_app_general_regression(self, recover_and_login_mdm, del_all_app_release_log,
                                     del_all_app_uninstall_release_log, go_to_app_page, uninstall_multi_apps):
        release_info = {"package_name": test_yml['app_info']['low_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}

        while True:
            try:
                log.info("*******************Apps-推送低版本的APP/卸载后重新安装用例开始*****************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                version = self.app_page.get_apk_package_version(file_path)
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
                app_size = self.app_page.get_file_size_in_windows(file_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))
                # self.android_mdm_page.start_app()
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
                self.app_page.input_release_app_info(release_info)
                log.info("平台成功推送app: %s" % release_info["package_name"])
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % release_info["package_name"]
                log.info("**********************终端中检测到下载记录**********************************")

                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"])
                log.info("原包的 hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("终端中下载中app 的hash_value: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                        log.info("@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                        assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                    self.app_page.time_sleep(10)
                log.info("**********************检测到终端下载完毕*************************************")

                # # check install

                # check upgrade
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                log.info("***********************检测到终端安装完毕*****************************")

                self.app_page.time_sleep(5)

                self.app_page.go_to_new_address("apps/logs")
                now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade action为： %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        log.error("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(20)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)

                log.info("******************低版本静默安装用例结束*********************")
                log.info("****************卸载后重新安装成功用例开始***********************")
                send_time_final = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                          case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                # uninstall app and check if app would be installed again in 10min
                self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
                # disconnect wifi
                self.android_mdm_page.disconnect_ip(self.wifi_ip)
                self.android_mdm_page.confirm_wifi_btn_close()
                self.app_page.time_sleep(3)
                self.android_mdm_page.open_mobile_data()
                self.android_mdm_page.confirm_wifi_btn_open()
                self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                # check upgrade
                now_time = self.app_page.get_current_time()
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        assert False, "@@@@3分钟还没有终端没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                self.app_page.time_sleep(5)
                log.info("*******************设备中检测安装成功***************************")
                self.app_page.refresh_page()
                report_now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time_final, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台upgrade action为： %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 180):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            log.error("@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                log.info("****************卸载后重新安装成功用例结束***********************")
                log.info("*******************Apps-推送低版本的APP/卸载后重新安装用例开始*****************")
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
                    self.app_page.go_to_new_address("apps")

    @allure.feature('GeneralRegressionTesting')
    @allure.title("一般性回归测试-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装")
    # @pytest.mark.dependency(depends=["test_release_app_ok"], scope='package')
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_high_version_app_cover_low_version_app_general_regression(self, recover_and_login_mdm, del_all_app_release_log,
                                                    del_all_app_uninstall_release_log,
                                                    go_to_app_page, uninstall_multi_apps):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes", "download_network": "NO Limit"}
        while True:
            try:
                log.info("Apps-推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装")
                log.info("*******************推送高版本APP覆盖安装用例开始***************************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]

                self.android_mdm_page.confirm_app_installed(self.android_mdm_page.get_apk_path(test_yml['app_info']['low_version_app']))

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

                self.android_mdm_page.start_app(release_info["package"])
                log.info("app：%s 可以正常运行" % release_info["package"])
                self.android_mdm_page.stop_app(release_info["package"])
                log.info("app：%s 可以正常停止运行" % release_info["package"])

                log.info("*******************静默高版本覆盖低版本安装完成***************************")
                log.info("*******************卸载并重启后重新安装用例开始***************************")
                # uninstall app and reboot, check if app would be reinstalled again
                now_time = self.app_page.get_current_time()
                send_time_again = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                          case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.android_mdm_page.confirm_app_is_uninstalled(release_info["package"])
                log.info("终端确认已经卸载app")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                while True:
                    if self.android_mdm_page.app_is_installed(release_info["package"]):
                        version_installed = self.app_page.transfer_version_into_int(
                            self.android_mdm_page.get_app_info(release_info["package"])['versionName'])
                        if version_installed == self.app_page.transfer_version_into_int(release_info["version"]):
                            log.info("再次安装后版本一致")
                            break
                        else:
                            log.error("@@@@再一次安装后版本不一致， 请检查！！！！")
                            assert False, "@@@@再一次安装后版本不一致， 请检查！！！！"
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 300):
                        log.info("@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！")
                        assert False, "@@@@5分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                    self.app_page.time_sleep(1)
                self.app_page.time_sleep(5)
                log.info("**************卸载并重启后检测到终端再次安装了app*******************")

                self.app_page.refresh_page()
                report_now_time = self.app_page.get_current_time()
                while True:
                    upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time_again, release_info)
                    if len(upgrade_list) != 0:
                        action = upgrade_list[0]["Action"]
                        log.info("平台显示的upgrade action为: %s" % action)
                        if self.app_page.get_action_status(action) == 4:
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_now_time, 180):
                        if self.app_page.service_is_normal("apps/logs", case_pack.user_info):
                            assert False, "@@@@3分钟还没有终端或者平台还没显示安装完相应的app， 请检查！！！"
                        else:
                            log.info("**********************检测到服务器503***********************")
                            self.app_page.recovery_after_service_unavailable("apps/logs", case_pack.user_info)
                            log.info("**********************服务器恢复正常*************************")
                            report_now_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(5)
                    self.app_page.refresh_page()
                self.app_page.time_sleep(5)
                log.info("*******************卸载并重启后重新安装用例结束*******************")
                log.info("*******************同版本覆盖安装用例开始***************************")

                # keep test environment clean
                log.info("开始删除install and uninstall log, 删除相关的下载文件")
                self.app_page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.del_all_downloaded_apk()
                log.info("成功删除install and uninstall log, 删除相关的下载文件")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info)
                log.info("推送同版本app指令下达")
                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % release_info["version"]
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@有检测到同版本app: %s的下载记录, 请检查！！！！" % release_info["package_name"]
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        break
                    self.app_page.time_sleep(3)
                log.info("**************没有检测到同版本app的下载记录******************")
                log.info("*******************同版本覆盖安装用例结束**************************")
                log.info("*******************低版本静默覆盖安装开始***************************")
                # keep test environment clean
                log.info("开始删除install and uninstall log, 删除相关的下载文件")
                self.app_page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.del_all_downloaded_apk()
                log.info("成功删除install and uninstall log, 删除相关的下载文件")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("重启终端")
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(test_yml['app_info']['low_version_app'])
                self.app_page.click_release_app_btn()
                self.app_page.input_release_app_info(release_info)

                now_time = self.app_page.get_current_time()
                shell_app_apk_name = release_info["package"] + "_%s.apk" % test_yml['app_info']['low_version_app']
                while True:
                    # check if app in download list
                    if self.android_mdm_page.download_file_is_existed(shell_app_apk_name):
                        assert False, "@@@@有检测到同版本app: %s的下载记录, 请检查！！！！" % release_info["package_name"]
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 180):
                        break
                    self.app_page.time_sleep(3)

                log.info("***没有检测到低版本app的下载记录*****")
                log.info("***********低版本覆盖安装用例结束**********************")
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

    @allure.feature('GeneralRegressionTesting')
    @allure.title("一般性回归测试 - 静默升级系统app/推送安装成功后自动运行app")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_upgrade_system_app_general_regression(self, recover_and_login_mdm, del_app_install_uninstall_release_log, del_download_apk,
                                uninstall_system_app):
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

    @allure.feature('GeneralRegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("一般性回归测试-静默卸载正在运行中的app：静默卸载/卸载正在运行的app")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_silent_uninstall_app_general_regression(self, recover_and_login_mdm, del_all_app_release_log,
                                  del_all_app_uninstall_release_log,
                                  uninstall_multi_apps, go_to_app_page):
        release_info = {"package_name": test_yml['app_info']['high_version_app'], "sn": self.device_sn,
                        "silent": "Yes"}
        while True:
            try:
                log.info("*******************静默卸载正在运行中的app 用例开始***************************")
                file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                self.android_mdm_page.reboot_device(self.wifi_ip)
                package = self.app_page.get_apk_package_name(file_path)
                release_info["package"] = package
                # install app for uninstall
                self.android_mdm_page.confirm_app_installed(file_path)
                # check if device is online
                # self.app_page.go_to_new_address("devices")
                opt_case.confirm_device_online(self.device_sn)
                log.info("检测到设备在线")
                # go to app release page
                self.app_page.go_to_new_address("apps")
                self.app_page.search_app_by_name(release_info["package_name"])

                app_list = self.app_page.get_apps_text_list()
                if len(app_list) == 0:
                    log.error("@@@@检测到平台没有 %s, 请检查！！！" % release_info["package_name"])
                    assert False, "@@@@检测到平台没有 %s, 请检查！！！" % release_info["package_name"]

                # start app and then uninstall it， added recently
                # self.android_mdm_page.start_app(release_info["package"])
                self.android_mdm_page.confirm_app_is_running(release_info["package"])
                self.android_mdm_page.screen_keep_on()
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                # self.android_mdm_page
                self.app_page.click_uninstall_app_btn()
                self.app_page.input_uninstall_app_info(release_info)
                log.info("筋膜卸载指令下达成功")

                self.app_page.go_to_new_address("apps/uninstalllogs")
                report_time = self.app_page.get_current_time()
                while True:
                    upgrade_log = self.app_page.get_app_latest_uninstall_log(send_time, release_info)
                    if len(upgrade_log) != 0:
                        action = upgrade_log[0]["Action"]
                        log.info("平台状态显示upgrade action: %s" % action)
                        if self.app_page.get_action_status(action) == 0:
                            log.info("平台显示完成app的静默卸载")
                            assert not self.android_mdm_page.app_is_installed(
                                release_info["package"]), "@@@@平台显示已经卸载app：%s, 检测到设备还没卸载， 请检查！！！" % release_info[
                                "package_name"]
                            log.info("检测到设备已经卸载了app： %s" % release_info["package_name"])
                            break
                    # wait upgrade 3 min at most
                    if self.app_page.get_current_time() > self.app_page.return_end_time(report_time, 180):
                        if self.app_page.service_is_normal("apps/uninstalllogs", case_pack.user_info):
                            log.error("@@@@3分钟还没有卸载完相应的app， 请检查！！！")
                            assert False, "@@@@3分钟还没有卸载完相应的app， 请检查！！！"
                        else:
                            self.app_page.recovery_after_service_unavailable("apps/uninstalllogs", case_pack.user_info)
                            report_time = self.app_page.get_current_time()
                    self.app_page.time_sleep(3)
                    self.app_page.refresh_page()
                log.info("****************************************静默卸载完成**********************************")
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
                    self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
                    self.app_page.go_to_new_address("apps")

    @allure.feature('GeneralRegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("一般性回归测试- AIMDM切换正式测试服服务api ")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_transfer_api_server_general_regression(self, recover_and_login_mdm, push_test_api_to_device):
        while True:
            try:
                log.info("*************AIMDM 切换正式测试服服务api 测试用例开始*************")
                log.info("服务器A为当前的主测试服务, 服务器B为需要切换的服务， 平台A和平台B也如此")
                exp_success_msg = "Updated Device Setting"
                test_version_api = test_yml['website_info']['test_api']
                log.info("服务器A 的api 接口： %s" % test_version_api)
                release_version_api = test_yml['website_info']['release_api']
                log.info("服务器B的api 接口： %s" % release_version_api)
                release_version_url = test_yml['website_info']['release_url']
                release_user_info = {"username": test_yml['website_info']['release_user'],
                                     "password": test_yml['website_info']['release_password']}
                sn = self.device_sn
                release_main_title = "Total Devices"
                release_login_ok_title = "Telpo MDM"
                opt_case.confirm_device_online(sn)
                root_dir = self.android_mdm_page.get_internal_storage_directory()
                self.device_page.refresh_page()
                self.device_page.page_load_complete()
                log.info("准备登录平台B： %s" % release_version_url)
                case_pack.BaseWebDriver().open_web_site(release_version_url)
                release_driver = case_pack.BaseWebDriver().get_web_driver()
                release_page = case_pack.ReleaseDevicePage(release_driver, 40)
                release_page.login_release_version(release_user_info)
                log.info("成功登录平台B： %s" % release_version_url)

                log.info("在平台B添加设备： %s" % sn)
                release_page.go_to_new_address("devices", release=True)
                release_page.search_device_by_sn(sn)
                devices_info = release_page.get_dev_info_list()
                # devices_sn = [device["SN"] for device in release_page.get_dev_info_list()]
                device_sn = self.android_mdm_page.get_device_sn()
                devices_list = {"SN": device_sn, "name": "aut" + device_sn}
                # if device_sn not in devices_sn:
                if len(devices_info) == 0:
                    # check if device model is existed, if not, add model
                    if "automation_debug" not in release_page.get_models_list():
                        release_page.click_model()
                        release_page.add_model("automation_debug")
                        release_page.refresh_page()
                    # check if device category is existed, if not, add category
                    if not release_page.category_is_existed("test_debug"):
                        release_page.click_category()
                        release_page.add_category("test_debug")
                    release_page.click_new_btn()
                    release_page.add_devices_info(devices_list, cate_model=False)
                    release_page.refresh_page()
                    # self.android_mdm_page.reboot_device(self.wifi_ip)
                    # release_page.refresh_page()

                opt_case.confirm_device_online(sn)
                log.info("当前平台A 显示设备%s在线在线" % sn)
                self.device_page.select_device(sn)
                # log.info("当前设备的api地址为： %s" % self.android_mdm_page.u2_send_command(
                #             "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])))
                log.info("当前设备的api地址为： %s" % self.android_mdm_page.get_mdmApiUrl_text())
                self.device_page.click_server_btn()
                self.device_page.api_transfer(release_version_api)
                log.info("设备切换服务器B： %s指令下达" % release_version_api)
                self.device_page.time_sleep(5)
                flag_f = 0
                now_time = self.device_page.get_current_time()
                while True:
                    if release_version_api in self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                        log.info("终端根目录下的aip 已经改变为服务器A的 api: %s" % release_version_api)
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(now_time):
                        flag_f += 1
                        break
                    self.device_page.time_sleep(10)

                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("成功重启设备")
                if flag_f != 0:
                    # check if the api had changed in device
                    log.info("检测到终端api变化情况")
                    now_time = self.device_page.get_current_time()
                    while True:
                        api_text = self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"]))
                        log.info("根目录下的api: %s" % api_text)
                        if release_version_api in api_text:
                            log.info("终端根目录下的api 已经变为服务器B的api：%s" % release_version_api)
                            break
                        if self.device_page.get_current_time() > self.device_page.return_end_time(now_time):
                            log.error("3分钟内终端还没改为服务器B的api： %s" % release_version_api)
                            assert False, "3分钟内终端还没改为服务器B的api： %s" % release_version_api
                        self.device_page.time_sleep(20)
                log.info("终端检测已经切换为服务器B的api: %s" % release_version_api)
                # check if device is offline in test version
                # self.page.refresh_page()
                # test_device_info = opt_case.get_single_device_list(sn)
                log.info("检测平台A中设备: %s的在线情况" % sn)
                online_time = self.device_page.get_current_time()
                reboot_flag = 0
                while True:
                    self.device_page.refresh_page()
                    if "OFF" in self.device_page.remove_space(
                            self.device_page.upper_transfer(opt_case.get_single_device_list(sn)[0]["Status"])):
                        log.info("测试平台A已经显示设备下线")
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(online_time, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time = self.device_page.get_current_time()
                        else:
                            log.error("@@@@3分钟内当前平台A显示设备还在线， 请检查！！！")
                            assert False, "@@@@3分钟内当前平台A显示设备还在线， 请检查！！！"
                    self.device_page.time_sleep(2)

                log.info("检测平台B中设备: %s的在线情况" % sn)
                # go to release version and check if device is online
                release_page.refresh_page()
                # release_page.go_to_device_page(release_main_title)

                release_data_list = release_page.get_single_device_list_release(sn)
                print(release_data_list)
                # assert "ON" in self.page.remove_space(self.page.upper_transfer(test_device_info[0]["Status"]))
                # if release_data_list[0]["Status"] == "Off":
                #     assert False
                reboot_flag = 0
                online_time1 = self.device_page.get_current_time()
                while True:
                    self.device_page.refresh_page()
                    if "ON" in self.device_page.remove_space(
                            self.device_page.upper_transfer(release_page.get_single_device_list_release(sn)[0]["Status"])):
                        log.info("测试平台B已经显示设备在线")
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(online_time1, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time1 = self.device_page.get_current_time()
                        else:
                            log.error("@@@@3分钟内当前平台B一直显示设备下线， 请检查！！！")
                            assert False, "@@@@3分钟内当前平台B一直显示设备下线， 请检查！！！"

                    self.device_page.time_sleep(2)
                log.info("设备再次切换回 服务器A 的api: %s, 切换回原来的服务器" % test_version_api)
                release_page.select_device(sn)
                # log.info("当前设备的api地址为： %s" % self.android_mdm_page.u2_send_command(
                #     "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])))
                log.info("当前设备的api地址为： %s" % self.android_mdm_page.get_mdmApiUrl_text())
                release_page.click_server_btn()
                release_page.api_transfer(test_version_api)
                log.info("切换服务器 api : %s指令下达成功" % test_version_api)
                flag = 0
                now_time = self.device_page.get_current_time()
                log.info("重启前检测终端api变化")
                while True:
                    if test_version_api in self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                        log.info("终端根目录下的aip 已经改变为服务器A的 api: %s" % test_version_api)
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(now_time, 120):
                        flag += 1
                        break
                    self.device_page.time_sleep(10)

                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("设备重启成功")

                if flag != 0:
                    log.info("重启后检测终端api变化")
                    reboot_flag = 0
                    online_time2 = self.device_page.get_current_time()
                    while True:
                        if test_version_api in self.android_mdm_page.u2_send_command(
                                "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                            log.info("终端根目录下的aip 已经改变为服务器A的api： %s" % test_version_api)
                            break
                        if self.device_page.get_current_time() > self.device_page.return_end_time(online_time2):
                            if reboot_flag == 0:
                                reboot_flag += 1
                                self.android_mdm_page.reboot_device(self.wifi_ip)
                                online_time2 = self.device_page.get_current_time()
                            else:
                                log.error("设备启动后3分钟内终端api还没改变为服务器A的api： %s, 请检查！！！" % test_version_api)
                                assert False, "设备启动后3分钟内终端api还没改变为服务器A的api： %s, 请检查！！！" % test_version_api
                        self.device_page.time_sleep(10)

                # check if device is offline in release version
                release_page.refresh_page()
                release_data_info_again = release_page.get_single_device_list_release(sn)
                print(release_data_info_again)

                log.info("检测平台B中设备: %s的在线情况" % sn)
                reboot_flag = 0
                online_time3 = self.device_page.get_current_time()
                while True:
                    self.device_page.refresh_page()
                    if "OFF" in self.device_page.remove_space(
                            self.device_page.upper_transfer(release_page.get_single_device_list_release(sn)[0]["Status"])):
                        log.info("检测到平台B中设备：%s显示下线状态" % sn)
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(online_time3, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time3 = self.device_page.get_current_time()
                        else:
                            log.error("@@@@3分钟内检测到平台B中设备一直显示在线， 请检查！！！")
                            assert False, "@@@@3分钟内检测到平台B中涉笔一直显示在线， 请检查！！！"
                    self.device_page.time_sleep(5)

                log.info("检测平台A中设备: %s的在线情况" % sn)
                # go to test version and check if device is online
                self.device_page.refresh_page()
                test_data_info = opt_case.get_single_device_list(sn)
                print(test_data_info)
                reboot_flag = 0
                online_time4 = self.device_page.get_current_time()
                while True:
                    self.device_page.refresh_page()
                    if "ON" in self.device_page.remove_space(
                            self.device_page.upper_transfer(opt_case.get_single_device_list(sn)[0]["Status"])):
                        log.info("平台A中设备：%s 显示在线状态" % sn)
                        break
                    if self.device_page.get_current_time() > self.device_page.return_end_time(online_time4, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time4 = self.device_page.get_current_time()
                        else:
                            log.error("@@@@3分钟内检测到平台A中设备一直显示下线， 请检查！！！")
                            assert False, "@@@@3分钟内检测到平台A中设备一直显示下线， 请检查！！！"
                    self.device_page.time_sleep(2)
                release_page.quit_browser()
                log.info("*****************AIMDM 切换正式测试服服务api 测试用例结束****************")
                break
            except Exception as e:
                if self.device_page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.device_page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["api_txt"]
                    if test_yml["website_info"]["test_api"] not in self.android_mdm_page.get_mdmApiUrl_text():
                        self.android_mdm_page.push_file_to_device(api_path,
                                                                  "/" + self.android_mdm_page.get_internal_storage_directory() + "/")
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.device_page.go_to_new_address("devices")

    @allure.feature('GeneralRegressionTesting')
    @allure.title("Devices- 日志的抓取")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_cat_logs_general_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('GeneralRegressionTesting')
    @allure.title("OTA-断网断点续传")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_OTA_package_general_regression_04(self, recover_and_login_mdm, fake_ota_package_operation,
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
                self.ota_page.go_to_new_address("ota")
                self.android_mdm_page.screen_keep_on()
                # close mobile data first
                log.info("先关闭流量数据")
                self.android_mdm_page.close_mobile_data()
                # get release ota package version
                release_info["version"] = self.ota_page.get_ota_package_version(release_info["package_name"])
                current_firmware_version = self.android_mdm_page.check_firmware_version()
                # compare current version and exp version
                err_info = "@@@@释放的ota升级包比当前固件版本版本低， 请检查！！！"
                assert self.ota_page.transfer_version_into_int(
                    current_firmware_version) < self.ota_page.transfer_version_into_int(
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
                                                    case_pack.time.localtime(self.ota_page.get_current_time()))
                self.ota_page.time_sleep(10)
                # if device is existed, click
                self.ota_page.click_release_btn()
                # nolimit  simcard  wifiethernet
                self.ota_page.input_release_OTA_package(release_info)
                log.info("平台释放ota升级包指令下达成功")
                # self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_received_alert(download_tips)
                log.info("终端弹出下载提示框并且点击确认下载")

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
                    self.ota_page.time_sleep(5)
                    log.info("等待...")
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.ping_network(timeout=300)
                    log.info("打开wifi开关并且确认可以上网")

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
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        err_msg = "@@@@断网重连%d次， 30分钟后还没有下载完相应的ota package， 请检查！！！" % times
                        log.error(err_msg)
                        assert False, err_msg
                        # raise Exception(err_msg)
                    self.ota_page.time_sleep(10)
                log.info("*******************ota包下载完成**************************")
                # 对比 update包
                now_time = self.ota_page.get_current_time()
                while True:
                    if "update.zip" in self.android_mdm_page.u2_send_command(
                            "ls %s/" % self.android_mdm_page.get_internal_storage_directory()):
                        updated_hash_value = self.android_mdm_page.calculate_updated_sha256_in_device()
                        log.info("update.zip 包的md5值为： %s" % updated_hash_value)
                        if updated_hash_value == act_ota_package_hash_value:
                            log.info("拷贝的update 包完整性一致")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        err_msg = "@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包， 请检查！！！"
                        log.error(err_msg)
                        assert False, err_msg
                        # raise Exception(err_msg)
                    self.ota_page.time_sleep(3)

                log.info("*******************根目录ota包拷贝完成完成**************************")

                # 检测copy update包是否完整
                self.ota_page.go_to_new_address("ota/log")
                report_now_time = self.ota_page.get_current_time()
                while True:
                    info = self.ota_page.get_ota_latest_upgrade_log(send_time, release_info)
                    if len(info) != 0:
                        action = info[0]["Action"]
                        log.info("平台upgrade action: %s" % action)
                        if self.ota_page.get_action_status(action) == 2 or self.ota_page.get_action_status(action) == 4 \
                                or self.ota_page.get_action_status(action) == 3:
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
                    self.android_mdm_page.screen_keep_on()
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









