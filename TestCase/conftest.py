"""

# @allure.feature # 用于定义被测试的功能，被测产品的需求点
# @allure.story # 用于定义被测功能的用户场景，即子功能点
# @allure.severity #用于定义用例优先级
# @allure.issue #用于定义问题表识，关联标识已有的问题，可为一个url链接地址
# @allure.testcase #用于用例标识，关联标识用例，可为一个url链接地址

# @allure.attach # 用于向测试报告中输入一些附加的信息，通常是一些测试数据信息
# @pytest.allure.step # 用于将一些通用的函数作为测试步骤输出到报告，调用此函数的地方会向报告中输出步骤
# allure.environment(environment=env) #用于定义environment

"""
import pytest
import TestCase

driver = TestCase.test_driver
device_page = TestCase.DevicesPage(driver, 40)
ota_page = TestCase.OTAPage(driver, 40)
app_page = TestCase.APPSPage(driver, 40)
content_page = TestCase.ContentPage(driver, 40)
android_page = TestCase.AndroidAimdmPage(TestCase.device_data, 30)
wifi_ip = TestCase.device_data["wifi_device_info"]["ip"]
serial = TestCase.Serial()
user_info = TestCase.user_info
conf = TestCase.Config()


@pytest.fixture()
def uninstall_big_size_app():
    apk_path = conf.project_path + '\\Public_Package\\APK\\APK_test_pressure.apk'
    apk_package_name = app_page.get_apk_package_name(apk_path)
    if android_page.app_is_installed(apk_package_name):
        android_page.uninstall_app(apk_package_name)
    yield
    if android_page.app_is_installed(apk_package_name):
        android_page.uninstall_app(apk_package_name)


@pytest.fixture()
def Big_APk_operation():
    apk_name = 'APK_test_pressure.apk'
    apk_path = conf.project_path + '\\Public_Package\\APK\\APK_test_pressure.apk'
    ota_page.go_to_new_address("apps")
    now_time = app_page.get_current_time()
    while True:
        try:
            app_page.search_app_by_name(apk_name)
            if len(app_page.get_apps_text_list()) == 0:
                app_page.click_add_btn()
                app_page.input_app_info(apk_path, timeout=600)
            else:
                break
        except:
            pass
        if ota_page.get_current_time() > ota_page.return_end_time(now_time, 1800):
            assert False, "@@@@无法上传apk包：%s, 请检查！！！！" % apk_name
        ota_page.refresh_page()
        ota_page.time_sleep(3)


@pytest.fixture()
def fake_ota_package_operation():
    ota_name = TestCase.yaml_data["ota_packages_info"]["package_name"]
    src = conf.project_path + '\\Public_Package\\origin\\test.zip'
    des = conf.project_path + '\\Public_Package\\new\\test.zip'
    rename_file = conf.project_path + '\\Public_Package\\new\\%s' % ota_name
    ota_page.copy_file(src, des)
    ota_page.rename_file_name(des, rename_file)
    ota_page.go_to_new_address("ota")
    del_time = ota_page.get_current_time()
    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                break
            ota_page.delete_ota_package()
        except:
            pass
            ota_page.refresh_page()
            ota_page.time_sleep(2)
            if ota_page.get_current_time() > ota_page.return_end_time(del_time, 900):
                assert False, "@@@@平台无法删除ota包：%s, 请检查！！！！" % ota_name

    ota_page.refresh_page()
    ota_page.time_sleep(2)
    now_time = ota_page.get_current_time()

    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                ota_page.click_add_btn()
                ota_page.input_ota_package_info({"file_name": rename_file})
                ota_page.click_save_add_ota_pack(timeout=1800)
                ota_page.refresh_page()
                ota_page.time_sleep(1)
            else:
                break
        except:
            pass
        if ota_page.get_current_time() > ota_page.return_end_time(now_time, 3600):
            assert False, "@@@@无法上传ota包：%s, 请检查！！！！" % rename_file
        ota_page.refresh_page()
        ota_page.time_sleep(3)
    yield
    ota_page.delete_file(rename_file)
    ota_page.go_to_new_address("ota")
    del_time = ota_page.get_current_time()
    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                break
            ota_page.delete_ota_package()
        except:
            pass
            ota_page.refresh_page()
            ota_page.time_sleep(2)
            if ota_page.get_current_time() > ota_page.return_end_time(del_time, 900):
                assert False, "@@@@平台无法删除ota包：%s, 请检查！！！！" % ota_name


@pytest.fixture()
def real_ota_package_operation():
    ota_name = TestCase.yaml_data["ota_packages_info"]["package_name"]
    ota_path = ota_page.get_apk_path(ota_name)
    ota_page.go_to_new_address("ota")
    del_time = ota_page.get_current_time()
    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                break
            ota_page.delete_ota_package()
        except:
            pass
            ota_page.refresh_page()
            ota_page.time_sleep(2)
            if ota_page.get_current_time() > ota_page.return_end_time(del_time, 900):
                assert False, "@@@@平台无法删除ota包：%s, 请检查！！！！" % ota_name

    ota_page.refresh_page()
    ota_page.time_sleep(2)
    now_time = ota_page.get_current_time()
    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                ota_page.click_add_btn()
                ota_page.input_ota_package_info({"file_name": ota_path})
                ota_page.click_save_add_ota_pack(timeout=1800)
                ota_page.refresh_page()
                ota_page.time_sleep(1)
            else:
                break
        except:
            pass
        if ota_page.get_current_time() > ota_page.return_end_time(now_time, 3600):
            assert False, "@@@@无法上传ota包：%s, 请检查！！！！" % ota_path
        ota_page.refresh_page()
        ota_page.time_sleep(3)

    yield
    ota_page.go_to_new_address("ota")
    del_time = ota_page.get_current_time()
    while True:
        try:
            ota_page.search_device_by_pack_name(ota_name)
            if len(ota_page.get_ota_package_list()) == 0:
                break
            ota_page.delete_ota_package()
        except:
            pass
            ota_page.refresh_page()
            ota_page.time_sleep(2)
            if ota_page.get_current_time() > ota_page.return_end_time(del_time, 900):
                assert False, "@@@@平台无法删除ota包：%s, 请检查！！！！" % ota_name


@pytest.fixture()
def recover_and_login_mdm():
    # content_page.time_sleep(30)
    content_page.check_service_expired(user_info)
    yield
    content_page.check_service_expired(user_info)


@pytest.fixture()
def login_and_logout_serial():
    serial.loginSer()
    yield
    serial.logoutSer()


@pytest.fixture()
def uninstall_system_app():
    android_page.confirm_system_app_uninstalled()
    yield
    android_page.confirm_system_app_uninstalled()


@pytest.fixture()
def del_all_content_file():
    android_page.del_all_content_file()
    yield
    android_page.del_all_content_file()


@pytest.fixture()
def push_test_api_to_device():
    api_path = TestCase.Config().project_path + "\\Param\\Work_APP\\%s" % TestCase.yaml_data["work_app"]["api_txt"]
    if TestCase.yaml_data["website_info"]["test_api"] not in android_page.get_mdmApiUrl_text():
        android_page.push_file_to_device(api_path, "/" + android_page.get_internal_storage_directory() + "/")
        android_page.reboot_device(wifi_ip)
    yield
    api_path = TestCase.Config().project_path + "\\Param\\Work_APP\\%s" % TestCase.yaml_data["work_app"]["api_txt"]
    if TestCase.yaml_data["website_info"]["test_api"] not in android_page.get_mdmApiUrl_text():
        android_page.push_file_to_device(api_path, "/" + android_page.get_internal_storage_directory() + "/")
        android_page.reboot_device(wifi_ip)


@pytest.fixture()
def uninstall_multi_apps():
    android_page.uninstall_multi_apps(TestCase.yaml_data["app_info"])
    yield
    android_page.uninstall_multi_apps(TestCase.yaml_data["app_info"])


@pytest.fixture()
def del_download_apk():
    android_page.del_all_downloaded_apk()
    yield
    android_page.del_all_downloaded_apk()


@pytest.fixture()
def unlock_screen():
    android_page.device_unlock()
    yield


@pytest.fixture()
def delete_ota_package_relate():
    android_page.del_all_downloaded_zip()
    android_page.del_updated_zip()
    yield
    android_page.del_all_downloaded_zip()
    android_page.del_updated_zip()


@pytest.fixture()
def connected_wifi_adb():
    pass
    # yield
    # android_page.confirm_wifi_adb_connected(TestCase.wifi_ip)
    # android_page.device_existed(TestCase.wifi_ip)
    # android_page.device_boot_complete()


@pytest.fixture()
def connect_wifi_adb_USB():
    yield
    android_page.open_wifi_btn()
    android_page.confirm_wifi_btn_open()
    # android_page.confirm_wifi_adb_connected(TestCase.wifi_ip)


@pytest.fixture()
def return_device_page():
    yield
    device_page.go_to_new_address("devices")
    # device_page.click_devices_btn()
    # # click devices list btn  -- just for test version
    # device_page.click_devices_list_btn()


@pytest.fixture()
def go_to_and_return_device_page():
    device_page.go_to_new_address("devices")
    yield
    device_page.go_to_new_address("devices")


@pytest.fixture()
def go_to_device_page():
    device_page.go_to_new_address("devices")
    yield


@pytest.fixture()
def go_to_ota_upgrade_logs_page():
    ota_page.go_to_new_address("ota/log")
    yield


@pytest.fixture()
def go_to_ota_upgrade_package_page():
    ota_page.go_to_new_address("ota")
    yield


@pytest.fixture()
def go_to_ota_package_release():
    app_page.go_to_new_address("ota/release")
    yield


@pytest.fixture()
def go_to_app_page():
    app_page.go_to_new_address("apps")
    yield


@pytest.fixture()
def del_all_app_release_log():
    app_page.go_to_new_address("apps/releases")
    app_page.delete_all_app_release_log()
    yield
    app_page.go_to_new_address("apps/releases")
    app_page.delete_all_app_release_log()


@pytest.fixture()
def del_app_install_uninstall_release_log():
    app_page.delete_app_install_and_uninstall_logs()
    yield
    app_page.delete_app_install_and_uninstall_logs()


@pytest.fixture()
def del_all_ota_release_log_before():
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()
    yield


@pytest.fixture()
def del_all_ota_release_log_after():
    yield
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()


@pytest.fixture()
def del_all_ota_release_log():
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()
    yield
    ota_page.go_to_new_address("ota/release")
    ota_page.delete_all_ota_release_log()


@pytest.fixture()
def go_to_ota_page():
    ota_page.go_to_new_address("ota")
    yield


@pytest.fixture()
def del_all_app_release_log_after():
    yield
    app_page.go_to_new_address("apps/releases")
    app_page.delete_all_app_release_log()


@pytest.fixture()
def go_to_content_page():
    content_page.go_to_new_address("content")
    yield


@pytest.fixture()
def del_all_content_release_logs():
    content_page.go_to_new_address("content/release")
    content_page.delete_all_content_release_log()
    yield
    content_page.go_to_new_address("content/release")
    content_page.delete_all_content_release_log()


@pytest.fixture()
def go_to_content_release_page():
    content_page.go_to_new_address("content/release")
    yield


@pytest.fixture()
def go_to_content_upgrade_page():
    content_page.go_to_new_address("content/log")
    yield


@pytest.fixture()
def del_all_app_uninstall_release_log():
    app_page.go_to_new_address("apps/appUninstall")
    app_page.delete_all_app_release_log()
    yield


@pytest.fixture()
def del_all_app_uninstall_release_log_after():
    yield
    app_page.go_to_new_address("apps/appUninstall")
    app_page.delete_all_app_release_log()


@pytest.fixture()
def go_to_app_release_log():
    app_page.go_to_new_address("apps/releases")
    yield


@pytest.fixture()
def go_to_app_uninstall_release_log():
    app_page.go_to_new_address("apps/appUninstall")
    yield
