import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

By = public_pack.By
EC = public_pack.EC
t_time = public_pack.t_time
log = public_pack.MyLog()
conf = public_pack.Config()


class APPSPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # private app related
    loc_private_app_btn = (By.LINK_TEXT, "Private Apps")
    private_app_main_title = "Private Apps"

    # search relate
    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_search_app_name = (By.ID, "search_app_name")
    loc_search_search = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_app_button']")

    # new apk btn
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square']")
    loc_choose_file = (By.ID, "file")
    loc_choose_category = (By.ID, "Category")
    loc_developer_box = (By.ID, "developer")
    loc_des_box = (By.ID, "desc")
    loc_apk_save_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_create_app_button']")

    # alert show
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")

    # app list relate
    loc_apps_list = (By.ID, "apps_list")
    loc_single_app_box = (
        By.CSS_SELECTOR, "[class = 'col-12 col-sm-6 col-md-4 d-flex align-items-stretch flex-column']")
    loc_app_detail_info = (By.CSS_SELECTOR, "[class = 'small pt-1']")
    # app delete btn
    loc_app_delete_btn = (By.CSS_SELECTOR, "[class = 'btn btn-sm bg-danger']")
    loc_app_confirm_del_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-light deleteapp_button']")
    # app release btn
    loc_app_release_alert = (By.ID, "modal-app-release")
    loc_app_release_btn = (By.CSS_SELECTOR, "[class = 'fas fa-registered']")
    loc_silent_install = (By.ID, "setsilent")
    loc_download_network = (By.ID, "download_network")
    loc_set_kiosk_mode = (By.ID, "setkioskmode")
    loc_set_auto_open = (By.ID, "release_app_autoopen")
    loc_device_selected_box = (By.CLASS_NAME, "label-selected")
    # device list and single device also work in app relate
    loc_device_list = (By.CLASS_NAME, "label-item")
    loc_single_device = (By.TAG_NAME, "li")
    loc_app_package_name = (By.ID, "release_apk_package")
    loc_app_release_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-primary confirm_release']")

    # release version sns box relate
    loc_release_devices_list = (By.ID, "releaseSNS")

    # app release Page
    loc_release_check_all = (By.ID, "checkall")
    loc_release_delete_btn = (By.CSS_SELECTOR, "[class = 'fas fa-trash-alt ']")
    loc_release_confirm_del_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_delete_release']")
    loc_release_list = (By.ID, "releases_list")
    loc_single_release = (By.TAG_NAME, "tr")
    loc_single_release_col = (By.CLASS_NAME, "text-center")

    # app release search btn relate
    loc_release_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_release_package_name = (By.ID, "search_package_name")
    loc_release_sn = (By.ID, "search_device_sn")
    loc_release_version = (By.ID, "version")
    loc_release_search_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_app_release']")
    loc_release_check_box = (By.NAME, "checkbox")
    # send release again
    loc_app_send_release_again = (By.CSS_SELECTOR, "[class = 'btn-witdh btn  btn-sm sync_release']")

    # app upgrade logs relate
    loc_app_upgrade_logs_body = (By.ID, "logs_list")
    loc_app_upgrade_single_log = (By.TAG_NAME, "tr")
    loc_app_upgrade_log_col = (By.TAG_NAME, "td")
    loc_package_name_box = (By.ID, "search_package_name")
    loc_sn_input_box = (By.ID, "search_device_sn")
    loc_upgrade_search_ensure = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_app_release']")

    # app uninstall relate
    loc_uninstall_btn = (By.CSS_SELECTOR, "[class = 'fas fa-eraser']")
    loc_app_uninstall_alert = (By.ID, "modal-appuninstall")

    loc_app_uninstall_confirm = (By.CSS_SELECTOR, "[class = 'btn btn-warning confirm_uninstall']")
    loc_uninstall_device_list = (By.ID, "labelItem1")

    # category
    loc_new_cate_btn = (By.LINK_TEXT, "Create New Category")
    loc_input_cate_box = (By.ID, "category_name")
    loc_save_btn_cate = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_category_button']")
    loc_cate_list = (By.CSS_SELECTOR, "[class = 'todo-list ui-sortable']")
    loc_single_cate = (By.CLASS_NAME, "listactive")

    def search_upgrade_logs(self, package_name, sn):
        self.click(self.loc_search_btn)
        self.confirm_alert_existed(self.loc_search_btn)
        self.input_text(self.loc_package_name_box, package_name)
        self.input_text(self.loc_sn_input_box, sn)
        self.click(self.loc_upgrade_search_ensure)
        self.confirm_alert_not_existed(self.loc_upgrade_search_ensure)

    # add category
    def add_app_category(self, cate_name):
        self.click(self.loc_new_cate_btn)
        self.confirm_alert_existed(self.loc_new_cate_btn)
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)
        self.confirm_tips_alert_show(self.loc_save_btn_cate)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def get_app_categories_list(self):
        if self.ele_is_existed(self.loc_cate_list):
            if self.ele_is_existed(self.loc_cate_list):
                eles = self.get_elements(self.loc_single_cate)
                cates_list = [self.remove_space(ele.text) for ele in eles]
                return cates_list
            else:
                return []
        else:
            return []

    def get_app_latest_upgrade_log(self, send_time, release_info):
        self.time_sleep(5)
        try:
            logs_list = []
            if self.ele_is_existed_in_range(self.loc_app_upgrade_logs_body, self.loc_app_upgrade_single_log):
                upgrade_list = self.get_element(self.loc_app_upgrade_logs_body)
                try:
                    now = self.get_current_time()
                    while True:
                        single_log = upgrade_list.find_elements(*self.loc_app_upgrade_single_log)
                        if len(single_log) > 0:
                            break
                        else:
                            self.refresh_page()
                        if self.get_current_time() > self.return_end_time(now, 15):
                            assert False
                        self.time_sleep(2)
                except Exception:
                    self.refresh_page()

                single_log = upgrade_list.find_elements(*self.loc_app_upgrade_single_log)[0]
                cols = single_log.find_elements(*self.loc_app_upgrade_log_col)
                receive_time_text = cols[3].text
                sn = cols[0].text
                action = cols[4].text
                package = cols[1].text
                version = cols[2].text
                time_line = self.extract_integers(receive_time_text)
                receive_time = self.format_string_time(time_line)
                if self.compare_time(send_time, receive_time):
                    if (release_info["sn"] in sn) and (release_info["package"] in package):
                        if release_info["version"] in version:
                            logs_list.append(
                                {"SN": sn, "Update Time": receive_time, "Action": action, "Version": version})
                return logs_list
            else:
                return []
        except Exception:
            return []

    def get_app_latest_uninstall_log(self, send_time, release_info):
        try:
            logs_list = []
            if self.ele_is_existed_in_range(self.loc_app_upgrade_logs_body, self.loc_app_upgrade_single_log):
                upgrade_list = self.get_element(self.loc_app_upgrade_logs_body)
                single_log = upgrade_list.find_elements(*self.loc_app_upgrade_single_log)[0]
                cols = single_log.find_elements(*self.loc_app_upgrade_log_col)
                receive_time_text = cols[4].text
                sn = cols[1].text
                action = cols[3].text
                package = cols[2].text
                time_line = self.extract_integers(receive_time_text)
                receive_time = self.format_string_time(time_line)
                if self.compare_time(send_time, receive_time):
                    if (release_info["sn"] in sn) and (release_info["package"] in package):
                        logs_list.append({"SN": sn, "Update Time": receive_time, "Action": action})
                return logs_list
            else:
                return []
        except Exception:
            return []

    def select_single_app_release_log(self):
        ele = self.get_element(self.loc_release_check_box)
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)

    def search_app_release_log(self, info):
        self.click(self.loc_release_search_btn)
        self.confirm_alert_existed(self.loc_release_search_btn)
        self.input_text(self.loc_release_package_name, info["package"])
        self.input_text(self.loc_release_sn, info['sn'])
        self.input_text(self.loc_release_version, info["version"])
        self.confirm_alert_not_existed(self.loc_release_search_confirm)

    def click_send_release_again(self):
        self.click(self.loc_app_send_release_again)
        self.confirm_tips_alert_show(self.loc_app_send_release_again)

    def click_uninstall_app_btn(self):
        self.click(self.loc_uninstall_btn)
        self.confirm_alert_existed(self.loc_uninstall_btn)

    def input_uninstall_app_info(self, info):
        uninstall_box = self.get_element(self.loc_app_uninstall_alert)
        devices = uninstall_box.find_element(*self.loc_uninstall_device_list).find_elements(*self.loc_single_device)
        for device in devices:
            if info["sn"] in device.get_attribute("data"):
                if device.get_attribute("class") == "selected":
                    break
                now_time = self.get_current_time()
                while True:
                    if device.get_attribute("class") == "selected":
                        break
                    else:
                        device.click()
                    if self.get_current_time() > self.return_end_time(now_time):
                        assert False, "@@@无法选中device sn, 请检查！！！"
                    self.time_sleep(1)
        self.click(self.loc_app_uninstall_confirm)
        self.confirm_tips_alert_show(self.loc_app_uninstall_confirm)
        self.refresh_page()
        # self.confirm_alert_not_existed(self.loc_app_uninstall_confirm)

    def click_delete_btn(self):
        self.click(self.loc_release_delete_btn)
        self.confirm_alert_existed(self.loc_release_delete_btn)
        self.click(self.loc_release_confirm_del_btn)
        self.confirm_tips_alert_show(self.loc_release_confirm_del_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_release_confirm_del_btn)

    def get_current_app_release_log_total(self):
        release_list = self.get_element(self.loc_release_list)
        is_exited = self.ele_is_existed_in_range(self.loc_release_list, self.loc_single_release)
        if is_exited:
            self.time_sleep(2)
            is_exited = self.ele_is_existed_in_range(self.loc_release_list, self.loc_single_release)
        if is_exited:
            release_count = len(release_list.find_elements(*self.loc_single_release))
            return release_count
        else:
            return 0

    def get_app_latest_release_log_list(self, send_time, release_info, uninstall=False):
        try:
            self.web_driver_wait_until(EC.text_to_be_present_in_element(self.loc_release_list, release_info["package"]))
            release_list = self.get_element(self.loc_release_list)
            logs_list = []
            existed = self.ele_is_existed_in_range(self.loc_release_list, self.loc_single_release)
            if not existed:
                self.time_sleep(2)
                existed = self.ele_is_existed_in_range(self.loc_release_list, self.loc_single_release)
            if not uninstall:
                if existed:
                    logs = release_list.find_elements(*self.loc_single_release)
                    for single_log in logs:
                        cols = single_log.find_elements(*self.loc_single_release_col)
                        receive_time_text = cols[3].text
                        sn = cols[5].text
                        package = cols[1].text
                        version = cols[2].text
                        time_line = self.extract_integers(receive_time_text)
                        receive_time = self.format_string_time(time_line)
                        if self.compare_time(send_time, receive_time):
                            if (release_info["sn"] in sn) and (release_info["package"] in package):
                                # if not release_info["version"]:
                                #     logs_list.append(single_log)
                                if release_info["version"] in version:
                                    logs_list.append(single_log)
                    return logs_list
                else:
                    return []
            elif uninstall:
                if existed:
                    logs = release_list.find_elements(*self.loc_single_release)
                    for single_log in logs:
                        cols = single_log.find_elements(*self.loc_single_release_col)
                        receive_time_text = cols[3].text
                        sn = cols[2].text
                        package = cols[1].text
                        time_line = self.extract_integers(receive_time_text)
                        receive_time = self.format_string_time(time_line)
                        if self.compare_time(send_time, receive_time):
                            if (release_info["sn"] in sn) and (release_info["package"] in package):
                                logs_list.append(single_log)
                    return logs_list
                else:
                    return []
        except Exception:
            return []

    def click_select_all_box(self):
        ele = self.get_element(self.loc_release_check_all)
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)

    def check_release_log_info_discard(self, send_time, device):
        now_time = self.get_current_time()
        while True:
            if len(self.get_app_latest_release_log_list(send_time, device)) != 1:
                break
            else:
                self.refresh_page()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@没有相应的 app release log， 请检查！！！"
            self.time_sleep(1)
        #
        # text = self.get_element(self.loc_release_list).find_element(*self.loc_single_release).text
        # if not info["package"] in text and (info["silent"] in text) and (info["version"] in text):
        #     assert False, "@@@@release app的log有误， 请检查！！！"

    def delete_app_install_and_uninstall_logs(self):
        self.go_to_new_address("apps/appUninstall")
        self.delete_all_app_release_log()
        self.go_to_new_address("apps/releases")
        self.delete_all_app_release_log()

    def delete_all_app_release_log(self):
        try:
            if self.get_current_app_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_btn()
                self.refresh_page()
        except Exception:
            self.refresh_page()
            if self.get_current_app_release_log_total() != 0:
                self.click_select_all_box()
                self.click_delete_btn()
                self.refresh_page()

    def click_release_app_btn(self):
        self.click(self.loc_app_release_btn)
        self.confirm_alert_existed(self.loc_app_release_btn)

    def input_release_app_info(self, info, kiosk_mode=False):
        self.time_sleep(3)
        release_box = self.get_element(self.loc_app_release_alert)
        if kiosk_mode:
            self.select_by_text(self.loc_set_kiosk_mode, "YES")
        else:
            self.select_by_text(self.loc_set_kiosk_mode, "NO")
        if info.get("auto_open"):
            if info["auto_open"] == "YES":
                self.select_by_text(self.loc_set_auto_open, "YES")
        self.select_by_text(self.loc_silent_install, info["silent"].upper())
        self.select_by_text(self.loc_download_network, info["download_network"])
        if "test" not in self.get_current_window_url():
            if isinstance(info["sn"], list):
                self.input_text(self.loc_release_devices_list, "|".join(info["sn"]))
            else:
                self.input_text(self.loc_release_devices_list, info["sn"])
        else:
            devices = release_box.find_element(*self.loc_device_list).find_elements(*self.loc_single_device)
            if isinstance(info["sn"], list):
                for sn in info["sn"]:
                    for device in devices:
                        if sn in device.get_attribute("data"):
                            if device.get_attribute("class") == "selected":
                                break
                            self.confirm_sn_is_selected(device)
            else:
                for device in devices:
                    if info["sn"] in device.get_attribute("data"):
                        if device.get_attribute("class") == "selected":
                            break
                        self.confirm_sn_is_selected(device)
        self.click(self.loc_app_release_confirm)
        self.confirm_tips_alert_show(self.loc_app_release_confirm)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_app_release_confirm)

    def click_delete_app_btn(self):
        self.click(self.loc_app_delete_btn)
        self.confirm_alert_existed(self.loc_app_delete_btn)
        self.click(self.loc_app_confirm_del_btn)
        self.confirm_tips_alert_show(self.loc_app_confirm_del_btn)
        self.confirm_alert_not_existed(self.loc_app_confirm_del_btn)

    def get_apps_text_list(self):
        if self.ele_is_existed(self.loc_single_app_box):
            boxes = self.get_elements(self.loc_single_app_box)
            return [box.text for box in boxes]
        else:
            return []

    def get_app_size(self):
        boxes = self.get_elements(self.loc_app_detail_info)
        size = self.extract_integers(boxes[1].text)
        return size

    def search_app_by_name(self, app_name):
        try:
            self.time_sleep(5)
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_app_name, app_name)
            self.time_sleep(1)
            self.click(self.loc_search_search)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search)
        except Exception:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_app_name, app_name)
            self.time_sleep(1)
            self.click(self.loc_search_search)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search)

    def click_private_app_btn(self):
        self.click(self.loc_private_app_btn)
        now_time = self.get_current_time()
        while True:
            if self.private_app_main_title in self.get_loc_main_title():
                break
            else:
                self.click(self.loc_private_app_btn)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@打开private app Page 出错！！！"
            self.time_sleep(1)

    def click_add_btn(self):
        self.click(self.loc_new_btn)
        self.confirm_alert_existed(self.loc_new_btn)

    def input_app_info(self, file):
        self.input_text(self.loc_choose_file, file)
        # self.select_by_text(self.loc_choose_category,"file_category")
        self.input_text(self.loc_developer_box, "test_engineer")
        self.input_text(self.loc_des_box, "just for automation test")
        self.time_sleep(1)
        self.click(self.loc_apk_save_btn)
        self.confirm_tips_alert_show(self.loc_apk_save_btn, timeout=300)
        self.time_sleep(2)
        self.refresh_page()
        # self.confirm_alert_existed(self.loc_apk_save_btn)
        # self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_apk_save_btn)

    def check_add_app_save_btn(self):
        self.confirm_alert_not_existed(self.loc_apk_save_btn)

    def alert_fade(self):
        try:
            self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 10)
            return True
        except public_pack.TimeoutException:
            return False

        # check if alert would appear

    def alert_show(self):
        try:
            self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 10)
            return True
        except public_pack.TimeoutException:
            return False

    def get_alert_text(self):
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text

    def confirm_alert_not_existed(self, loc, ex_js=0):
        now_time = self.get_current_time()
        while True:
            if self.alert_fade():
                break
            else:
                if ex_js == 1:
                    self.exc_js_click_loc(loc)
                else:
                    self.click(loc)
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@弹窗无法关闭 出错， 请检查！！！"
            self.time_sleep(1)
