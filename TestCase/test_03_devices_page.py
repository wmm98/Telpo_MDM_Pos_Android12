import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
test_yml = case_pack.yaml_data
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()

data_cate_mode = [{"cate": "台式2", "model": "M1"},
                  {"cate": "壁挂式-test", "model": "TPS980P-test"}]

devices = [{"name": "TPS980-cc", "SN": "3180980P12300283", "cate": "壁挂式", "model": "TPS980P"},
           {"name": "M1K-MM", "SN": "00002002000000000", "cate": "手持终端", "model": "M1"}]


class TestDevicesPage:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.DevicesPage(self.driver, 40)
        self.meg_page = case_pack.MessagePage(self.driver, 40)
        self.cat_log_page = case_pack.CatchLogPage(self.driver, 40)
        self.telpo_mdm_page = case_pack.TelpoMDMPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.page.go_to_new_address("devices")
        # self.android_mdm_page.device_unlock()

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('MDM_device_test')
    @allure.story('MDM-Show')
    @allure.title("Devices- 锁机和解锁")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    def test_lock_and_unlock_single_device(self, recover_and_login_mdm, go_to_and_return_device_page):
        while True:
            try:
                log.info("*******************锁机和解锁用例开始********************")
                sn = self.device_sn
                opt_case.confirm_device_online(sn)
                self.android_mdm_page.screen_keep_on()
                # case is stable
                exp_lock_msg = "Device %s Locked" % sn
                exp_unlock_msg = "Device %s UnLocked" % sn
                lock_tips = "pls contact the administrator to unlock it!"
                for k in range(2):
                    # test lock btn
                    opt_case.check_single_device(sn)
                    log.info("检测到设备： %s 在线" % sn)
                    self.page.select_device(sn)
                    self.page.click_lock()
                    log.info("平台发送锁定设备： %s指令" % sn)
                    # assert 1 == 0
                    self.page.refresh_page()
                    # check if device lock already
                    now_time = self.page.get_current_time()
                    while True:
                        if "Locked" in opt_case.get_single_device_list(sn)[0]["Lock Status"]:
                            log.info("已经锁定设备")
                            break
                        if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                            log.error("@@@@锁定设备指令发送失败，请检查！！！！")
                            assert False, "@@@@锁定设备指令发送失败，请检查！！！！"
                        self.page.refresh_page()
                        self.page.time_sleep(1)

                    # go to device and check the lock alert
                    assert self.android_mdm_page.mdm_msg_alert_show(180), "@@@@180s后还没显示锁定设备， 请检查！！！"
                    self.android_mdm_page.confirm_received_text(lock_tips)
                    log.info("设备弹框文本为： %s" % lock_tips)
                    self.page.refresh_page()

                    opt_case.get_single_device_list(sn)
                    self.page.select_device(sn)
                    self.page.click_unlock()
                    log.info("平台发送解锁设备： %s指令" % sn)
                    assert self.android_mdm_page.confirm_msg_alert_fade(
                        self.page.remove_space(lock_tips)), "@@@@60s后还没解锁， 请检查！！！"
                    self.page.refresh_page()
                    now_time = self.page.get_current_time()
                    for j in range(5):
                        if "Normal" in opt_case.get_single_device_list(sn)[0]["Lock Status"]:
                            log.info("解锁成功")
                            break
                        if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                            log.info("@@@@解锁失败，请检查！！！！")
                            assert False, "@@@@解锁失败，请检查！！！！"
                        self.page.refresh_page()
                        self.page.time_sleep(1)
                log.info("********************锁机和解锁用例结束**************************")
                break
            except Exception as e:
                if self.page.service_is_normal("apps", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("apps", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("devices")

    @allure.feature('MDM_device_test')
    @allure.title("Devices- 发送设备重启指令：设备重启5次")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reboot_single_device_pressure_testing(self, recover_and_login_mdm, connected_wifi_adb, go_to_and_return_device_page):
        while True:
            try:
                log.info("****************发送设备重启指令：设备重启5次用例开始***********************")
                exp_reboot_text = "Sending Reboot Comand to Devices"
                self.android_mdm_page.screen_keep_on()
                sn = self.device_sn
                self.page.refresh_page()
                for i in range(5):
                    log.info("*************第%d次重启****************" % (i + 1))
                    opt_case.confirm_device_online(sn)
                    self.page.select_device(sn)
                    self.android_mdm_page.disconnect_ip(self.wifi_ip)
                    self.page.click_reboot_btn()
                    for j in range(10):
                        case_pack.time.sleep(3)
                        log.info("等待3秒")
                        self.page.refresh_page()
                        # get device info
                        # check if command trigger in 3s
                        if "Off" in opt_case.get_single_device_list(sn)[0]["Status"]:
                            log.info("设备重启下线， 指令在3s内触发")
                            break
                    assert "Off" in opt_case.get_single_device_list(sn)[0]["Status"]
                    log.info("设备重启下线， 指令在3s内触发")
                    self.page.time_sleep(4)
                    self.android_mdm_page.confirm_usb_adb_connect(self.wifi_ip)
                    # self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
                    self.android_mdm_page.device_existed(self.wifi_ip)
                    self.android_mdm_page.device_boot_complete()
                    log.info("设备启动完成")
                    self.android_mdm_page.screen_keep_on()
                    # wait device network normal
                    self.android_mdm_page.ping_network_wifi()
                    log.info("确认注册上网络")
                    now_time = self.page.get_current_time()
                    while True:
                        self.page.refresh_page()
                        if "On" in opt_case.get_single_device_list(sn)[0]["Status"]:
                            log.info("检测到设备在线")
                            break
                        if self.page.get_current_time() > self.page.return_end_time(now_time, 180):
                            assert False, "@@@@恢复网络后3分钟内没与平台通讯！！"
                        self.page.time_sleep(1)
                    print("成功运行 %s 次" % str(i))
                    # case_pack.connect.reconnect(self.wifi_ip)
                log.info("*************发送设备重启指令：设备重启5次结束****************")
                break
            except Exception as e:
                if self.page.service_is_normal("apps", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("apps", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("apps")

    @allure.feature('MDM_device_test')
    @allure.title("Devices- 重置设备TPUI密码")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reset_TPUI_password(self, recover_and_login_mdm, go_to_and_return_device_page):
        while True:
            tpui_apk = case_pack.yaml_data["work_app"]["tpui_apk"]
            tpui_path = conf.project_path + "\\Param\\Work_APP\\%s" % tpui_apk
            tpui_package_name = self.page.get_apk_package_name(tpui_path)
            try:
                log.info("***************重置设备TPUI密码用例开始*********************")
                exp_psw_text = "Password changed"
                sn = self.device_sn
                password = ["123456", "000000", "999999"]
                self.android_mdm_page.screen_keep_on()
                self.android_mdm_page.confirm_app_installed(tpui_path)
                log.info("确认已经安装好tpui软件")
                self.page.refresh_page()
                for psw in password:
                    opt_case.confirm_device_online(sn)
                    log.info("检测到设备在线")
                    self.android_mdm_page.confirm_app_is_running(tpui_package_name)
                    log.info("tpui软件在运行中")
                    self.page.select_device(sn)
                    self.page.click_psw_btn()
                    self.page.change_TPUI_password(psw)
                    log.info("平台修改tpui： %s 密码" % psw)
                    self.page.time_sleep(1)
                    self.android_mdm_page.input_tpui_password(psw)
                    log.info("设备中输入密码提交成功登录")
                    self.android_mdm_page.stop_app(tpui_package_name)
                    log.info("停止运行tpui软件")
                    self.page.refresh_page()
                self.android_mdm_page.confirm_app_is_uninstalled(tpui_package_name)
                log.info("确认已经卸载tpui软件")
                log.info("********************重置设备TPUI密码用例结束********************")
                break
            except Exception as e:
                self.android_mdm_page.confirm_app_is_uninstalled(tpui_package_name)
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("devices")

    @allure.feature('MDM_device_test')
    @allure.title("Devices- 重置设备密码")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reset_device_password(self, recover_and_login_mdm, go_to_and_return_device_page):
        while True:
            try:
                log.info("*****************重重置设备密码用例开始***************")
                exp_psw_text = "Password changed"
                self.android_mdm_page.screen_keep_on()
                sn = self.device_sn
                lock_tips = "pls contact the administrator to unlock it!"
                password = ["123456", "000000", "999999"]
                self.page.refresh_page()
                for psw in password:
                    opt_case.confirm_device_online(sn)
                    log.info("检测到设备： %s 在线" % sn)
                    self.page.select_device(sn)
                    self.page.click_psw_btn()
                    self.page.change_device_password(psw)
                    log.info("平台修改设备的密码为： %s" % psw)
                    # lock device
                    self.page.select_device(sn)
                    self.page.click_lock()
                    log.info("锁住设备: %s" % sn)
                    # input password in device
                    assert self.android_mdm_page.mdm_msg_alert_show(time_out=5), "@@@@180s后还没显示锁机，请检查！！！"
                    self.android_mdm_page.confirm_received_text(lock_tips)
                    log.info("确认已经锁机")
                    # need to click confirm btn six times, device would disappear
                    self.android_mdm_page.manual_unlock()
                    log.info("设备点击6次进入密码框")
                    try:
                        self.android_mdm_page.lock_psw_box_presence()
                        self.android_mdm_page.lock_psw_input(psw)
                    except:
                        self.page.time_sleep(1)
                        log.info("再次解锁")
                        self.android_mdm_page.manual_unlock()
                        self.android_mdm_page.lock_psw_input(psw)
                    self.android_mdm_page.click_psw_confirm_btn()
                    log.info("输入密码: %s提交" % psw)
                    assert self.android_mdm_page.confirm_psw_alert_fade(), "@@@@无法确认密码， 请检查！！！"
                    log.info("设备： %s确认解锁" % sn)
                    self.page.refresh_page()
                log.info("*****************重重置设备密码用例结束***************")
                break
            except Exception as e:
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("devices")

    @allure.feature('MDM_device_test')
    @allure.title("Devices- AIMDM发消息压力测试")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_pressure_send_message_to_single_device(self, recover_and_login_mdm, unlock_screen, go_to_and_return_device_page):
        while True:
            # 设置发送消息的次数
            length = 5
            try:
                log.info("***************AIMDM发消息压力测试用例开始*******************")
                exp_success_send_text = "Message Sent"
                # sn would change after debug with devices
                self.android_mdm_page.screen_keep_on()
                sn = self.device_sn
                # confirm if device is online and execute next step, if not, end the case execution
                opt_case.confirm_device_online(sn)
                data = opt_case.check_single_device(sn)
                # print(data)
                if self.page.upper_transfer("Locked") in self.page.remove_space_and_upper(
                        data[0]["Lock Status"]):
                    self.page.select_device(sn)
                    self.page.click_unlock()
                self.android_mdm_page.clear_download_and_upgrade_alert()
                log.info("设备清屏成功")
                # get device category
                device_cate = data[0]['Category']
                now = case_pack.time.strftime('%Y-%m-%d %H:%M', case_pack.time.localtime(case_pack.time.time()))
                message_list = []
                for i in range(length):
                    self.page.refresh_page()
                    log.info("检测到设备：%s 在线" % sn)
                    msg = "%s:#$*%d" % (now, i)
                    opt_case.check_single_device(sn)
                    self.page.select_device(sn)
                    self.page.click_send_btn()
                    self.page.msg_input_and_send(msg)
                    log.info("发送消息： %s 成功" % msg)
                    message_list.append(msg)
                    # check message in device
                    wait_time = 180
                    now_time = self.page.get_current_time()
                    while True:
                        if self.android_mdm_page.mdm_msg_alert_show():
                            break
                        if self.page.get_current_time() > self.page.return_end_time(now_time, wait_time):
                            assert False, "@@@@%ss内无法接收到信息， 请检查设备是否在线！！！！" % wait_time

                    self.android_mdm_page.confirm_received_text(msg)
                    log.info("设备：%s已经接收到消息" % msg)
                    try:
                        self.android_mdm_page.click_msg_confirm_btn()
                        self.android_mdm_page.confirm_msg_alert_fade(msg)
                    except Exception:
                        pass
                log.info("去到Message模块查看设备接收信息的上报情况")
                self.page.go_to_new_address("message")
                # check if Page loaded completely
                self.meg_page.page_load_complete()
                # Check result of device message in the Message Module and msg status
                self.meg_page.choose_device(sn, device_cate)
                now_time = self.page.get_current_time()
                # res = self.meg_page.get_device_message_list(now)
                # print(res)
                while True:
                    receive_list = self.meg_page.get_device_message_list(now)
                    if len(receive_list) >= length:
                        msg_list = [self.page.remove_space(m['message']) for m in receive_list[:length]]
                        for meg in message_list:
                            if self.page.remove_space(meg) not in msg_list:
                                log.error("@@@@平台反馈终端接收的信息有误， 请检查！！！！")
                                assert False, "@@@@平台反馈终端接收的信息有误， 请检查！！！！"
                        status_list = [i['status'].upper() for i in receive_list[:length]]
                        if len(msg_list) == length and status_list.count("Successed".upper()) == length:
                            log.info("平台Message模块中设备接收所有发送的信息")
                            break
                    if self.page.get_current_time() > self.page.return_end_time(now_time):
                        log.info("@@@终端收到信息后, 平台180s内无法收到相应的信息")
                        assert False, "@@@终端收到信息后, 平台180s内无法收到相应的信息"
                    self.page.time_sleep(1)
                log.info("*******************AIMDM发消息压力测试用例结束************************")
                break
            except Exception as e:
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("devices")

    @allure.feature('MDM_device_test--no test -now')
    @allure.title("Devices- 恢复出厂设置压测10次， 计算准备率")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_factory_recovery_pressure_testing(self, recover_and_login_mdm, go_to_and_return_device_page):
        self.page.factory_reset()
        now_time = self.page.get_current_time()
        while True:
            if "Off" in opt_case.get_single_device_list(self.device_sn)[0]["Status"]:
                self.page.device_not_existed(self.wifi_ip)
                break
            if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                assert False, "1分钟内无法触发恢复出厂设置， 请检查！！！！"
            self.page.time_sleep(1)

        # self.android_mdm_page.confirm_wifi_adb_connected(self.wifi_ip)
        # self.android_mdm_page.device_existed(self.wifi_ip)
        # self.android_mdm_page.device_boot_complete()

    @allure.feature('MDM_device_test')
    @allure.story('MDM-Show')
    @allure.title("Devices- AIMDM 切换正式测试服服务api ")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_transfer_api_server(self, recover_and_login_mdm, push_test_api_to_device):
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
                self.page.refresh_page()
                self.page.page_load_complete()
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
                self.page.select_device(sn)
                # log.info("当前设备的api地址为： %s" % self.android_mdm_page.u2_send_command(
                #             "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])))
                log.info("当前设备的api地址为： %s" % self.android_mdm_page.get_mdmApiUrl_text())
                self.page.click_server_btn()
                self.page.api_transfer(release_version_api)
                log.info("设备切换服务器B： %s指令下达" % release_version_api)
                self.page.time_sleep(5)
                flag_f = 0
                now_time = self.page.get_current_time()
                while True:
                    if release_version_api in self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                        log.info("终端根目录下的aip 已经改变为服务器A的 api: %s" % release_version_api)
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time):
                        flag_f += 1
                        break
                    self.page.time_sleep(10)

                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("成功重启设备")
                if flag_f != 0:
                    # check if the api had changed in device
                    log.info("检测到终端api变化情况")
                    now_time = self.page.get_current_time()
                    while True:
                        api_text = self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"]))
                        log.info("根目录下的api: %s" % api_text)
                        if release_version_api in api_text:
                            log.info("终端根目录下的api 已经变为服务器B的api：%s" % release_version_api)
                            break
                        if self.page.get_current_time() > self.page.return_end_time(now_time):
                            log.error("3分钟内终端还没改为服务器B的api： %s" % release_version_api)
                            assert False, "3分钟内终端还没改为服务器B的api： %s" % release_version_api
                        self.page.time_sleep(20)
                log.info("终端检测已经切换为服务器B的api: %s" % release_version_api)
                # check if device is offline in test version
                # self.page.refresh_page()
                # test_device_info = opt_case.get_single_device_list(sn)
                log.info("检测平台A中设备: %s的在线情况" % sn)
                online_time = self.page.get_current_time()
                reboot_flag = 0
                while True:
                    self.page.refresh_page()
                    if "OFF" in self.page.remove_space(
                            self.page.upper_transfer(opt_case.get_single_device_list(sn)[0]["Status"])):
                        log.info("测试平台A已经显示设备下线")
                        break
                    if self.page.get_current_time() > self.page.return_end_time(online_time, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time = self.page.get_current_time()
                        else:
                            log.error("@@@@3分钟内当前平台A显示设备还在线， 请检查！！！")
                            assert False, "@@@@3分钟内当前平台A显示设备还在线， 请检查！！！"
                    self.page.time_sleep(2)

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
                online_time1 = self.page.get_current_time()
                while True:
                    self.page.refresh_page()
                    if "ON" in self.page.remove_space(
                            self.page.upper_transfer(release_page.get_single_device_list_release(sn)[0]["Status"])):
                        log.info("测试平台B已经显示设备在线")
                        break
                    if self.page.get_current_time() > self.page.return_end_time(online_time1, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time1 = self.page.get_current_time()
                        else:
                            log.error("@@@@3分钟内当前平台B一直显示设备下线， 请检查！！！")
                            assert False, "@@@@3分钟内当前平台B一直显示设备下线， 请检查！！！"

                    self.page.time_sleep(2)
                log.info("设备再次切换回 服务器A 的api: %s, 切换回原来的服务器" % test_version_api)
                release_page.select_device(sn)
                # log.info("当前设备的api地址为： %s" % self.android_mdm_page.u2_send_command(
                #     "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])))
                log.info("当前设备的api地址为： %s" % self.android_mdm_page.get_mdmApiUrl_text())
                release_page.click_server_btn()
                release_page.api_transfer(test_version_api)
                log.info("切换服务器 api : %s指令下达成功" % test_version_api)
                flag = 0
                now_time = self.page.get_current_time()
                log.info("重启前检测终端api变化")
                while True:
                    if test_version_api in self.android_mdm_page.u2_send_command(
                            "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                        log.info("终端根目录下的aip 已经改变为服务器A的 api: %s" % test_version_api)
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 120):
                        flag += 1
                        break
                    self.page.time_sleep(10)

                self.android_mdm_page.reboot_device(self.wifi_ip)
                log.info("设备重启成功")

                if flag != 0:
                    log.info("重启后检测终端api变化")
                    reboot_flag = 0
                    online_time2 = self.page.get_current_time()
                    while True:
                        if test_version_api in self.android_mdm_page.u2_send_command(
                                "cat /%s/%s" % (root_dir, test_yml["work_app"]["api_txt"])):
                            log.info("终端根目录下的aip 已经改变为服务器A的api： %s" % test_version_api)
                            break
                        if self.page.get_current_time() > self.page.return_end_time(online_time2):
                            if reboot_flag == 0:
                                reboot_flag += 1
                                self.android_mdm_page.reboot_device(self.wifi_ip)
                                online_time2 = self.page.get_current_time()
                            else:
                                log.error("设备启动后3分钟内终端api还没改变为服务器A的api： %s, 请检查！！！" % test_version_api)
                                assert False, "设备启动后3分钟内终端api还没改变为服务器A的api： %s, 请检查！！！" % test_version_api
                        self.page.time_sleep(10)

                # check if device is offline in release version
                release_page.refresh_page()
                release_data_info_again = release_page.get_single_device_list_release(sn)
                print(release_data_info_again)

                log.info("检测平台B中设备: %s的在线情况" % sn)
                reboot_flag = 0
                online_time3 = self.page.get_current_time()
                while True:
                    self.page.refresh_page()
                    if "OFF" in self.page.remove_space(
                            self.page.upper_transfer(release_page.get_single_device_list_release(sn)[0]["Status"])):
                        log.info("检测到平台B中设备：%s显示下线状态" % sn)
                        break
                    if self.page.get_current_time() > self.page.return_end_time(online_time3, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time3 = self.page.get_current_time()
                        else:
                            log.error("@@@@3分钟内检测到平台B中设备一直显示在线， 请检查！！！")
                            assert False, "@@@@3分钟内检测到平台B中涉笔一直显示在线， 请检查！！！"
                    self.page.time_sleep(5)

                log.info("检测平台A中设备: %s的在线情况" % sn)
                # go to test version and check if device is online
                self.page.refresh_page()
                test_data_info = opt_case.get_single_device_list(sn)
                print(test_data_info)
                reboot_flag = 0
                online_time4 = self.page.get_current_time()
                while True:
                    self.page.refresh_page()
                    if "ON" in self.page.remove_space(
                            self.page.upper_transfer(opt_case.get_single_device_list(sn)[0]["Status"])):
                        log.info("平台A中设备：%s 显示在线状态" % sn)
                        break
                    if self.page.get_current_time() > self.page.return_end_time(online_time4, 180):
                        if reboot_flag == 0:
                            reboot_flag += 1
                            self.android_mdm_page.reboot_device(self.wifi_ip)
                            online_time4 = self.page.get_current_time()
                        else:
                            log.error("@@@@3分钟内检测到平台A中设备一直显示下线， 请检查！！！")
                            assert False, "@@@@3分钟内检测到平台A中设备一直显示下线， 请检查！！！"
                    self.page.time_sleep(2)
                release_page.quit_browser()
                log.info("*****************AIMDM 切换正式测试服服务api 测试用例结束****************")
                break
            except Exception as e:
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    api_path = conf.project_path + "\\Param\\Work_APP\\%s" % test_yml["work_app"]["api_txt"]
                    if test_yml["website_info"]["test_api"] not in self.android_mdm_page.get_mdmApiUrl_text():
                        self.android_mdm_page.push_file_to_device(api_path,
                                                                  "/" + self.android_mdm_page.get_internal_storage_directory() + "/")
                    self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.page.go_to_new_address("devices")

    @allure.feature('MDM_device_test')
    @allure.title("Devices- 日志的抓取")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_cat_logs(self, recover_and_login_mdm, go_to_and_return_device_page):
        durations = [5, 10, 30]
        # durations = [5]
        while True:
            try:
                log.info("*****************日志的抓取用例开始********************")
                opt_case.confirm_device_online(self.device_sn)
                for duration in durations:
                    exp_log_msg = "Device Debug Command sent"
                    sn = self.device_sn
                    # self.android_mdm_page.reboot_device(self.wifi_ip)
                    self.page.refresh_page()
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(case_pack.time.time()))
                    opt_case.catch_logs(sn, duration, time_out=duration * 200)
                    log.info("捕捉%d分钟日志指令下达" % duration)
                    # check if device log generates and upload to allure report
                    self.android_mdm_page.generate_and_upload_log(send_time, "%dmin_" % duration)
                    log.info("***************日志的抓取用例结束******************")
                break
            except Exception as e:
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503*************************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("apps")
