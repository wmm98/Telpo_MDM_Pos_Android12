import Page as public_pack
from Page.Telpo_MDM_Page import TelpoMDMPage

conf = public_pack.Config()
By = public_pack.By
t_time = public_pack.t_time
EC = public_pack.EC


class DevicesPage(TelpoMDMPage):
    def __init__(self, driver, times):
        TelpoMDMPage.__init__(self, driver, times)
        self.driver = driver

    # Devices_list btn  --new add for test version
    loc_devices_list_btn = (By.LINK_TEXT, "Devices List")

    loc_category_btn = (By.LINK_TEXT, "Create New Category")
    loc_input_cate_box = (By.ID, "category_name")
    loc_save_btn_cate = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_category_button']")
    loc_close_btn_cate = (By.XPATH, "//*[@id=\"modal-add-category\"]/div/div/div[3]/button[1]")

    loc_mode_btn = (By.LINK_TEXT, "Create New Model")
    loc_input_mode_box = (By.ID, "model_name")
    loc_save_btn_mode = (By.CSS_SELECTOR, "[class = 'btn btn-primary create_model_button']")
    loc_close_btn_mode = (By.XPATH, "//*[@id=\"modal-add-model\"]/div/div/div[3]/button[1]")
    loc_alert_show = (By.CSS_SELECTOR, "[class = 'modal fade show']")

    # 提示框
    loc_cate_name_existed = (By.ID, "swal2-title")
    loc_mode_name_success = (By.ID, "swal2-title")

    # Model盒子,model list
    loc_models_box = (By.CSS_SELECTOR, "[class = 'modelSelectd model_list']")

    # 种类text
    loc_cate_box = (By.CLASS_NAME, "category_list")

    # New device btn relate
    loc_new_btn = (By.CSS_SELECTOR, "[class = 'fas fa-plus-square text-black']")
    loc_input_dev_name = (By.ID, "device_name")
    loc_input_dev_SN = (By.ID, "device_sn")
    loc_select_dev_cate = (By.ID, "Category")
    loc_select_dev_mode = (By.ID, "Model")
    loc_save_dev_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_create_device_button']")
    loc_close_dev_btn = (By.XPATH, "//*[@id=\"modal-add-device\"]/div/div/div[3]/button[1]")
    loc_add_device_success_warning = (By.ID, "modal-warning-device-model")
    # 设备列表
    loc_devices_list = (By.ID, "device_list")
    loc_label = (By.TAG_NAME, "label")
    loc_tr = (By.TAG_NAME, "tr")
    loc_td = (By.CLASS_NAME, "text-center")

    # check box
    loc_check_all = (By.ID, "checkall")

    # Import btn relate; import devices
    loc_import_btn = (By.CSS_SELECTOR, "[class = 'fas fa-file-upload batch_upload_device']")
    loc_download_template_btn = (By.LINK_TEXT, "Download Template Here")
    loc_choose_file_btn = (By.ID, "file")
    loc_import_cate_btn = (By.ID, "import_Category")
    loc_import_model_btn = (By.ID, "import_Model")
    loc_import_company_btn = (By.ID, "import_subcompany")
    loc_import_save_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_import_device_button']")
    # just for find the close-btn
    loc_import_devices_box = (By.ID, "modal-import-device")
    loc_import_close_btn = (By.CSS_SELECTOR, "[class = 'btn btn-default']")
    file_path = conf.project_path + "\\Param\\device import.xlsx"

    # send message
    loc_msg_btn = (By.CSS_SELECTOR, "[class = 'fas fa-envelope batch_message']")
    loc_msg_input_box = (By.ID, "device_notification")
    loc_msg_input_send_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_send_device_message']")
    loc_msg_input_close_btn_large = (By.ID, "modal-device-message")  # just for serach the exact close btn
    loc_msg_input_close_btn = (By.CSS_SELECTOR, "[class = 'btn btn-default']")

    # search device(sn)
    loc_search_btn = (By.CSS_SELECTOR, "[class = 'fas fa-search']")
    loc_search_input_box = (By.ID, "search_device_sn")
    loc_search_search_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_search_device_button']")

    # lock and unlock btn  relate
    loc_lock_btn = (By.CSS_SELECTOR, "[class = 'fas fa-lock batch_lock']")
    loc_unlock_btn = (By.CSS_SELECTOR, "[class = 'fas fa-lock-open batch_unlock']")

    # reboot btn relate
    loc_reboot_btn = (By.CSS_SELECTOR, "[class = 'fas fa-retweet batch_reboot']")
    loc_sure_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_batch_reboot']")
    loc_warning = (By.ID, "modal-device-reboot-message")

    # Action button relate
    # shutdown btn
    loc_dropdown_btn = (By.CSS_SELECTOR, "[class = 'btn btn-warning dropdown-toggle dropdown-icon']")
    loc_menu_show = (By.CSS_SELECTOR, "[class = 'dropdown-menu dropdown-menu-right show']")
    loc_shutdown_btn = (By.CSS_SELECTOR, "[class = 'fas fa-power-off']")
    loc_shutdown_sure_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_command_button']")

    # psw btn relate
    loc_psw_btn = (By.CSS_SELECTOR, "[class = 'fas fa-key batch_password']")
    loc_TPUI_password = (By.ID, "device_tpui_password")
    loc_lock_password = (By.ID, "device_password")
    loc_save_psw_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary comfirm_update_device_password']")

    # server relate
    lco_server_btn = (By.CSS_SELECTOR, "[class = 'fas fa-server batch_api']")
    loc_api_box = (By.ID, "new_api")
    loc_api_send_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary sure_update_server_api']")

    # left bar
    loc_left_bar = (By.CLASS_NAME, "col-md-3")

    # cat log btn
    loc_cat_log_btn = (By.CSS_SELECTOR, "[class = 'far fa-file-code']")
    loc_type_box = (By.CLASS_NAME, "select2-search__field")
    loc_log_type_options_box = (By.CSS_SELECTOR, "[class = 'select2-dropdown select2-dropdown--below']")
    loc_log_types = (By.TAG_NAME, "li")

    loc_save_catch_btn = (By.CSS_SELECTOR, "[class = 'btn btn-primary btn-submit-catch']")
    # log type is selected, title = system log
    loc_type_selected = (By.CLASS_NAME, "select2-selection__choice")
    loc_type_selected_box = (By.CSS_SELECTOR, "[class = 'select2-selection select2-selection--multiple]")

    # Duration
    loc_duration_selector = (By.CSS_SELECTOR, "[class = 'form-control catch_duration']")
    loc_duration_option = (By.TAG_NAME, "option")

    # factory reset
    loc_factory_reset_btn = (By.CSS_SELECTOR, "[class = 'fas fa-eraser']")
    loc_factory_reset_sure_btn = (By.CSS_SELECTOR, "[class = 'btn btn-outline-dark sure_command_button']")

    def show_log_type(self):
        ele = self.get_element(self.loc_type_box)
        ele.click()
        now_time = self.get_current_time()
        while True:
            if self.ele_is_existed(self.loc_log_type_options_box):
                break
            else:
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@@无法选择log类型， 请检查！！！"
            self.time_sleep(1)

    def show_log_type_again(self):
        ele = self.get_element(self.loc_type_box)
        ele.click()
        now_time = self.get_current_time()
        while True:
            if self.ele_is_existed(self.loc_log_type_options_box):
                break
            else:
                ele.click()
            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@@无法选择log类型， 请检查！！！"
            self.time_sleep(1)

    def select_app_log(self):
        app_log = self.get_element(self.loc_log_type_options_box).find_elements(*self.loc_log_types)[0]
        app_text = app_log.text
        print(app_text)
        app_log.click()
        all_text = ''
        while True:
            flag = 0
            if self.ele_is_existed(self.loc_type_selected):
                eles = self.get_elements(self.loc_type_selected)
                for e in eles:
                    all_text += self.remove_space(self.upper_transfer(e.text))
                    print(all_text)
                    selected_text = self.remove_space(self.upper_transfer(app_text))
                    if selected_text in all_text:
                        flag += 1
                        break
                if flag == 1:
                    break
            else:
                app_log.click()
            self.time_sleep(1)

    def get_catch_log_duration_list(self):
        select_box = self.get_element(self.loc_duration_selector)
        select_options = select_box.find_elements(*self.loc_duration_option)
        values = [option.get_attribute("value") for option in select_options]
        return values

    def select_system_log(self):
        app_log = self.get_element(self.loc_log_type_options_box).find_elements(*self.loc_log_types)[1]
        app_text = app_log.text
        print(app_text)
        app_log.click()
        all_text = ''
        while True:
            flag = 0
            if self.ele_is_existed(self.loc_type_selected):
                eles = self.get_elements(self.loc_type_selected)
                for e in eles:
                    all_text += self.remove_space(self.upper_transfer(e.text))
                    print(all_text)
                    selected_text = self.remove_space(self.upper_transfer(app_text))
                    if selected_text in all_text:
                        flag += 1
                        print("已经选中了application log")
                        break
                if flag == 1:
                    break
            else:
                app_log.click()
            self.time_sleep(1)

    def select_log_duration(self, minutes):
        flag = 0
        for m in self.get_catch_log_duration_list():
            if m == str(minutes):
                flag += 1
                self.select_by_value(self.loc_duration_selector, m)
                break
        assert flag == 1, "@@@@传入的log 捕捉时长不对， 请检查！！！！！"

    def click_cat_log(self):
        self.click(self.loc_cat_log_btn)
        self.confirm_alert_existed(self.loc_cat_log_btn)

    def click_save_catch_log(self):
        self.click(self.loc_save_catch_btn)
        self.confirm_tips_alert_show(self.loc_save_catch_btn)
        self.refresh_page()

    def click_save_catch_log_fail(self):
        for i in range(5):
            self.click(self.loc_save_catch_btn)
            self.confirm_tips_alert_show(self.loc_save_catch_btn)
            self.alert_show()
            self.time_sleep(2)

    def catch_all_log(self, minutes):
        self.click_cat_log()
        self.show_log_type()
        self.select_app_log()
        self.show_log_type_again()
        self.select_system_log()
        self.select_log_duration(minutes)
        self.click_save_catch_log()

    def click_shutdown_btn(self):
        self.click(self.loc_shutdown_btn)
        self.confirm_alert_existed(self.loc_shutdown_btn)
        self.click(self.loc_shutdown_sure_btn)
        self.confirm_tips_alert_show(self.loc_shutdown_sure_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_shutdown_sure_btn)

    def factory_reset(self):
        self.click_dropdown_btn()
        self.click(self.loc_factory_reset_btn)
        self.confirm_alert_existed(self.loc_factory_reset_btn)
        self.click(self.loc_factory_reset_sure_btn)
        self.time_sleep(3)
        self.click(self.loc_factory_reset_sure_btn)
        self.time_sleep(3)
        self.confirm_tips_alert_show(self.loc_factory_reset_sure_btn)
        self.refresh_page()
        # self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_factory_reset_sure_btn)

    def click_server_btn(self):
        self.click(self.lco_server_btn)
        self.confirm_alert_existed(self.lco_server_btn)

    def api_transfer(self, api_url):
        self.input_text(self.loc_api_box, api_url)
        self.time_sleep(5)
        self.click(self.loc_api_send_btn)
        self.confirm_tips_alert_show(self.loc_api_send_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_api_send_btn)

    def click_psw_btn(self):
        self.click(self.loc_psw_btn)
        self.confirm_alert_existed(self.loc_psw_btn)

    def change_TPUI_password(self, psw):
        self.alert_show()
        self.input_text(self.loc_TPUI_password, psw)
        self.click(self.loc_save_psw_btn)
        self.confirm_tips_alert_show(self.loc_save_psw_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_psw_btn)
        # self.alert_fade()

    def change_device_password(self, psw):
        self.alert_show()
        self.input_text(self.loc_lock_password, psw)
        self.click(self.loc_save_psw_btn)
        self.confirm_tips_alert_show(self.loc_save_psw_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_psw_btn)
        # self.alert_fade()

    def click_dropdown_btn(self):
        self.click(self.loc_dropdown_btn)
        now_time = self.get_current_time()
        while True:
            if self.ele_is_existed(self.loc_menu_show):
                break
            else:
                self.click(self.loc_dropdown_btn)

            if self.get_current_time() > self.return_end_time(now_time):
                assert False, "@@@@dropdown 按钮无法打开！！！"
        self.time_sleep(1)
        # self.web_driver_wait_until(EC.presence_of_element_located(self.loc_menu_show), 10)

    # reboot relate
    def click_reboot_btn(self):
        self.click(self.loc_reboot_btn)
        self.confirm_alert_existed(self.loc_sure_btn)
        self.click(self.loc_sure_btn)
        self.click(self.loc_sure_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_sure_btn)

    def get_reboot_warning_alert_text(self, text):
        if text in self.get_element(self.loc_warning).text:
            # print(self.get_element(self.loc_warning).text)
            self.refresh_page()
        else:
            self.click(self.loc_sure_btn)
            self.refresh_page()
        # try:
        #     self.alert_fade()
        # except Exception:
        #     self.refresh_page()

    def click_lock(self):
        try:
            self.click(self.loc_lock_btn)
            self.confirm_tips_alert_show(self.loc_lock_btn)
        except public_pack.StaleElementReferenceException:
            self.click(self.loc_lock_btn)
            self.confirm_tips_alert_show(self.loc_lock_btn)

    def click_unlock(self):
        try:
            self.click(self.loc_unlock_btn)
            self.confirm_tips_alert_show(self.loc_unlock_btn)
        except Exception:
            self.click(self.loc_unlock_btn)
            self.confirm_tips_alert_show(self.loc_unlock_btn)

    def search_device_by_sn(self, sn):
        try:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except public_pack.StaleElementReferenceException:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except public_pack.ElementNotInteractableException:
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)
        except public_pack.TimeoutException:
            self.refresh_page()
            self.click(self.loc_search_btn)
            self.confirm_alert_existed(self.loc_search_btn)
            self.input_text(self.loc_search_input_box, sn)
            self.time_sleep(1)
            self.click(self.loc_search_search_btn)
            self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_search_search_btn)

    def click_send_btn(self):
        self.click(self.loc_msg_btn)
        self.confirm_alert_existed(self.loc_msg_btn)

    def msg_input_and_send(self, msg):
        self.input_text(self.loc_msg_input_box, msg)
        self.click(self.loc_msg_input_send_btn)
        self.confirm_tips_alert_show(self.loc_msg_input_send_btn)
        self.refresh_page()
        # self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_msg_input_send_btn)

    def send_message(self, msg):
        self.click_send_btn()
        self.msg_input_and_send(msg)

    def confirm_msg_alert_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_msg_input_send_btn)

    def click_devices_list_btn(self):
        self.click(self.loc_devices_list_btn)

    def click_import_btn(self):
        self.click(self.loc_import_btn)
        self.confirm_alert_existed(self.loc_import_btn)

    def click_download_template_btn(self):
        # download,
        self.click(self.loc_download_template_btn)
        # need add step check if success to download

    def import_devices_info(self, info):
        self.alert_show()
        if not public_pack.os.path.exists(self.file_path):
            raise FileNotFoundError
        self.input_text(self.loc_choose_file_btn, self.file_path)
        self.select_by_text(self.loc_import_cate_btn, info['cate'])
        self.select_by_text(self.loc_import_model_btn, info['model'])
        self.click(self.loc_import_save_btn)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_import_save_btn)

    def click_new_btn(self):
        self.click(self.loc_new_btn)
        self.confirm_alert_existed(self.loc_new_btn)

    def add_devices_info(self, dev_info, cate_model=True):
        # name
        self.input_text(self.loc_input_dev_name, dev_info['name'])
        # SN
        self.input_text(self.loc_input_dev_SN, dev_info['SN'])
        if cate_model:
            # cate
            self.select_by_text(self.loc_select_dev_cate, dev_info['cate'])
            # model
            self.select_by_text(self.loc_select_dev_mode, dev_info['model'])
        # save
        self.click(self.loc_save_dev_btn)

    def get_add_dev_warning_alert(self):
        flag = 0
        now_time = self.get_current_time()
        while True:
            ele = self.get_element(self.loc_add_device_success_warning)
            print(ele.get_attribute("style"))
            if "block" in ele.get_attribute("style"):
                flag += 1
                break
            if self.get_current_time() > self.return_end_time(now_time, 5):
                break
            self.time_sleep(1)

        now_time1 = self.get_current_time()
        if flag == 0:
            while True:
                if not ("block" in self.get_element(self.loc_add_device_success_warning).get_attribute("style")):
                    self.click(self.loc_save_dev_btn)
                else:
                    break
                if self.get_current_time() > self.return_end_time(now_time1, 5):
                    assert False, "无法添加device, 请检查！！！"
                self.time_sleep(1)

    # another alert would appear when add device successfully, would conflict
    def confirm_add_device_alert_fade_discard(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_dev_btn)

    def close_btn_add_dev_info(self):
        self.click(self.loc_close_dev_btn)
        self.alert_fade()

    # return devices_list
    def get_dev_info_list(self):
        devices_list = []
        is_existed = self.ele_is_existed_in_range(self.loc_devices_list, self.loc_tr)
        if not is_existed:
            is_existed = self.ele_is_existed_in_range(self.loc_devices_list, self.loc_tr)
        if is_existed:
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            for tr_ele in tr_eles:
                td_eles = tr_ele.find_elements(*self.loc_td)[1:8]
                devices_list.append({"Name": td_eles[0].text, "Category": td_eles[2].text, "Model": td_eles[3].text,
                                     "SN": td_eles[4].text, "Status": td_eles[5].text,
                                     "Lock Status": td_eles[6].text})
            return devices_list
        else:
            return []

    # return length of devices_list
    def get_dev_info_length(self):
        try:
            eles = self.get_element(self.loc_devices_list)
            tr_eles = eles.find_elements(*self.loc_tr)
            return len(tr_eles)
        except public_pack.TimeoutException:
            return 0

    def select_all_devices(self):
        ele = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_check_all))
        self.exc_js_click(ele)
        # self.deal_ele_selected(ele)
        return ele

    def select_device(self, device_sn):
        loc = (By.ID, device_sn)
        ele = self.web_driver_wait_until(EC.presence_of_element_located(loc))
        self.exc_js_click(ele)
        self.deal_ele_selected(ele)
        return ele

    def check_ele_is_selected(self, ele):
        self.deal_ele_selected(ele)

    def check_ele_is_not_selected(self, ele):
        self.deal_ele_not_selected(ele)

    def get_devices_list_label_text_discard(self):
        devices = self.get_element(self.loc_devices_list)
        label_eles = devices.find_elements(*self.loc_label)
        text = [label_ele.text for label_ele in label_eles]
        return text

    # check if alert would disappear
    def alert_fade(self):
        self.web_driver_wait_until_not(EC.presence_of_element_located(self.loc_alert_show), 10)

    # check if alert would appear
    def alert_show(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_alert_show), 10)

    # add single device
    def get_models_list(self):
        if self.ele_is_existed(self.loc_models_box):
            eles = self.get_elements(self.loc_models_box)
            models_list = [ele.text for ele in eles]
            # print(models_list)
            return models_list
        else:
            return []

    # get all categories
    def get_categories_list(self):
        if self.ele_is_existed(self.loc_cate_box):
            eles = self.get_elements(self.loc_cate_box)
            cates_list = [ele.text for ele in eles]
            print(cates_list)
            return cates_list
        else:
            return []

    def category_is_existed(self, cate):
        if cate in self.get_categories_list():
            return True
        else:
            return False

    # find cate element
    def find_category(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_category_btn))

    # find model ele
    def find_model(self):
        self.web_driver_wait_until(EC.presence_of_element_located(self.loc_mode_btn))

    # click [Create New Category] btn
    def click_category(self):
        self.click(self.loc_category_btn)
        self.confirm_alert_existed(self.loc_save_btn_cate)

    # add category
    def add_category(self, cate_name):
        self.input_text(self.loc_input_cate_box, cate_name)
        self.click(self.loc_save_btn_cate)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def confirm_add_category_box_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    # click [Create New Model] btn
    def click_model(self):
        self.click(self.loc_mode_btn)
        self.confirm_alert_existed(self.loc_mode_btn)

    # add model
    def add_model(self, model_name):
        self.input_text(self.loc_input_mode_box, model_name)
        self.click(self.loc_save_btn_mode)
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def confirm_add_model_box_fade(self):
        self.comm_confirm_alert_not_existed(self.loc_alert_show, self.loc_save_btn_cate)

    def close_btn_mode(self):
        self.click(self.loc_close_btn_mode)

    def close_btn_cate(self):
        self.click(self.loc_close_btn_cate)

    # get devices Page alert text
    def get_alert_text(self):
        # 1: tip_box is existed, 2:tip_box
        # try:
        #     tips_box = self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed), 5)
        #     text = tips_box.text
        #     return text
        # except TimeoutException:
        #     return False
        return self.web_driver_wait_until(EC.presence_of_element_located(self.loc_cate_name_existed)).text
