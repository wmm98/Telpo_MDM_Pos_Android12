import allure
import pytest
import TestCase as case_pack

conf = case_pack.Config()
excel = case_pack.ExcelData()
opt_case = case_pack.Optimize_Case()
alert = case_pack.AlertData()
log = case_pack.MyLog()
test_yml = case_pack.yaml_data


class TestRegressionTesting:
    def setup_class(self):
        self.driver = case_pack.test_driver
        self.page = case_pack.DevicesPage(self.driver, 40)
        self.meg_page = case_pack.MessagePage(self.driver, 40)
        self.app_page = case_pack.APPSPage(self.driver, 40)
        self.cat_log_page = case_pack.CatchLogPage(self.driver, 40)
        self.telpo_mdm_page = case_pack.TelpoMDMPage(self.driver, 40)
        self.android_mdm_page = case_pack.AndroidAimdmPage(case_pack.device_data, 5)
        self.wifi_ip = case_pack.device_data["wifi_device_info"]["ip"]
        self.device_sn = self.android_mdm_page.get_device_sn()
        self.page.go_to_new_address("devices")

    def teardown_class(self):
        self.page.refresh_page()

    @allure.feature('RegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("需要测试时回归测试- 锁机和解锁")
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    def test_lock_and_unlock_single_device_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.title("需要测试时回归测试- 发送设备重启指令：设备重启5次")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reboot_single_device_pressure_testing_regression(self, recover_and_login_mdm, connected_wifi_adb,
                                                              go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.title("需要测试时回归测试- 重置设备TPUI密码")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reset_TPUI_password_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.title("需要测试时回归测试- 重置设备密码")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reset_device_password_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.title("需要测试时回归测试- AIMDM发消息压力测试")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_pressure_send_message_to_single_device_regression(self, recover_and_login_mdm, unlock_screen,
                                                               go_to_and_return_device_page):
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
    @allure.title("需要测试时回归测试- 恢复出厂设置压测10次， 计算准备率")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_factory_recovery_pressure_testing_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.title("需要测试时回归测试- 日志的抓取")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_cat_logs_regression(self, recover_and_login_mdm, go_to_and_return_device_page):
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

    @allure.feature('RegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("需要测试时回归测试- 断网重连压测消耗流量情况")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reconnect_get_mobile_data_regression(self, recover_and_login_mdm, connect_wifi_adb_USB):
        while True:
            try:
                log.info("********断网重连获取aimdm消耗的流量用例开始**********")
                length = 1
                # settings interval minutes
                disconnect_time = [2, 4, 6, 8]
                opt_case.confirm_device_online(self.device_sn)
                self.android_mdm_page.back_to_home_USB()
                self.android_mdm_page.confirm_wifi_btn_close()
                self.android_mdm_page.disconnect_ip(self.device_sn)
                log.info("确认关闭wifi")
                self.android_mdm_page.open_mobile_data()
                try:
                    self.android_mdm_page.ping_network(times=5, timeout=60)
                except AssertionError:
                    log.error("@@@@@无法开启移动网络， 请检查！！！！")
                    assert False, "@@@@@无法开启移动网络， 请检查！！！！"
                log.info("确认打开流量卡， 并且可以上网")
                opt_case.confirm_device_online(self.device_sn)
                base_directory = "Mobile_Data_Used"
                first_data_used = 0
                last_data_used = 0
                for i in range(len(disconnect_time)):
                    # self.android_mdm_page.open_mobile_data()
                    self.android_mdm_page.screen_keep_on_USB()
                    # clear all app data before testing
                    self.android_mdm_page.clear_recent_app_USB()
                    # self.android_mdm_page.back_to_home_USB()
                    data_used = self.android_mdm_page.get_aimdm_mobile_data()
                    if i == 0:
                        first_data_used = data_used
                    image_before_disconnect = "%s\\data_used_disconnect_network_%d.jpg" % (base_directory, i)
                    self.android_mdm_page.save_screenshot_to_USB(image_before_disconnect)
                    self.android_mdm_page.upload_image_JPG(
                        conf.project_path + "\\ScreenShot\\%s" % image_before_disconnect,
                        "data_used_disconnect_network_%d" % i)
                    log.info("第%d次断网前前的使用数据详情： %s" % (i, data_used))
                    self.android_mdm_page.clear_recent_app_USB()
                    # self.android_mdm_page.back_to_home_USB()
                    self.android_mdm_page.time_sleep(2)
                    self.android_mdm_page.close_mobile_data()
                    try:
                        self.android_mdm_page.no_network()
                    except AssertionError:
                        log.error("@@@@@无法关闭移动网络， 请检查！！！！")
                        assert False, "@@@@@无法关闭移动网络， 请检查！！！！"
                    # not stable
                    opt_case.confirm_device_offline(self.device_sn)

                    # sleep in settings time
                    self.android_mdm_page.time_sleep(disconnect_time[i] * 60)
                    self.android_mdm_page.open_mobile_data()
                    self.android_mdm_page.screen_keep_on_USB()
                    now_time = self.android_mdm_page.get_current_time()
                    while True:
                        try:
                            if self.android_mdm_page.ping_network():
                                break
                        except AssertionError:
                            pass
                        self.android_mdm_page.open_mobile_data()
                        if now_time > self.page.return_end_time(now_time, 90):
                            assert False, "@@@@@无法开启移动网络， 请检查！！！！"
                        self.page.time_sleep(1)
                    # not stable
                    opt_case.confirm_device_online(self.device_sn)
                    self.android_mdm_page.clear_recent_app_USB()
                    # self.android_mdm_page.back_to_home_USB()
                    data_used_reconnect = self.android_mdm_page.get_aimdm_mobile_data()
                    if i == length - 1:
                        last_data_used = data_used_reconnect
                    image_after_connect = "%s\\data_used_reconnect_network_%d.jpg" % (base_directory, i)
                    self.android_mdm_page.save_screenshot_to_USB(image_after_connect)
                    self.android_mdm_page.upload_image_JPG(conf.project_path + "\\ScreenShot\\%s" % image_after_connect,
                                                           "data_used_reconnect_network_%d" % i)
                    log.info("第%d次重连后的使用数据详情： %s" % (i, data_used_reconnect))
                first_data_float = self.page.remove_space(self.page.extract_integers(first_data_used)[0])
                last_data_float = self.page.remove_space(self.page.extract_integers(last_data_used)[0])
                total_data_used = float(last_data_float) - float(first_data_float)
                data_size = self.android_mdm_page.get_mobile_data_size()
                log.info("总共使用了流量数据： %s %s" % (str(round(total_data_used, 2)), data_size))
                self.android_mdm_page.clear_recent_app_USB()
                # self.android_mdm_page.back_to_home_USB()
                self.android_mdm_page.open_wifi_btn()
                self.android_mdm_page.confirm_wifi_status_open()
                log.info("***************************断网重连获取aimdm消耗的流量用例结束*********************")
                break
            except Exception as e:
                pass
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.android_mdm_page.clear_recent_app_USB()
                    self.android_mdm_page.back_to_home_USB()
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_status_open()
                    self.page.go_to_new_address("devices")

    @allure.feature('RegressionTesting')
    @allure.story('MDM-Show')
    @allure.title("需要测试时回归测试- 断网重连压测消耗流量情况")
    @pytest.mark.dependency(depends=["test_login_ok"], scope='package')
    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    def test_reconnect_silent_upgrade_regression(self, recover_and_login_mdm, connect_wifi_adb_USB, del_app_install_uninstall_release_log,
                                                 del_download_apk, uninstall_multi_apps):
        while True:
            try:
                log.info("********断网重连压测消耗流量情况用例开始**********")
                self.android_mdm_page.reboot_device(self.wifi_ip)
                length = 1
                # settings interval minutes
                disconnect_time = [2, 30]
                #
                apks = [test_yml['app_info']['other_app_limit_network_A'],
                        test_yml['app_info']['other_app_limit_network_B']]
                opt_case.confirm_device_online(self.device_sn)
                self.android_mdm_page.back_to_home_USB()
                self.android_mdm_page.confirm_wifi_btn_close()
                self.android_mdm_page.disconnect_ip(self.device_sn)
                log.info("确认关闭wifi")
                self.android_mdm_page.open_mobile_data()
                try:
                    self.android_mdm_page.ping_network(times=5, timeout=60)
                except AssertionError:
                    log.error("@@@@@无法开启移动网络， 请检查！！！！")
                    assert False, "@@@@@无法开启移动网络， 请检查！！！！"
                log.info("确认打开流量卡， 并且可以上网")
                opt_case.confirm_device_online(self.device_sn)
                #  reconnect loop
                for i in range(len(disconnect_time)):
                    self.android_mdm_page.close_mobile_data()
                    try:
                        self.android_mdm_page.no_network()
                    except AssertionError:
                        log.error("@@@@@无法关闭移动网络， 请检查！！！！")
                        assert False, "@@@@@无法关闭移动网络， 请检查！！！！"
                    # not stable
                    opt_case.confirm_device_offline(self.device_sn)

                    # sleep in settings time
                    self.android_mdm_page.time_sleep(disconnect_time[i] * 60)
                    self.android_mdm_page.open_mobile_data()
                    self.android_mdm_page.screen_keep_on_USB()
                    now_time = self.android_mdm_page.get_current_time()
                    while True:
                        try:
                            if self.android_mdm_page.ping_network():
                                break
                        except AssertionError:
                            pass
                        self.android_mdm_page.open_mobile_data()
                        if now_time > self.page.return_end_time(now_time, 90):
                            assert False, "@@@@@无法开启移动网络， 请检查！！！！"
                        self.page.time_sleep(1)
                    # not stable
                    opt_case.confirm_device_online(self.device_sn)

                    # silent install app relate
                    release_info = {"package_name": apks[i],
                                    "sn": self.device_sn,
                                    "silent": "Yes", "download_network": "NO Limit"}
                    file_path = conf.project_path + "\\Param\\Package\\%s" % release_info["package_name"]
                    package = self.page.get_apk_package_name(file_path)
                    release_info["package"] = package
                    version = self.page.get_apk_package_version(file_path)
                    release_info["version"] = version

                    app_size = self.page.get_file_size_in_windows(file_path)
                    log.info("获取到的app 的size(bytes): %s" % str(app_size))
                    # self.android_mdm_page.start_app()
                    # go to app page
                    self.page.go_to_new_address("apps")
                    send_time = case_pack.time.strftime('%Y-%m-%d %H:%M',
                                                        case_pack.time.localtime(self.page.get_current_time()))
                    self.page.time_sleep(10)
                    self.app_page.search_app_by_name(release_info["package_name"])
                    app_list = self.app_page.get_apps_text_list()
                    if len(app_list) == 0:
                        log.error("@@@@没有 %s, 请检查！！！" % release_info["package_name"])
                        assert False, "@@@@没有 %s, 请检查！！！" % release_info["package_name"]
                    self.app_page.click_release_app_btn()
                    self.app_page.input_release_app_info(release_info)
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
                        upgrade_list = self.app_page.get_app_latest_upgrade_log(send_time, release_info)
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

                self.android_mdm_page.open_wifi_btn()
                self.android_mdm_page.confirm_wifi_status_open()
                log.info("***************************断网重连获静默升级用例结束*********************")
                break
            except Exception as e:
                pass
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.android_mdm_page.clear_recent_app_USB()
                    self.android_mdm_page.back_to_home_USB()
                    self.android_mdm_page.open_wifi_btn()
                    self.android_mdm_page.confirm_wifi_status_open()
                    self.page.go_to_new_address("devices")

    @allure.feature('RegressionTesting-test')
    @allure.title("Devices- 关机 -- test in the last")
    @pytest.mark.flaky(reruns=1, reruns_delay=3)
    def test_device_shutdown_regression(self, recover_and_login_mdm):
        while True:
            try:
                log.info("*******************关机用例开始***************************")
                sn = self.device_sn
                exp_shutdown_text = "Device ShutDown Command sent"
                opt_case.check_single_device(sn)
                self.page.click_dropdown_btn()
                self.page.click_shutdown_btn()
                # check if shutdown command works in 3 sec

                now_time = self.page.get_current_time()
                while True:
                    self.page.refresh_page()
                    if "Off" in opt_case.get_single_device_list(sn)[0]["Status"]:
                        break
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                        assert False, "@@@@已发送关机命令， 平台显示设备1分钟内还显示在线状态"
                # check if device is offline
                now_time = self.page.get_current_time()
                while True:
                    try:
                        self.android_mdm_page.device_not_existed(self.wifi_ip)
                        break
                    except AssertionError:
                        pass
                    self.page.refresh_page()
                    if self.page.get_current_time() > self.page.return_end_time(now_time, 60):
                        assert False, "@@@@关机指令下发1分钟内设备还没下线， 请检查！！！！"

                log.info("**********设备关机用例结束*************")
                break
            except Exception as e:
                if self.page.service_is_normal("devices", case_pack.user_info):
                    assert False, e
                else:
                    log.info("**********************检测到服务器503***********************")
                    self.page.recovery_after_service_unavailable("devices", case_pack.user_info)
                    log.info("**********************服务器恢复正常*************************")
                    self.page.go_to_new_address("devices")
