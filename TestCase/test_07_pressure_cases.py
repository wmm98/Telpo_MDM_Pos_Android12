import allure
import pytest
import TestCase as case_pack
import sys

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
test_yml = case_pack.yaml_data


class TestPressureTesting:
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
        self.pass_flag = 0

    def teardown_class(self):
        # pass
        self.app_page.delete_app_install_and_uninstall_logs()
        self.android_mdm_page.del_all_downloaded_apk()
        self.android_mdm_page.uninstall_multi_apps(test_yml['app_info'])
        self.android_mdm_page.del_updated_zip()
        self.android_mdm_page.reboot_device(self.wifi_ip)

    @allure.feature('Pressure_Test-case0')
    @allure.title("OTA - OTA下载拷贝校验完整性压测")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=100, reruns_delay=3)
    def test_OTA_pressure_testing_01(self, recover_and_login_mdm, fake_ota_package_operation,
                                     connect_wifi_adb_USB, del_all_ota_release_log,
                                     delete_ota_package_relate):


        while True:
            try:
                self.ota_page.delete_all_ota_release_log()
                self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                self.android_mdm_page.open_root_auth_usb()
                self.android_mdm_page.del_data_zip()
                self.android_mdm_page.del_updated_zip()
                self.android_mdm_page.del_all_downloaded_zip()
                self.android_mdm_page.confirm_wifi_btn_open()

                log.info("*******************OTAOTA-OTA 下载拷贝校验完整性开始***************************")
                download_tips = "Foundanewfirmware,whethertoupgrade?"
                upgrade_tips = "whethertoupgradenow?"
                exp_success_text = "success"
                exp_existed_text = "ota release already existed"
                release_info = {"package_name": test_yml['ota_packages_info']['package_name'], "sn": self.device_sn,
                                "category": "NO Limit", "network": "NO Limit"}
                self.android_mdm_page.reboot_device(self.wifi_ip)
                self.android_mdm_page.open_root_auth_usb()
                # self.android_mdm_page.reboot_device_root(self.wifi_ip)
                # check if device is online
                opt_case.confirm_device_online(release_info["sn"])
                times = 2
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
                print("固件升级的目标版本%s" % release_info["version"])
                # check file size and hash value in directory Param/package
                # ota_package_path = self.android_mdm_page.get_apk_path(release_info["package_name"])
                ota_package_path = conf.project_path + '\\Public_Package\\new\\%s' % release_info["package_name"]

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
                        #     raise Exception("stop1")
                        # else:
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
                    log.info("关闭wifi按钮")
                    self.android_mdm_page.no_network()
                    log.info("确认断开网络，终端无法上网")
                    self.ota_page.time_sleep(5)
                    log.info("等待...")
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    log.info("打开wifi按钮")
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
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 3700):
                        err_msg = "@@@@1个钟分钟后还没有下载完相应的ota package， 请检查！！！"
                        log.error(err_msg)
                        # assert False, err_msg
                        raise Exception("stop1")

                    self.ota_page.time_sleep(10)
                log.info("*******************ota包下载完成**************************")
                # 对比 update包
                now_time = self.ota_page.get_current_time()
                while True:
                    if "update.zip" in self.android_mdm_page.u2_send_command(
                            "ls %s/" % self.android_mdm_page.get_internal_storage_directory()):
                        updated_hash_value = self.android_mdm_page.calculate_updated_sha256_in_device()
                        log.info("检测到根目录有update包")
                        log.info("update.zip 包的md5值为： %s" % updated_hash_value)
                        if updated_hash_value == act_ota_package_hash_value:
                            log.info("拷贝的update 包完整性一致")
                            break
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 300):
                        err_msg = "@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包， 请检查！！！"
                        log.error(err_msg)
                        # assert False, err_msg
                        raise Exception("stop2")
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

                self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_alert_show(timeout=300)
                log.info("*****************检测到有升级提示框********************")
                try:
                    self.android_mdm_page.confirm_received_alert(upgrade_tips)
                except Exception as e:
                    self.android_mdm_page.confirm_received_alert(upgrade_tips)

                # 检测data 分区的update包
                # 对比 update包
                # 如果是金融或者user版本， 不检测data分区
                if not test_yml["MDMTestData"]["android_device_info"]["is_user"]:
                    if self.android_mdm_page.get_device_info()['model'] not in ['P8']:
                        now_time = self.ota_page.get_current_time()
                        self.android_mdm_page.open_root_auth_usb()
                        while True:
                            if "update.zip" in self.android_mdm_page.send_shell_command("ls data"):
                                data_updated_hash_value = self.android_mdm_page.calculate_data_updated_sha256_in_device()
                                log.info("检测到data 分区 有update包")
                                log.info("update.zip 包的md5值为： %s" % data_updated_hash_value)
                                if data_updated_hash_value == act_ota_package_hash_value:
                                    log.info("分区拷贝的update 包完整性一致")
                                    break
                            if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 60):
                                err_msg = "@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包到data分区， 请检查！！！"
                                log.error(err_msg)
                                # assert False, err_msg
                                raise Exception("stop3")
                            self.ota_page.time_sleep(3)
                        log.info("**********data 分区update 包拷贝完成**************************")

                self.pass_flag += 1
                log.info("************900P: md5值检测通过%d次*****************" % self.pass_flag)
                log.info("*******************OTA-OTA 下载拷贝校验完整性用例结束***************************")
                log.info("****************************ota升级升级包下载完成***************************")
                print("************900P: md5值检测通过%d次*****************" % self.pass_flag)
            except Exception as e:
                log.info("捕捉到的异常：%s" % str(e))
                if self.ota_page.service_is_normal("ota", case_pack.user_info):
                    if self.android_mdm_page.mdm_msg_alert_show():
                        text = self.android_mdm_page.get_msg_tips_text()
                        log.info("900P 在点击了升级后弹出了弹框，， 提示为：%s" % text)
                        alert.getAlert("900P 在点击了升级后弹出了弹框，请检查， 请检查！！！！")
                        raise Exception("900P 在点击了升级后弹出了弹框，请检查， 请检查！！！！")
                    if "stop1" in str(e):
                        alert.getAlert("900P 超过60分钟还没下载的包MD5值可能有问题， 检查下包的大小和MD5值， 请检查！！！！")
                        log.error("900P 超过60分钟还没下载的包MD5值可能有问题， 检查下包的大小和MD5值， 请检查！！！！")
                        sys.exit()
                        # raise Exception("下载的包MD5值有问题")
                    elif "stop2" in str(e):
                        alert.getAlert("@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包, 根目录update包MD5值有问题，请检查！！！")
                        log.error("@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包, 根目录update包MD5值有问题，请检查！！！")
                        sys.exit()
                        # raise Exception("根目录update包MD5值有问题")
                    elif "stop3" in str(e):
                        alert.getAlert(" @@@@ 5分钟内分钟后还没有拷贝完相应update.zip包到data分区, data分区update包MD5值有问题，请检查！！！")
                        log.error("@@@@ 5分钟内分钟后还没有拷贝完相应update.zip包到data分区, data分区update包MD5值有问题，请检查！！！")
                        sys.exit()
                        # raise Exception("900P data分区update包MD5值有问题，请检查！！！")
                    else:
                        self.ota_page.delete_all_ota_release_log()
                        self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                        self.android_mdm_page.open_root_auth_usb()
                        self.android_mdm_page.del_data_zip()
                        self.android_mdm_page.del_updated_zip()
                        self.android_mdm_page.del_all_downloaded_zip()
                        self.android_mdm_page.confirm_wifi_btn_open()
                        # assert False, e
                else:
                    self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                    self.android_mdm_page.confirm_wifi_status_open()
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    log.info("**********************检测到服务器503***********************")
                    self.ota_page.recovery_after_service_unavailable("ota", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.ota_page.delete_all_ota_release_log()
                    self.android_mdm_page.del_all_downloaded_zip()
                    self.android_mdm_page.del_updated_zip()
                    self.ota_page.go_to_new_address("ota")

    @allure.feature('Pressure_Test-case1')
    @allure.title("APP - APP大附件断点压测")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=1000, reruns_delay=3)
    def test_APK_pressure_testing_01(self, recover_and_login_mdm, Big_APk_operation,
                                     connect_wifi_adb_USB, del_app_install_uninstall_release_log,
                                     del_download_apk, uninstall_big_size_app):

        apk_path = conf.project_path + '\\Public_Package\\APK\\APK_test_pressure.apk'
        apk_name = 'APK_test_pressure.apk'
        release_info = {"package_name": apk_name, "sn": self.device_sn, "silent": "Yes", "download_network": "NO Limit"}
        apk_package_name = self.app_page.get_apk_package_name(apk_path)
        release_info["package"] = apk_package_name
        version = self.app_page.get_apk_package_version(apk_path)
        release_info["version"] = version

        while True:
            try:
                self.app_page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                self.android_mdm_page.del_all_downloaded_apk()
                self.android_mdm_page.uninstall_app(apk_package_name)
                self.android_mdm_page.confirm_wifi_btn_open()

                log.info("*******************APP大附件断点续传压测开始***************************")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                opt_case.confirm_device_online(release_info["sn"])
                times = 2
                self.ota_page.go_to_new_address("apps")
                self.android_mdm_page.screen_keep_on()
                # get release ota package version
                original_app_md5_value = self.app_page.calculate_sha256_in_windows(apk_name, 'Public_Package\\APK')
                log.info("app的MD5值为：%s" % original_app_md5_value)
                app_size = self.app_page.get_file_size_in_windows(file_path=apk_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))
                # self.android_mdm_page.start_app()
                # go to app page
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.search_app_by_name(release_info["package_name"])
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
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % shell_app_apk_name)
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % shell_app_apk_name
                log.info("**********************终端中检测到下载记录**********************************")

                package_size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
                log.info("断网前下载的的app size: %s" % str(package_size))
                flag = False
                times = 0
                while True:
                    self.android_mdm_page.disconnect_ip(self.wifi_ip)
                    self.android_mdm_page.close_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_close()
                    log.info("关闭wifi按钮")
                    self.android_mdm_page.no_network()
                    log.info("确认断开网络，终端无法上网")
                    self.ota_page.time_sleep(90)
                    log.info("等待...")
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_btn_open()
                    log.info("打开wifi按钮")
                    self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.ping_network(timeout=300)
                    log.info("打开wifi开关并且确认可以上网")

                    while True:
                        current_size = self.android_mdm_page.get_file_size_in_device_USB(shell_app_apk_name)
                        log.info("断网%s次之后当前ota package 的size: %s" % (str(times + 1), current_size))
                        if current_size == app_size:
                            # 大小一样的情况下检查MD5值
                            shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                            log.info("终端中下载中app 的hash_value: %s" % shell_hash_value)
                            if original_app_md5_value == shell_hash_value:
                                flag = True
                                break
                        if current_size > package_size:
                            package_size = current_size
                            break
                        if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 180):
                            err_msg = "@@@@确认下载提示后， 2分钟内apk升级包没有大小没变， 没在下载， 请检查！！！"
                            print(err_msg)
                            log.error(err_msg)
                            assert False, err_msg
                        self.ota_page.time_sleep(3)
                        # 断网完成
                    # 间隔1分钟再断点
                    self.app_page.time_sleep(60)
                    if flag:
                        break
                    now_time = self.app_page.get_current_time()
                    if self.ota_page.get_current_time() > self.ota_page.return_end_time(now_time, 3600):
                        log.error("@@@@一个钟还没下载完apk， 请检查！！！")
                        sys.exit()
                log.info("*******************完成%d次断网操作*********************************" % (times + 1))

                # check if download completed
                # now_time = self.app_page.get_current_time()
                # original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                #     "%s" % release_info["package_name"])
                # log.info("原包的 hash value: %s" % original_hash_value)
                # while True:
                #     shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                #     log.info("终端中下载中app 的hash_value: %s" % shell_hash_value)
                #     if original_hash_value == shell_hash_value:
                #         break
                #     if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 1800):
                #         log.info("@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"])
                #         assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
                #     self.app_page.time_sleep(10)
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
                self.pass_flag += 1
                log.info("**********APP大附件断点续传压测结束 %d 次**************" % self.pass_flag)
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

    @allure.feature('Pressure_Test-case2')
    @allure.title("APP - APP大附件压测")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=1000, reruns_delay=3)
    def test_APK_pressure_testing_02(self, recover_and_login_mdm, Big_APk_operation,
                                     connect_wifi_adb_USB, del_app_install_uninstall_release_log,
                                     del_download_apk, uninstall_big_size_app):

        apk_path = conf.project_path + '\\Public_Package\\APK\\APK_test_pressure.apk'
        apk_name = 'APK_test_pressure.apk'
        release_info = {"package_name": apk_name, "sn": self.device_sn, "silent": "Yes", "download_network": "NO Limit"}
        apk_package_name = self.app_page.get_apk_package_name(apk_path)
        release_info["package"] = apk_package_name
        version = self.app_page.get_apk_package_version(apk_path)
        release_info["version"] = version

        while True:
            try:
                self.app_page.delete_app_install_and_uninstall_logs()
                self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                self.android_mdm_page.del_all_downloaded_apk()
                self.android_mdm_page.uninstall_app(apk_package_name)
                self.android_mdm_page.confirm_wifi_btn_open()

                log.info("*******************APP大附件压测开始***************************")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                # check if device is online
                opt_case.confirm_device_online(release_info["sn"])
                times = 2
                self.ota_page.go_to_new_address("apps")
                self.android_mdm_page.screen_keep_on()
                # get release ota package version
                original_app_md5_value = self.app_page.calculate_sha256_in_windows(apk_name, 'Public_Package\\APK')
                log.info("app的MD5值为：%s" % original_app_md5_value)
                app_size = self.app_page.get_file_size_in_windows(file_path=apk_path)
                log.info("获取到的app 的size(bytes): %s" % str(app_size))
                # self.android_mdm_page.start_app()
                # go to app page
                send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                    case_pack.time.localtime(self.app_page.get_current_time()))
                self.app_page.time_sleep(10)
                self.app_page.search_app_by_name(release_info["package_name"])
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
                        log.error("@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % shell_app_apk_name)
                        assert False, "@@@@多应用推送中超过3分钟还没有app: %s的下载记录" % shell_app_apk_name
                log.info("**********************终端中检测到下载记录**********************************")

                # check if download completed
                now_time = self.app_page.get_current_time()
                original_hash_value = self.android_mdm_page.calculate_sha256_in_windows(
                    "%s" % release_info["package_name"], "Public_Package\\APK")
                log.info("原包的 hash value: %s" % original_hash_value)
                while True:
                    shell_hash_value = self.android_mdm_page.calculate_sha256_in_device(shell_app_apk_name)
                    log.info("终端中下载中app 的hash_value: %s" % shell_hash_value)
                    if original_hash_value == shell_hash_value:
                        break
                    if self.app_page.get_current_time() > self.app_page.return_end_time(now_time, 3600):
                        log.error("@@@@多应用推送中超过30分钟还没有完成%s的下载, 请检查！！！" % release_info["package_name"])
                        sys.exit()
                        # assert False, "@@@@多应用推送中超过30分钟还没有完成%s的下载" % release_info["package_name"]
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

                self.pass_flag += 1
                log.info("**********APP大附件压测结束 %d 次**************" % self.pass_flag)

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
