import Page as public_pack
from Page.Android_Page_USB import AndroidBasePageUSB
from Page.Android_Page_WiFi import AndroidBasePageWiFi
import time

config = public_pack.Config()
log = public_pack.MyLog()

# aimdm_package = public_pack.yaml_data["work_app"]["aidmd_apk"]


class AndroidAimdmPage(AndroidBasePageUSB, AndroidBasePageWiFi):
    def __init__(self, devices_data, times):
        self.client = devices_data["usb_device_info"]["device"]
        self.serial = devices_data["usb_device_info"]["serial"]
        self.wifi_client = devices_data["wifi_device_info"]["device"]
        self.device_ip = devices_data["wifi_device_info"]["ip"]
        AndroidBasePageUSB.__init__(self, self.client, times, self.serial)
        AndroidBasePageWiFi.__init__(self, self.wifi_client, times, self.device_ip)
        self.is_landscape = public_pack.yaml_data["android_device_info"]["is_landscape"]
        aimdm_apk = public_pack.yaml_data["work_app"]["aidmd_apk"]
        tpui_apk = public_pack.yaml_data["work_app"]["tpui_apk"]
        self.aimdm_package = self.get_apk_package_name(config.project_path + "\\Param\\Work_APP\\%s" % aimdm_apk)
        self.tpui_pakcage = self.get_apk_package_name(config.project_path + "\\Param\\Work_APP\\%s" % tpui_apk)
        self.android_settings_package = "com.android.settings"
        self.android_relatelayout_package = "android"
        self.android_osrecent_package = "com.android.common.osrecent"

        # aimdm_package = "com.tpos.aimdm"
        # msg_box related
        self.msg_header_id = "android.widget.TextView"
        self.msg_tips_id = "%s:id/tip" % self.aimdm_package
        self.msg_confirm_id = "%s:id/confirm" % self.aimdm_package
        self.msg_cancel_id = "%s:id/cancel" % self.aimdm_package
        self.msg_alert_id = "%s:id/root_view" % self.aimdm_package
        # 900P  confirm->download->confirm->upgrade

        # lock alert, input device psw relate
        self.lock_psw_id = "%s:id/et_pwd" % self.aimdm_package
        self.psw_confirm_id = "%s:id/confirm_pwd" % self.aimdm_package

        # aimdm app info page
        self.settings_title = "%s:id/entity_header_title" % self.android_settings_package
        self.settings_summary = "%s:id/summary" % self.android_relatelayout_package
        self.container = "%s:id/container_material" % self.android_settings_package
        self.layout = "android.widget.LinearLayout"

        # aimdm more detail info
        self.spinner = "%s:id/cycles_spinner" % self.android_settings_package
        self.total_data_summary = "%s:id/summary" % self.android_relatelayout_package
        self.data_used_title = "Mobile data & Wi‑Fi"

        # clear recent app btn
        self.clear_all = ":id/btn_remove_all"
        self.clear_all_android13 = ":id/clear_all"
        self.recent_panel = ":id/snapshot"
        self.over_view_panel = ":id/overview_panel"

        # tpui relate
        self.tpui_main = "%s:id/layout_main" % self.tpui_pakcage
        # ele[1]
        self.more_btn = "android.widget.ImageView"
        self.psw_box = "%s:id/edit_login_password" % self.tpui_pakcage
        self.tpui_psw_confirm = "%s:id/text_confirm" % self.tpui_pakcage
        self.tpui_pasw_cancel = "%s:id/text_cancel" % self.tpui_pakcage

        # wifi module relate
        # switch btn
        self.wifi_switch_btn = "%s:id/switch_widget" % self.android_relatelayout_package   # ui change compare with android 10, and the same as android 12
        # wifi switch closed status-- ele(widget_frame) not existed and when open, ele is existed
        self.wifi_settings_btn = "%s:id/widget_frame" % self.android_relatelayout_package
        # wifi list
        self.wifi_view = "%s:id/recycler_view" % self.android_settings_package
        self.single_wifi_box = "android.widget.RelativeLayout"
        self.wifi_name = "%s:id/title" % self.android_relatelayout_package
        # if wifi is connected, "id/summary" would exist
        self.wifi_status = "%s:id/summary" % self.android_relatelayout_package
        self.input_wifi_box = "%s:id/password" % self.android_settings_package
        self.conn_wifi_btn = "%s:id/button1" % self.android_relatelayout_package

    def get_swipe_point(self):
        if self.is_landscape:
            point = self.get_screen_size()
            size = [point[1], point[0]]
        else:
            size = self.get_screen_size()
        x1 = int(size[0]) / 2 + 200
        y1 = int(size[1]) / 2 + 300
        x2 = x1
        y2 = int(size[1]) / 2 - 400
        return [x1, y1, x2, y2]

    def connect_available_wifi(self, wifi_list):
        # open wlan page
        # self.open_wifi_btn()
        # self.time_sleep(2)
        # self.confirm_open_wifi_page()
        # self.confirm_wifi_switch_open()
        # self.time_sleep(5)
        self.connect_settings_wifi(wifi_list)

    def connect_settings_wifi(self, wifi_list):
        # get swipe point, and set the swipe range
        points = self.get_swipe_point()
        x1 = points[0]
        y1 = points[1]
        x2 = points[2]
        y2 = points[3]
        all_wifi_boxes = self.get_element_by_id(self.wifi_view).child(className=self.single_wifi_box)
        # print(all_wifi_boxes)
        device_wifi_list = []
        # find available wifi
        flag = 0
        for i in range(10):
            for box in all_wifi_boxes:
                for ava_wifi in wifi_list:
                    text = '-+'
                    try:
                        text = self.remove_space(box.child(resourceId=self.wifi_name).get_text())
                        # print(text)
                    except Exception as e:
                        pass
                    if self.remove_space(ava_wifi["name"]) in text:
                        if ava_wifi not in device_wifi_list:
                            device_wifi_list.append(ava_wifi)
            print("wifi列表: ", device_wifi_list)
            if len(device_wifi_list) == 0:
                # 滑动屏幕
                if i <= 5:
                    self.swipe_screen(x1, y1, x2, y2)
                    continue
                else:
                    self.swipe_screen(x1, y2, x2, y1)
                    continue

            if self.ele_text_is_existed(device_wifi_list[0]["name"], time_to_wait=3):
                print(device_wifi_list[0]["name"])
                wifi_ele = self.get_element_by_text(device_wifi_list[0]["name"])
                wifi_ele.click()
                now_time = self.get_current_time()
                while True:
                    if self.ele_id_is_existed_USB(self.input_wifi_box):
                        break
                    if self.get_current_time() > self.return_end_time(now_time):
                        assert False, "@@@@无法打开 %s wifi密码框， 请检查！！！！" % device_wifi_list[0]["name"]
                    wifi_ele.click()
                    self.time_sleep(1)

            input_psw_box = self.get_element_by_id(self.input_wifi_box)
            connect_btn = self.get_element_by_id(self.conn_wifi_btn)
            now_time = self.get_current_time()
            while True:
                try:
                    self.press_back()
                    self.input_element_text(input_psw_box, device_wifi_list[0]["password"])
                except Exception as e:
                    print(e)
                    device_wifi_list = []
                    self.swipe_screen(x1, y1, x2, y2)
                    break
                self.time_sleep(2)
                self.press_enter()
                # connect_btn.click()
                if not self.ele_id_is_existed_USB(self.input_wifi_box):
                    flag += 1
                    break
                if self.get_current_time() > self.return_end_time(now_time):
                    assert False, "@@@@无法打开 %s wifi， 请检查！！！！" % device_wifi_list[0]["name"]

            if flag == 1:
                break

        if len(device_wifi_list) == 0:
            assert False, "@@@没连接上wifi, 请检擦！！！！"

    def confirm_open_wifi_page(self):
        now_time = self.get_current_time()
        while True:
            log.info("am start -a android.settings.WIFI_SETTINGS")
            self.u2_send_command("am start -a android.settings.WIFI_SETTINGS")
            switch_btn = self.ele_id_is_existed_USB(self.wifi_switch_btn, timeout=5)
            # print(switch_btn)
            # switch_btn = 1
            if switch_btn:
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@无法打开wifi 页面， 请检查！！！"

    def confirm_wifi_switch_open(self):
        now_time = self.get_current_time()
        switch_btn = self.get_element_by_id(self.wifi_switch_btn)
        while True:
            settings_btn = self.ele_id_is_existed_USB(self.wifi_settings_btn, timeout=10)
            if settings_btn:
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@无法打开wifi 页面， 请检查！！！"
            switch_btn.click()
            try:
                self.wait_ele_presence_by_id(self.wifi_settings_btn, time_to_wait=15)
            except Exception:
                pass

    def input_tpui_password(self, psw_text):
        if self.wait_ele_presence_by_id(self.tpui_main, 10):
            # click more btn
            eles = self.get_element_by_id(self.tpui_main).child(className=self.more_btn)
            eles[1].click()
            now_time = self.get_current_time()
            while True:
                if self.wait_ele_presence_by_id(self.psw_box, 5):
                    break
                eles[1].click()
                self.time_sleep(1)
                if self.get_current_time() > self.return_end_time(now_time, 120):
                    assert False, "@@@无法掉出密码窗口， 请检查！！！！"
            psw_box_ele = self.get_element_by_id(self.psw_box)
            self.input_element_text(psw_box_ele, psw_text)
            confirm_btn = self.get_element_by_id(self.tpui_psw_confirm)
            confirm_btn.click()
            self.time_sleep(1)
            while True:
                if self.wait_ele_gone_by_id(self.psw_box, 5):
                    break
                confirm_btn.click()
                self.time_sleep(1)
                if self.get_current_time() > self.return_end_time(now_time, 60):
                    assert False, "@@@无法确认提交密码， 请检查！！！！"
        else:
            assert False, "@@@@tpui主页无法打开，请检查！！！"

    def get_aimdm_mobile_data(self):
        points = self.get_swipe_point()
        x1 = points[0]
        y1 = points[1]
        x2 = points[2]
        y2 = points[3]
        try:
            self.open_app_detail_info_page_USB(self.aimdm_package)
        except AssertionError:
            if self.ele_id_is_existed_USB(self.settings_title):
                title_text = self.get_element_text_USB(self.get_element_by_id_USB(self.settings_title))
                if self.remove_space_and_upper(title_text) == "AIMDM":
                    pass
                else:
                    assert False, "@@@@无法打开aimdm的app info 页面， 请检查！！！！"
        print(self.get_element_text_USB(self.get_element_by_id_USB(self.settings_title)))
        for i in range(5):
            btn = self.ele_text_is_existed(self.data_used_title, 5)
            if btn:
                break
            if i < 2:
                self.swipe_screen(x1, y1, x2, y2)
            else:
                self.swipe_screen(x1, y2, x2, y1)

        # pre_mobile_wifi_data_btn = self.get_element_by_id_USB(self.container).child(className=self.layout)[5]
        # go to mobile data used detail page
        pre_mobile_wifi_data_btn = self.get_element_by_text(self.data_used_title)
        pre_mobile_wifi_data_btn.click()
        self.confirm_ele_is_existed_USB(pre_mobile_wifi_data_btn, self.spinner)
        self.time_sleep(6)
        # get total used detail and return
        return self.get_total_data_text()

    def get_total_data_text(self):
        # get total used detail
        mobile_data_used = self.get_element_text_USB(self.get_element_by_id_USB(self.total_data_summary))
        return mobile_data_used

    def get_mobile_data_size(self):
        data_used_info = self.remove_space_and_upper(self.get_total_data_text())
        if "KB" in data_used_info:
            return "kB"
        elif "MB" in data_used_info:
            return "MB"

    def click_cleat_recent_app_btn_USB(self, id_no):
        recent_app = self.get_current_app_USB()
        now_time = self.get_current_time()
        while True:
            try:
                if int(self.get_android_version()) >= 13:
                    if self.ele_id_is_existed_USB(recent_app + self.clear_all_android13):
                        clear_btn = self.get_element_by_id_USB(recent_app + self.clear_all_android13)
                        clear_btn.click()
                        if self.wait_ele_gone_by_id_USB(recent_app + self.clear_all_android13, 5):
                            return True
                    if self.ele_id_is_existed_USB(recent_app + self.recent_panel):
                        panels = self.get_element_by_id_USB(recent_app + self.recent_panel)
                        size = self.get_screen_size()
                        size = [int(size[0]), int(size[1])]

                        for i in range(len(panels)):
                            if self.is_landscape:
                                self.swipe_screen(size[1] / 2, size[0] / 2, size[1], size[0] / 2)
                            else:
                                self.swipe_screen(size[0] / 2, size[1] / 2, size[0], size[1] / 2)
                    else:
                        break
                else:
                    if self.wait_ele_presence_by_id_USB(recent_app + id_no, 5):
                        self.click_element_USB(self.get_element_by_id_USB(recent_app + id_no))
                        if self.wait_ele_gone_by_id_USB(recent_app + id_no, 5):
                            return True
                if self.get_current_time() > self.return_end_time(now_time, 60):
                    assert False, "@@@@无法清除最近应用， 请检查！！！！"
                self.time_sleep(1)
            except AssertionError as e:
                print(e)
                break

    def open_recent_page_USB(self):
        self.back_to_home_USB()
        first_app = self.get_current_app_USB()
        now_time = self.get_current_time()
        while True:
            self.u2_send_command_USB("input keyevent KEYCODE_APP_SWITCH")
            self.time_sleep(2)
            if int(self.get_android_version()) >= 13:
                if self.wait_ele_presence_by_id(self.get_current_app() + self.over_view_panel, 5):
                    break
            else:
                next_app = self.get_current_app_USB()
                if first_app != next_app:
                    break
            if self.get_current_time() > self.return_end_time(now_time, 60):
                assert False, "@@@无法打开最近应用页面， 请检查！！！！"

    def clear_recent_app_USB(self):
        self.open_recent_page_USB()
        self.click_cleat_recent_app_btn_USB(self.clear_all)

    def manual_unlock(self):
        self.time_sleep(3)
        ele_lock = self.get_element_by_id(self.msg_confirm_id)
        x, y = ele_lock.center()
        print(ele_lock.get_text())

        try:
            for i in range(6):
                self.client.long_click(x, y, duration=0.2)
                # self.click_element(ele_lock)
                # self.time_sleep(0.3)
                # print(i)
        except Exception as e:
            print(e)

    def confirm_system_app_uninstalled(self):
        apk_file = public_pack.yaml_data['app_info']['low_version_app']
        # self.wifi_adb_root(self.device_ip)
        # self.rm_file("system/app/%s" % apk_file)
        # self.reboot_device_root(self.device_ip)
        now_time = self.get_current_time()
        while True:
            # self.wifi_adb_root(self.device_ip)
            # self.open_root_auth_usb()
            self.open_root_auth_usb()
            self.rm_file("system/app/%s" % apk_file)
            package_name = self.get_apk_package_name(self.get_apk_path(apk_file))
            if not self.app_is_installed(package_name):
                break
            self.reboot_device(self.device_ip)
            self.uninstall_app(package_name)
            if self.get_current_time() > self.return_end_time(now_time, 900):
                assert False, "@@@@system app--%s:%s仍然存在， 请检查！！！！" % (apk_file, package_name)

    def check_firmware_version(self):
        return self.u2_send_command("getprop ro.product.version")

    def confirm_received_alert(self, exp_tips):
        # self.mdm_msg_alert_show()
        self.confirm_alert_show()
        self.confirm_received_text(exp_tips)
        self.click_msg_confirm_btn()
        self.confirm_msg_alert_fade(exp_tips)

    def confirm_received_text(self, exp, timeout=60):
        now_time = self.get_current_time()
        while True:
            exp_text = self.upper_transfer(self.remove_space(exp))
            act_text = self.upper_transfer(self.remove_space(self.get_msg_tips_text()))
            print(exp_text)
            print(act_text)
            if exp_text == act_text:
                break
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                assert exp_text == act_text, "@@@1分钟内检测到预期的提示信息和实际提示信息不一样， 请检查！！！！"
            self.time_sleep(1)

    def clear_download_and_upgrade_alert(self):
        tips = []
        lock_tips = self.remove_space_and_upper("pls contact the administrator to unlock it!")
        download_tips = self.remove_space_and_upper("Foundanewfirmware,whethertoupgrade?")
        upgrade_tips = self.remove_space_and_upper("whethertoupgradenow?")
        tips.append(lock_tips)
        tips.append(download_tips)
        tips.append(upgrade_tips)
        if self.msg_alert_is_existed():
            current_tip = self.remove_space_and_upper(self.get_msg_tips_text())
            if download_tips in current_tip:
                self.click_cancel_btn()
            if upgrade_tips in current_tip:
                self.click_cancel_btn()

    def confirm_wifi_btn_open(self, timeout=60):
        now = self.get_current_time()
        while True:
            if self.open_wifi_btn():
                break
            if self.get_current_time() > self.return_end_time(now, timeout):
                assert False, "@@@@1分钟内无法打开wifi开关， 请检查!!!!"
            self.time_sleep(1)

    def confirm_wifi_btn_close(self, timeout=60):
        now = self.get_current_time()
        while True:
            if self.close_wifi_btn():
                break
            if self.get_current_time() > self.return_end_time(now, timeout):
                assert False, "@@@@1分钟内无法关闭wifi开关， 请检查!!!!"
            self.time_sleep(1)

    def get_aimdm_logs_list_discard(self):
        cmd = "ls /%s/aimdm/log" % self.get_internal_storage_directory()
        files = self.u2_send_command(cmd)
        files_list = files.split("\n")
        return files_list

    def get_aimdm_logs_list(self):
        cmd = "ls /%s/aimdm/log" % self.get_internal_storage_directory()
        files = self.u2_send_command(cmd)
        files_list = files.split("\n")
        if len(files_list) == 0:
            return []
        return files_list

    def get_logs_txt(self, send_time):
        """
        TPS900+unknown+V1.1.16+20230830.093927_2023_9_21_9_18_16+radio.txt
        TPS900+unknown+V1.1.16+20230830.093927_2023_9_21_9_18_16+main.txt
        """
        logs_list = self.get_aimdm_logs_list()
        generate_list = []
        if len(logs_list) == 0:
            return []
        else:
            logs = logs_list[:-1]
            for log in logs:
                # 20230830.093927_2023_9_21_9_33_7
                log_time = log.split("+")[-2]
                # ['20230830.093927', '2023', '9', '21', '9', '18', '16']
                time_list = self.extract_integers(log_time)
                generate_time = self.format_time(time_list[1:])
                if self.compare_time(send_time, generate_time):
                    generate_list.append(log)
            return generate_list

    def pull_logs_file(self, logs):
        # conf.project_path + "\\Report\\environment.properties"
        internal = self.get_internal_storage_directory()
        des = config.project_path + "\\CatchLogs"
        for txt in logs:
            cmd = "pull /%s/aimdm/log/%s %s" % (internal, txt, des)
            try:
                res = self.send_adb_command(cmd)
                print(res)
            except Exception:
                res = self.send_adb_command(cmd)
                print(res)

    def generate_and_upload_log(self, send_time, file_name):
        logs = self.get_logs_txt(send_time)
        self.pull_logs_file(logs)
        for lo in logs:
            file_path = config.project_path + "\\CatchLogs\\" + lo
            if not self.path_is_existed(file_path):
                assert False, "@@@@无%s文件， 请检查！！！" % lo
            upload_name = file_name + lo
            public_pack.allure.attach.file(file_path, name=upload_name,
                                           attachment_type=public_pack.allure.attachment_type.TEXT)

    def upload_log(self, file, name):
        public_pack.allure.attach(file, name=name, attachment_type=public_pack.allure.attachment_type.TEXT)

    def upload_image_JPG(self, file_path, new_name):
        # print(file_path)
        # public_pack.allure.attach(file_path, name=new_name, attachment_type=public_pack.allure.attachment_type.JPG)
        with open(file_path, 'rb') as image_file:
            public_pack.allure.attach(image_file.read(), name=new_name,
                                      attachment_type=public_pack.allure.attachment_type.JPG)

    def lock_psw_box_presence(self, time_to_wait=3):
        self.wait_ele_presence_by_id(self.lock_psw_id, time_to_wait)

    def lock_psw_input(self, text):
        ele = self.get_element_by_id(self.lock_psw_id)
        self.input_element_text(ele, text)

    def click_psw_confirm_btn(self):
        ele = self.get_element_by_id(self.psw_confirm_id)
        self.click_element(ele)

    def confirm_psw_alert_fade(self, timeout=0):
        now_time = self.get_current_time()
        while True:
            if self.wait_ele_gone_by_id(self.psw_confirm_id, 3):
                return True
            else:
                ele = self.get_element_by_id(self.psw_confirm_id)
                self.click_element(ele)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                return False
            self.time_sleep(1)

    def get_msg_tips_text(self):
        ele = self.get_element_by_id(self.msg_tips_id)
        return self.remove_space(self.get_element_text(ele))

    def get_msg_header_text(self):
        ele = self.get_element_by_id(self.msg_alert_id).child(className=self.msg_header_id)
        return self.remove_space(self.get_element_text(ele))

    def click_msg_confirm_btn(self):
        ele = self.get_element_by_id(self.msg_confirm_id)
        self.click_element(ele)

    def click_cancel_btn(self):
        ele = self.get_element_by_id(self.msg_cancel_id)
        self.click_element(ele)

    def mdm_msg_alert_show(self, time_out=5):
        now_time = self.get_current_time()
        while True:
            ele = self.wait_ele_presence_by_id(self.msg_alert_id, time_out)
            if ele:
                return True
            if self.get_current_time() > self.return_end_time(now_time):
                return False

    def msg_alert_is_existed(self):
        flag = self.wait_ele_presence_by_id(self.msg_alert_id, 5)
        return flag

    def confirm_alert_show(self, timeout=120):
        now_time = self.get_current_time()
        while True:
            if self.mdm_msg_alert_show():
                break
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@%d内还没弹出弹框， 请检查！！！！" % timeout
            self.time_sleep(1)

    def public_alert_show(self, timeout=60):
        now_time = self.get_current_time()
        while True:
            ele = self.wait_ele_presence_by_id(self.msg_alert_id, timeout)
            print(ele)
            if ele:
                return True
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                return False
            self.time_sleep(1)

    def mdm_msg_alert_show_discard(self, time_out=5):
        now_time = self.get_current_time()
        if not self.wait_alert_appear(self.msg_alert_id, time_out):
            assert False

    def confirm_msg_alert_fade(self, text, timeout=0):
        now_time = self.get_current_time()
        while True:
            ele = self.wait_ele_gone_by_id(self.msg_alert_id, timeout)
            if ele:
                return True
            else:
                # deal with different alert
                if self.get_msg_tips_text() not in self.remove_space(text):
                    return True
                ele = self.get_element_by_id(self.msg_confirm_id)
                self.click_element(ele)
            if self.get_current_time() > self.return_end_time(now_time, timeout):
                return False
            self.time_sleep(1)
