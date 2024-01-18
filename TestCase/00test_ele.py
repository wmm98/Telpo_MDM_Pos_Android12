import uiautomator2 as u2
# # from Common.Shell import Shell
# # import time
# # # from PIL import Image
# import time
# # import subprocess
# # import threading
# # from concurrent.futures import ThreadPoolExecutor
# #
# from selenium import webdriver
#
# from selenium import webdriver
#
# # 创建一个 Edge 浏览器实例
# # driver = webdriver.Edge()
# driver = webdriver.Chrome()
# # 打开 Microsoft 的网站
# driver.get("https://www.baidu.com")
# driver.implicitly_wait(5)
# driver.maximize_window()
# time.sleep(5)
# # 执行其他自动化测试操作...
#
# # 关闭浏览器
# driver.quit()
# #
# # chrome_options = pack.Options()
# # chrome_options.add_argument("--allow-insecure-localhost")  # 允许访问不安全的本地主机（可选）
# # chrome_options.add_argument("--ignore-certificate-errors")  # 忽略证书错误
# # driver = pack.webdriver.Chrome(options=chrome_options)
#
# driver = webdriver.Chrome()
# driver.implicitly_wait(5)
# driver.maximize_window()
# # url = 'http://test.telpoai.com/login'
# url = "http://www.baidu.com"
# # 窗口最大化
# driver.get(url)
# time.sleep(5)
# ele = driver.find_element(By.ID, "IU")
# ele.value_of_css_property()

# print(driver.current_url)
#

# device = u2.Device()
# device.screen_off()
# device.press("power")
# device.swipe(0.1, 0.9, 0.9, 0.1)
# device.swipe(0.1, 0.9, 0.9, 0.1)
# device.unlock()
# print(device.current_app())
# print(device.current_app())
#
# # cmd_send = Shell()
# # # # #
# usb_device = u2.connect("d")
# print(usb_device.device_info)
# # usb_device.freeze_rotation(True)
# print(usb_device.info)
# print(usb_device.app_current())
# print(usb_device.wlan_ip)
# text = usb_device.shell("wm size").output
# print(text)
# print((text.split("x")))
# usb_device(resourceId="com.tpos.aimdm:id/confirm").child()
# usb_device.swipe(700, 780, 700, 400, duration=0.5)
# usb_device.swipe(400, 600, 400, 300)
# ele = usb_device(text="CONFIRM")
# ele = usb_device(resourceId="com.tpos.aimdm:id/confirm")
# x, y = ele.center()
# for i in range(6):
#     # ele = usb_device(resourceId="com.tpos.aimdm:id/confirm")
#     # ele = usb_device(text="CONFIRM")
#     # ele.click_gone(maxretry=12, interval=0.15)
#     # print(ele)
#     # print(ele.center())
#     # ele.long_click(duration=0.2)
#     # usb_device.click(0.745, 0.519)
#     # usb_device.shell("input tap 531 677")
#     usb_device.long_click(x, y, duration=0.2)
#     # time.sleep(3)
#     # time.sleep(0.2)

# usb_device.settings
# res = u2.Device("d")
# res(resourceId="4").click()
# # print(res.info)
# res.shell("input keyevent KEYCODE_APP_SWITCH")
# res.shell("input keyevent KEYCODE_APP_SWITCH")
# res.exists()


# act2 = res.shell("%s |grep \"registrationState=\"").output
# print(act2)
# print(res.device_info)
# res.app_stop_all()
# print(res.info)

#
# res.press("recent")
# res.press("recent")
#
# Swipe up or down to clear the recent apps (adjust the coordinates accordingly)
# res.swipe(500, 1500, 500, 500)

# # print(res.wlan_ip)
# # wifi_d = u2.connect_adb_wifi("10.168.1.234")
# # u2.connect_usb()
# # print(wifi_d.info)
# # u2.connect_adb_wifi()
# # usb_device = u2.Device("d")
# # res = usb_device.push("E:\Mingming\Telpo_Automation\Telpo_MDM\Param\Package\perfmon.apk", "/sdcard/")
# # usb_device.unlock()
# # usb_device.unlock()
# # # usb_device.screen_on()
# # # usb_device.screen_off()
# # # print(usb_device.device_info)
# # # for i in usb_device.device_info:
# # #     print(i, usb_device.device_info[i])
# # print("===================================")
# # print(usb_device.device_info["battery"]["usbPowered"])
# # import time
# # # print("请拔开USB线后点击确定!!!!!")
# # while True:
# #     res = usb_device.device_info["battery"]["usbPowered"]
# #     print(res)
# #     if not res:
# #         break
# #     else:
# #         print("还没有拔开USB线， 请拨开后点击确定!!!!!")
# #     time.sleep(2)
# # print(usb_device.info)
# # for j in usb_device.info:
# #     print(j, usb_device.info[j])
# # print("===================================")
# # print(usb_device.info.get("screenOn"))
#
# # print(usb_device.exists(["sdcard/aimdm"]))
# # wifi_device = u2.Device("10.168.1.159:5555")
# # wifi_device.press("home")
# # # file = wifi_device.screenshot("full_screen.jpg")
# # print(wifi_device.app_current())
# # wifi_device.app_stop("com.bjw.ComAssistant")
#
# # wifi_device.screenshot("full_screen1")
# # print(file)
# # # 打开照片文件
# # image = Image.open(file)
# # print(image)
# # #
# # # # 保存照片到本地
# # image.save('E:\\%s' % file)
# #
# # print("照片保存成功")
#
# # usb_device.app_start('com.android.settings')
# # print(usb_device.app_current()['package'])
# # print(usb_device.info)
# # print(usb_device.wlan_ip)
# # 10.168.1.159
#
# # print(usb_device.wlan_ip)
# #
# # wifi_device = u2.Device("10.168.1.159:5555")
# # wifi_device = u2.connect_adb_wifi("10.168.1.159:5555")
# # print(wifi_device.info)
#
# # print(cmd_send.invoke("adb -s 10.168.1.159:5555 shell getprop sys.boot_completed"))
# #
# # wifi_device.uiautomator.start()
# # wifi_device.app_start('com.telpo.mylauncher.launcher3')
# # # wifi_device.app_stop('com.tpos.aimdm')
# # wifi_device.app_start('com.tpos.aimdm')
# # #
# # # print(cmd_send.invoke("adb devices"))
# # cmd_send.invoke("adb -s 10.168.1.159:5555 reboot")
# # time.sleep(90)
# # print("***********重启之后*******************")
# # print(cmd_send.invoke("adb connect 10.168.1.159:5555"))
# # # while True:
# # #     if "10.168.1.159:5555" in cmd_send.invoke("adb devices"):
# # #         break
# # #     else:
# # #         time.sleep(2)
# # #
# # # time.sleep(5)
# # print(cmd_send.invoke("adb connect 10.168.1.159:5555"))
# # time.sleep(5)
# # print(cmd_send.invoke("adb connect 10.168.1.159:5555"))
# # print(cmd_send.invoke("adb connect 10.168.1.159:5555"))
# # print(cmd_send.invoke("adb connect 10.168.1.159:5555"))
# # print(wifi_device.info)
# # print(cmd_send.invoke("adb devices"))
# # print(cmd_send.invoke("adb -s 10.168.1.159:5555 shell getprop sys.boot_completed"))
# #
# import yaml
#
# #
# # # # 从 YAML 文件中加载数据
# # path = r"E:\\Mingming\\Telpo_Automation\\Telpo_MDM\\Conf\\test_data.yaml"
# # with open(path, 'r', encoding='utf-8') as file:
# #     data = yaml.load(file, Loader=yaml.FullLoader)
# # #
# # # # 访问数据
# # print(data['MDMTestData']['Content_info']['wallpaper'])
# # # print(type(data['MDMTestData']['settings']['version']))
#

# import uiautomator2 as u2
# import subprocess
#
#
# try:
#     d = u2.connect_adb_wifi("10.168.1.231:555")  # 连接设备
# except Exception as e:
#     print(e)
#     # print(type(e))
#     print(str(e))

# # d.app_install()
# print(d.info)
# 调用函数来防止设备休眠


# name = {"name": [1, 3], "age": [40, 60]}
#
# for i in name:
#     print(name[i])
#
# print(list(name.values()))
#
# print(type(name.values()))
# for i in list(name.values()):
#     print(i)
#     # for j in i:
#     #     print(j)

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView
from PyQt5.QtGui import QStandardItemModel, QStandardItem

import sys
from PyQt5.QtWidgets import QApplication, QTreeView, QWidget, QVBoxLayout, QLabel, \
    QAbstractItemView, QCheckBox, QHBoxLayout, QLineEdit

class CheckableTreeView(QTreeView):
    def __init__(self, parent=None):
        super(CheckableTreeView, self).__init__(parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setModel(QStandardItemModel())

class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Checkable Tree View')

        treeView = CheckableTreeView()
        model = treeView.model()

        # 添加根节点
        rootItem = model.invisibleRootItem()
        for i in range(3):
            parentItem = QStandardItem(f'模块{i}')
            parentItem.setCheckable(True)
            rootItem.appendRow(parentItem)

            # 添加子节点
            for j in range(5):
                childItem = QStandardItem(f'用例{j}')
                childItem.setCheckable(True)
                parentItem.appendRow(childItem)

        layout = QVBoxLayout()
        layout.addWidget(treeView)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())

# class ModuleSubCaseSelectionWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
#
#     def init_ui(self):
#         self.setWindowTitle("Module Sub-Case Selection")
#         self.setGeometry(400, 400, 300, 400)
#
#         self.tree_view = QTreeView(self)
#         self.setCentralWidget(self.tree_view)
#
#         self.model = QStandardItemModel()
#         self.tree_view.setModel(self.model)
#
#         self.add_module("Module 1")
#         self.add_sub_case("Sub Case 1.1", "Module 1")
#         self.add_sub_case("Sub Case 1.2", "Module 1")
#
#         self.add_module("Module 2")
#         self.add_sub_case("Sub Case 2.1", "Module 2")
#         self.add_sub_case("Sub Case 2.2", "Module 2")
#         self.add_sub_case("Sub Case 2.3", "Module 2")
#
#         self.add_module("Module 3")
#         self.add_sub_case("Sub Case 3.1", "Module 3")
#
#         self.tree_view.expandAll()
#
#         self.show()
#
#     def add_module(self, module_name):
#         module_item = QStandardItem(module_name)
#         module_item.setCheckable(True)
#         self.model.appendRow(module_item)
#
#     def add_sub_case(self, case_name, module_name):
#         module_item = self.find_module_item(module_name)
#         if module_item is not None:
#             case_item = QStandardItem(case_name)
#             case_item.setCheckable(True)
#             module_item.appendRow(case_item)
#
#     def find_module_item(self, module_name):
#         for row in range(self.model.rowCount()):
#             item = self.model.item(row)
#             if item.text() == module_name:
#                 return item
#         return None
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ModuleSubCaseSelectionWindow()
#     sys.exit(app.exec_())