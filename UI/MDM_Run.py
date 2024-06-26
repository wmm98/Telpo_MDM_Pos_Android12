# -*- coding: utf-8 -*-
import subprocess
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool
from treewidget import Ui_MainWindow
import yaml
import os
import shutil


class AllCertCaseValue:
    ROOT_PROTOCON = 0
    # 立项测试 cases
    ROOT_PROTOCON_STA_CHILD = 1
    # sta scan tmi band0/1/2/3
    ROOT_PROTOCON_STA_TMISCAN_B0_0 = 1.1
    ROOT_PROTOCON_STA_TMISCAN_B0_1 = 1.2
    ROOT_PROTOCON_STA_TMISCAN_B0_2 = 1.3
    ROOT_PROTOCON_STA_TMISCAN_B0_3 = 1.4
    ROOT_PROTOCON_STA_TMISCAN_B0 = 1.5
    # ROOT_PROTOCON_STA_TMISCAN_B_2 = 2
    ROOT_PROTOCON_STA_TMISCAN_B1 = 3
    ROOT_PROTOCON_STA_TMISCAN_B2 = 4
    ROOT_PROTOCON_STA_TMISCAN_B3 = 5
    # sta tonemask band0/1/2/3
    ROOT_PROTOCON_STA_TM_B0 = 6
    ROOT_PROTOCON_STA_TM_B1 = 7
    ROOT_PROTOCON_STA_TM_B2 = 8
    ROOT_PROTOCON_STA_TM_B3 = 9
    ROOT_PROTOCON_STA_TM_B4 = 10
    ROOT_PROTOCON_STA_TM_B5 = 11
    ROOT_PROTOCON_STA_TM_B6 = 12
    ROOT_PROTOCON_STA_TM_B7 = 13
    ROOT_PROTOCON_STA_TM_B8 = 14
    ROOT_PROTOCON_STA_TM_B9 = 15
    ROOT_PROTOCON_STA_TM_B10 = 16
    ROOT_PROTOCON_STA_TM_B11 = 17
    ROOT_PROTOCON_STA_TM_B12 = 18
    ROOT_PROTOCON_STA_TM_B13 = 19
    ROOT_PROTOCON_STA_TM_B14 = 20
    ROOT_PROTOCON_STA_TM_B15 = 21
    ROOT_PROTOCON_STA_TM_B16 = 22

    ROOT_PROTOCON_STA_MAX = ROOT_PROTOCON_STA_TM_B16 + 1

    # 一般性测试 cases
    ROOT_PROTOCON_CCO_CHILD = 40
    # cco scan tmi band0/1/2/3
    ROOT_PROTOCON_CCO_TMISCAN_B0_0 = 40.1
    ROOT_PROTOCON_CCO_TMISCAN_B0_1 = 40.2
    ROOT_PROTOCON_CCO_TMISCAN_B0_2 = 40.3
    ROOT_PROTOCON_CCO_TMISCAN_B0 = 41
    ROOT_PROTOCON_CCO_TMISCAN_B1 = 42
    ROOT_PROTOCON_CCO_TMISCAN_B2 = 43
    ROOT_PROTOCON_CCO_TMISCAN_B3 = 44
    # sta tonemask band0/1/2/3
    ROOT_PROTOCON_CCO_TM_B0 = 45
    ROOT_PROTOCON_CCO_TM_B1 = 46
    ROOT_PROTOCON_CCO_TM_B2 = 47
    ROOT_PROTOCON_CCO_TM_B3 = 48
    ROOT_PROTOCON_CCO_TM_B4 = 49

    ROOT_PROTOCON_CCO_MAX = ROOT_PROTOCON_CCO_TM_B4 + 1

    # 专项测试 cases
    ROOT_PERFORMANCE_CHILD = 80
    ROOT_PERFORMANCE_STA_CHILD_0 = 80.1
    ROOT_PERFORMANCE_STA_CHILD_1 = 80.2
    ROOT_PERFORMANCE_STA_CHILD_2 = 80.3
    ROOT_PERFORMANCE_STA_CHILD_3 = 80.4
    ROOT_PERFORMANCE_STA_CHILD = 81

    # white noise
    ROOT_PERFORMANCE_STA_WN_B1 = 82
    ROOT_PERFORMANCE_STA_WN_B2 = 83
    # anti-ppm
    ROOT_PERFORMANCE_STA_ANTIPPM_B1 = 84
    ROOT_PERFORMANCE_STA_ANTIPPM_B2 = 85
    # anti-attenuation
    ROOT_PERFORMANCE_STA_ANTIATT_B1 = 86
    ROOT_PERFORMANCE_STA_ANTIATT_B2 = 87
    # anti-narrowband
    ROOT_PERFORMANCE_STA_ANTINARROW_B1 = 88
    ROOT_PERFORMANCE_STA_ANTINARROW_B2 = 89
    # anti-pulse
    ROOT_PERFORMANCE_STA_ANTIPULSE_B1 = 90
    ROOT_PERFORMANCE_STA_ANTIPULSE_B2 = 91
    # psd
    ROOT_PERFORMANCE_STA_PSD_B1 = 92
    ROOT_PERFORMANCE_STA_PSD_B2 = 93
    # sta rate
    ROOT_PERFORMANCE_STA_RATE_B1 = 94
    ROOT_PERFORMANCE_STA_RATE_B2 = 95

    ROOT_PERFORMANCE_STA_MAX = ROOT_PERFORMANCE_STA_RATE_B2 + 1

    ROOT_PERFORMANCE_CCO_CHILD = 100
    # white noise
    ROOT_PERFORMANCE_CCO_WN_B0 = 100.1
    ROOT_PERFORMANCE_CCO_WN_B1 = 101
    ROOT_PERFORMANCE_CCO_WN_B2 = 102
    # anti-ppm
    ROOT_PERFORMANCE_CCO_ANTIPPM_B1 = 103
    ROOT_PERFORMANCE_CCO_ANTIPPM_B2 = 104
    # anti-attenuation
    ROOT_PERFORMANCE_CCO_ANTIATT_B1 = 105
    ROOT_PERFORMANCE_CCO_ANTIATT_B2 = 106
    # anti-narrowband
    ROOT_PERFORMANCE_CCO_ANTINARROW_B1 = 107
    ROOT_PERFORMANCE_CCO_ANTINARROW_B2 = 108
    # anti-pulse
    ROOT_PERFORMANCE_CCO_ANTIPULSE_B1 = 109
    ROOT_PERFORMANCE_CCO_ANTIPULSE_B2 = 110
    # psd
    ROOT_PERFORMANCE_CCO_PSD_B1 = 111
    ROOT_PERFORMANCE_CCO_PSD_B2 = 112
    # CCO rate
    ROOT_PERFORMANCE_CCO_RATE_B1 = 113
    ROOT_PERFORMANCE_CCO_RATE_B2 = 114
    ROOT_PERFORMANCE_CCO_MAX = ROOT_PERFORMANCE_CCO_RATE_B2 + 1
    # 压测
    ROOT_OTHER_CHILD = 130
    ROOT_OTHER_RATE = 131
    ROOT_OTHER_RATE1 = 132
    ROOT_OTHER_RATE2 = 133
    ROOT_OTHER_MAX = ROOT_OTHER_RATE2 + 1

    # max
    TREE_MAX = ROOT_OTHER_MAX + 1


DictCommandInfo = {

    "A": AllCertCaseValue.ROOT_PROTOCON,
    # STA test case
    "立项测试": AllCertCaseValue.ROOT_PROTOCON_STA_CHILD,
    # "登录连网-辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_0,
    # "添加ota升级包--辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_1,
    # "添加APK包--辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_2,
    "添加content文件--辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_3,
    "断网重连获取aimdm消耗的流量": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0,
    "限定4G网络推送app ": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B1,
    "限定WIFI网络推送app ": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B2,
    "OTA断网重连断点续传": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B3,
    "推送低版本的APP/卸载后重新安装 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B0,
    "推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B1,
    "锁机和解锁 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B2,
    "发送设备重启指令：设备重启5次": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B3,
    "重置设备TPUI密码 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B4,
    "重置设备密码 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B5,
    "AIMDM发消息压力测试 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B6,
    "AIMDM 切换正式测试服服务api": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B7,
    "日志的抓取": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B8,
    "推送壁纸 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B9,
    "应用满屏推送 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B10,
    "推送text.zip文件 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B11,
    "多应用推送 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B11,
    "静默卸载正在运行中的app： 静默卸载/卸载正在运行的app ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B12,
    "静默ota升级 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B13,
    "静默升级系统app/推送安装成功后自动运行app ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B14,
    "推送开机logo/动画 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B15,
    "关机 ": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B16,

    # CCO test case
    "一般性测试": AllCertCaseValue.ROOT_PROTOCON_CCO_CHILD,
    # "登录连网-辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_0,
    # "添加ota升级包--辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_1,
    # "添加APK包--辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_2,
    "OTA断网重连次断点续传": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0,
    "OTA重启断点续传": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B1,
    "OTA升级": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B2,
    "推送低版本的APP/卸载后重新安装": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B3,
    "推送高版本APP覆盖安装/卸载后检测重新下载/卸载重启检查安装/同版本覆盖安装/低版本覆盖安装": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B0,
    "静默升级系统app/推送安装成功后自动运行app": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B1,
    "静默卸载/卸载正在运行的app": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B2,
    "切换正式测试服服务api": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B3,
    "一般性-日志的抓取": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B4,

    # communication performance
    "专项测试": AllCertCaseValue.ROOT_PERFORMANCE_CHILD,
    # "登录连网-辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_0,
    # "添加ota升级包--辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_1,
    # "添加APK包--辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_2,
    "添加content文件--辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_3,
    "系统/应用日志的抓取": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD,
    "应用满屏推送": AllCertCaseValue.ROOT_PERFORMANCE_STA_WN_B1,
    "推送壁纸": AllCertCaseValue.ROOT_PERFORMANCE_STA_WN_B2,
    "OTA静默升级": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPPM_B1,
    "普通应用静默升级": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPPM_B2,
    "系统应用静默升级/推送安装成功后自动运行app": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIATT_B1,
    "限定4G网络推送app": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIATT_B2,
    "限定WIFI网络推送app": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTINARROW_B1,
    "文件文件推送成功率": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTINARROW_B2,
    "文件推送-网络恢复断点续传": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPULSE_B1,
    # "e": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPULSE_B2,
    # "f": AllCertCaseValue.ROOT_PERFORMANCE_STA_PSD_B1,
    # "g": AllCertCaseValue.ROOT_PERFORMANCE_STA_PSD_B2,
    # "h": AllCertCaseValue.ROOT_PERFORMANCE_STA_RATE_B1,
    # "i": AllCertCaseValue.ROOT_PERFORMANCE_STA_RATE_B2,

    "回归测试": AllCertCaseValue.ROOT_PERFORMANCE_CCO_CHILD,
    # "登录连网 - 辅助测试用例": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B0,
    "锁机和解锁  ": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B1,
    "发送设备重启指令：设备重启5次压测": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B2,
    "重置设备TPUI密码": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPPM_B1,
    "重置设备密码": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPPM_B2,
    "AIMDM发消息压力测试": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIATT_B1,
    "回归-日志的抓取": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIATT_B2,
    "断网重连压测消耗流量情况": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTINARROW_B1,
    "断网重连静默升级app": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTINARROW_B2,
    "关机测试": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPULSE_B1,
    # "t": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPULSE_B2,
    # "u": AllCertCaseValue.ROOT_PERFORMANCE_CCO_PSD_B1,
    # "v": AllCertCaseValue.ROOT_PERFORMANCE_CCO_PSD_B2,
    # "w": AllCertCaseValue.ROOT_PERFORMANCE_CCO_RATE_B1,
    # "x": AllCertCaseValue.ROOT_PERFORMANCE_CCO_RATE_B2,

    # other test case
    "压测": AllCertCaseValue.ROOT_OTHER_CHILD,
    "OTA下载拷贝校验完整性压测": AllCertCaseValue.ROOT_OTHER_RATE,
    "APK大附件断点续传压测": AllCertCaseValue.ROOT_OTHER_RATE1,
    "APK大附件压测": AllCertCaseValue.ROOT_OTHER_RATE2
}


class tree(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(tree, self).__init__()
        self.setupUi(self)
        self.AllTestCase = None
        self.intiui()

    def intiui(self):
        # 设置列数
        self.treeWidget.setColumnCount(1)

        # 设置树形控件头部的标题
        self.treeWidget.setHeaderLabels(['测试用例'])
        self.treeWidget.setColumnWidth(0, 120)

        # 设置根节点
        self.AllTestCase = QTreeWidgetItem(self.treeWidget)
        self.AllTestCase.setText(0, '测试项')
        # self.AllTestCase.setCheckState(0, Qt.Unchecked)
        # self.AllTestCase.setFlags(self.AllTestCase.flags() | Qt.ItemIsSelectable)
        # self.AllTestCase.setFlags(self.AllTestCase.flags() & ~Qt.ItemIsUserCheckable)  # 移除可选中的标志位

        # 通过字典获取所有子项
        item_protocon = ""
        item_sta_father = ""
        item_cco_father = ""
        item_prerf_father = ""
        item_prerf_sta_father = ""
        item_prerf_cco_father = ""
        item_other_father = ""

        for value in DictCommandInfo.keys():
            if DictCommandInfo[value] == AllCertCaseValue.ROOT_PROTOCON_STA_CHILD:
                item_sta_father = QTreeWidgetItem(self.AllTestCase)
                item_sta_father.setText(0, value)
                item_sta_father.setCheckState(0, Qt.Unchecked)
                item_sta_father.setFlags(item_sta_father.flags() | Qt.ItemIsSelectable)
            elif (AllCertCaseValue.ROOT_PROTOCON_STA_CHILD < DictCommandInfo[value] <
                  AllCertCaseValue.ROOT_PROTOCON_STA_MAX):
                item_sta_child = QTreeWidgetItem(item_sta_father)
                item_sta_child.setText(0, value)
                item_sta_child.setCheckState(0, Qt.Unchecked)
                item_sta_child.setFlags(item_sta_child.flags() | Qt.ItemIsSelectable)
            elif DictCommandInfo[value] == AllCertCaseValue.ROOT_PROTOCON_CCO_CHILD:
                item_cco_father = QTreeWidgetItem(self.AllTestCase)
                item_cco_father.setText(0, value)
                item_cco_father.setCheckState(0, Qt.Unchecked)
                item_cco_father.setFlags(item_cco_father.flags() | Qt.ItemIsSelectable)
            elif (AllCertCaseValue.ROOT_PROTOCON_CCO_CHILD < DictCommandInfo[value] <
                  AllCertCaseValue.ROOT_PROTOCON_CCO_MAX):
                item_cco_child = QTreeWidgetItem(item_cco_father)
                item_cco_child.setText(0, value)
                item_cco_child.setCheckState(0, Qt.Unchecked)
                item_cco_child.setFlags(item_cco_child.flags() | Qt.ItemIsSelectable)
            elif DictCommandInfo[value] == AllCertCaseValue.ROOT_PERFORMANCE_CHILD:
                item_prerf_father = QTreeWidgetItem(self.AllTestCase)
                item_prerf_father.setText(0, value)
                item_prerf_father.setCheckState(0, Qt.Unchecked)
                item_prerf_father.setFlags(item_prerf_father.flags() | Qt.ItemIsSelectable)
            elif (AllCertCaseValue.ROOT_PERFORMANCE_CHILD < DictCommandInfo[value] <
                  AllCertCaseValue.ROOT_PERFORMANCE_STA_MAX):
                item_perf_sta_child = QTreeWidgetItem(item_prerf_father)
                item_perf_sta_child.setText(0, value)
                item_perf_sta_child.setCheckState(0, Qt.Unchecked)
                item_perf_sta_child.setFlags(item_perf_sta_child.flags() | Qt.ItemIsSelectable)
            elif DictCommandInfo[value] == AllCertCaseValue.ROOT_PERFORMANCE_CCO_CHILD:
                item_prerf_cco_father = QTreeWidgetItem(self.AllTestCase)
                item_prerf_cco_father.setText(0, value)
                item_prerf_cco_father.setCheckState(0, Qt.Unchecked)
                item_prerf_cco_father.setFlags(item_prerf_cco_father.flags() | Qt.ItemIsSelectable)
            elif (AllCertCaseValue.ROOT_PERFORMANCE_CCO_CHILD < DictCommandInfo[value] <
                  AllCertCaseValue.ROOT_PERFORMANCE_CCO_MAX):
                item_perf_cco_child = QTreeWidgetItem(item_prerf_cco_father)
                item_perf_cco_child.setText(0, value)
                item_perf_cco_child.setCheckState(0, Qt.Unchecked)
                item_perf_cco_child.setFlags(item_perf_cco_child.flags() | Qt.ItemIsSelectable)
            elif DictCommandInfo[value] == AllCertCaseValue.ROOT_OTHER_CHILD:
                item_other_father = QTreeWidgetItem(self.AllTestCase)
                item_other_father.setText(0, value)
                item_other_father.setCheckState(0, Qt.Unchecked)
                item_other_father.setFlags(item_other_father.flags() | Qt.ItemIsSelectable)
            elif AllCertCaseValue.ROOT_OTHER_CHILD < DictCommandInfo[value] < \
                    AllCertCaseValue.ROOT_OTHER_MAX:
                item_other_child = QTreeWidgetItem(item_other_father)
                item_other_child.setText(0, value)
                item_other_child.setCheckState(0, Qt.Unchecked)
                item_other_child.setFlags(item_other_child.flags() | Qt.ItemIsSelectable)

        # 节点全部展开
        self.treeWidget.expandAll()
        # self.treeWidget.expand(1)
        # 链接槽函数
        self.treeWidget.itemChanged.connect(self.handlechanged)

        self.aimdm_upload_button.clicked.connect(self.aimdm_upload_file)
        self.tpui_info_upload_button.clicked.connect(self.tpui_upload_file)
        self.upload_button.clicked.connect(self.ota_upload_file)

        # 使能aimdm 上传按钮
        self.checkbox_mdm.stateChanged.connect(self.onAimdmCheckboxStateChanged)
        # 使能COM口输入框
        self.checkbox_serial.stateChanged.connect(self.onSerialCheckboxStateChanged)
        # 测试设备状态：
        self.devic_online_btn.clicked.connect(self.checkDeviceOnline)
        # 连接信号和槽
        self.submit_button.clicked.connect(self.handle_submit)

    def get_message_box(self, text):
        QMessageBox.warning(self, "错误提示", text)

    def checkDeviceOnline(self):
        device_name = self.edit_device_name.text()
        if len(device_name) == 0:
            self.get_message_box("设备名称为空，输入设备名称")
            return
        # 需要串口的情况
        if self.checkbox_serial.isChecked():
            # pass
            COM_name = self.COM_name.currentText()
            if COM_name.strip() in self.serial.get_current_COM():
                self.serial.loginSer(COM_name)
                if self.serial.check_usb_adb_connect_serial(device_name):
                    current_firmware_version = self.serial.invoke(
                        "adb -s %s shell getprop ro.product.version" % self.edit_device_name.text())
                    destination_version = str(self.ota_file_path.text()).split("-")[-1][:-4]
                    self.device_state_tips.setText("设备当前的版本：%s, 目标版本为：%s" % (
                        self.serial.remove_space(current_firmware_version), destination_version))
                    self.device_state_tips.setVisible(True)
                else:
                    self.device_state_tips.setText("设备%s不在线， 请再次测试！！！" % device_name)
                    self.device_state_tips.setVisible(True)
                self.serial.confirm_relay_closed()
                self.serial.logoutSer()
            else:
                self.get_message_box("没有可用的串口，请检查！！！")
        else:
            # 不需要串口的情况下
            if self.serial.check_usb_adb_connect_no_serial(device_name):
                current_firmware_version = self.serial.invoke(
                    "adb -s %s shell getprop ro.product.version" % self.edit_device_name.text())
                destination_version = str(self.ota_file_path.text()).split("-")[-1][:-4]
                self.device_state_tips.setText(
                    "设备当前的版本：%s, 目标版本为：%s" % (self.serial.remove_space(current_firmware_version), destination_version))
                self.device_state_tips.setVisible(True)
            else:
                self.device_state_tips.setText("设备%s不在线， 请再次测试！！！" % device_name)
                self.device_state_tips.setVisible(True)

    def handle_submit(self):

        # 获取文本框中的文本内容
        tree_status = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            tree_status.append(self.get_tree_item_status(item))

        # 修改yaml 数据的属性值
        if 'TestCase' not in self.data:
            self.data["TestCase"] = {}

        for slave in tree_status[0]["children"]:
            # print(slave)
            if slave["text"] == '立项测试':
                if "LiXiang_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["LiXiang_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["LiXiang_Test"]["LiXiang_Test-case%d" % i] = int(child["status"])
                    i += 1
            elif slave["text"] == '一般性测试':
                if "General_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["General_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["General_Test"]["General_Test-case%d" % i] = int(child["status"])
                    i += 1
            elif slave["text"] == '专项测试':
                if "Special_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["Special_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["Special_Test"]["Special_Test-case%d" % i] = int(child["status"])
                    i += 1
            elif slave["text"] == '回归测试':
                if "Regression_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["Regression_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["Regression_Test"]["Regression_Test-case%d" % i] = int(child["status"])
                    i += 1
            elif slave["text"] == '稳定性测试':
                if "Stability_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["Stability_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["Stability_Test"]["Stability_Test-case%d" % i] = int(child["status"])
                    i += 1
            elif slave["text"] == '压测':
                if "Pressure_Test" not in self.data["TestCase"]:
                    self.data["TestCase"]["Pressure_Test"] = {}
                i = 0
                for child in slave['children']:
                    self.data["TestCase"]["Pressure_Test"]["Pressure_Test-case%d" % i] = int(child["status"])
                    i += 1

        # # 拷贝上传的文件并且改变yaml 里字段的值
        package_path = self.project_path + "\\Param\\Package\\"
        work_path = self.project_path + "\\Param\\Work_APP\\"
        ota_name = str(self.ota_file_path.text())
        aimdm_name = str(self.aimdm_file_path.text())
        tpui_name = str(self.tpui_info_file_path.text())
        if "/" in ota_name:
            ota_real_name = ota_name.split("/")[-1]
            # 修改字段值
            self.data["MDMTestData"]["ota_packages_info"]["package_name"] = ota_real_name
            self.copy_file(ota_name, package_path + ota_real_name)
        elif "/" in aimdm_name:
            aimdm_name_real_name = aimdm_name.split("/")[-1]
            if self.checkbox_mdm.isChecked():
                self.copy_file(aimdm_name, work_path + aimdm_name_real_name)
        elif "/" in tpui_name:
            tpui_real_name = tpui_name.split("/")[-1]
            self.copy_file(tpui_name, work_path + tpui_real_name)

        # 文本框非空检查
        if len(self.test_url_edit.text()) == 0:
            self.get_message_box("测试地址不能为空!")
            return
        elif len(self.test_api_edit.text()) == 0:
            self.get_message_box("测试服务api不能为空!")
            return
        elif len(self.test_user_edit.text()) == 0:
            self.get_message_box("测试账号不能为空!")
            return
        elif len(self.test_psw_edit.text()) == 0:
            self.get_message_box("测试密码不能为空!")
            return
        elif len(self.edit_device_name.text()) == 0:
            # 显示错误消息框
            self.get_message_box("设备名称不能为空!")
            return
        elif len(self.ota_file_path.text()) == 0:
            self.get_message_box("请上传OTA包!")
            return
        elif len(self.aimdm_file_path.text()) == 0:
            if self.checkbox_mdm.isChecked():
                self.get_message_box("请上传aimdm软件!")
                return

        # 修改用户信息
        self.data["MDMTestData"]["website_info"]["test_url"] = self.test_url_edit.text()
        self.data["MDMTestData"]["website_info"]["test_api"] = self.test_api_edit.text()
        self.data["MDMTestData"]["website_info"]["test_user"] = self.test_user_edit.text()
        self.data["MDMTestData"]["website_info"]["test_password"] = self.test_psw_edit.text()
        self.data["MDMTestData"]["website_info"]["release_url"] = self.release_url_edit.text()
        self.data["MDMTestData"]["website_info"]["release_api"] = self.release_api_edit.text()
        self.data["MDMTestData"]["website_info"]["release_user"] = self.release_edit.text()
        self.data["MDMTestData"]["website_info"]["release_password"] = self.release_psw_edit.text()

        # 检设备名字，检查check box 属性
        self.data["MDMTestData"]["android_device_info"]["device_name"] = self.edit_device_name.text()
        self.data["MDMTestData"]["android_device_info"]["is_serial"] = self.checkbox_serial.isChecked()
        self.data["MDMTestData"]["android_device_info"]["install_aimdm"] = self.checkbox_mdm.isChecked()
        self.data["MDMTestData"]["android_device_info"]["is_user"] = self.checkbox_user.isChecked()
        self.data["MDMTestData"]["android_device_info"]["is_landscape"] = self.checkbox_screen.isChecked()
        if self.checkbox_serial.isChecked():
            self.data["MDMTestData"]["android_device_info"]["COM"] = self.COM_name.currentText()

        testcases = []
        for cases in self.data["TestCase"]:
            for case in self.data["TestCase"][cases]:
                if self.data["TestCase"][cases][case] == 2:
                    testcases.append(case)
        # 检测用例为非空
        if len(testcases) == 0:
            self.get_message_box("请勾选需要测试的用例！！！")
            return
        # 保存要跑得用例
        self.data["Run_Cases"] = ",".join(testcases)
        # 需要测试的数据：General_Test - case0, General_Test - case4, General_Test - case5, General_Test - case6
        # 保存修改后的内容回 YAML 文件
        with open(self.yaml_file_path, 'w') as file:
            yaml.safe_dump(self.data, file)
        self.close()
        subprocess.run([self.project_path + "\\run.bat"])

    # 获取所有节点的状态
    def get_tree_item_status(self, tree_item):
        status = tree_item.checkState(0)
        result = {
            "text": tree_item.text(0),
            "status": status,
            "children": []
        }
        # 我添加的
        for i in range(tree_item.childCount()):
            child_item = tree_item.child(i)
            # print(child_item.text())
            # print(self.get_tree_item_status(child_item))
            result["children"].append(self.get_tree_item_status(child_item))
        return result

    def handle_selection_changed(self):
        tree_status = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)
            tree_status.append(self.get_tree_item_status(item))

    def handlechanged(self, item, column):
        # 获取选中节点的子节点个数
        count = item.childCount()
        # 如果被选中
        if item.checkState(column) == Qt.Checked:
            # 连同下面子子节点全部设置为选中状态
            for f in range(count):
                if item.child(f).checkState(0) != Qt.Checked:
                    item.child(f).setCheckState(0, Qt.Checked)
        # 如果取消选中
        if item.checkState(column) == Qt.Unchecked:
            # 连同下面子子节点全部设置为取消选中状态
            for f in range(count):
                if item.child(f).checkState != Qt.Unchecked:
                    item.child(f).setCheckState(0, Qt.Unchecked)

    def copy_file(self, origin, des):
        if self.path_is_existed(origin):
            while True:
                if not self.path_is_existed(des):
                    shutil.copy(origin, des)
                else:
                    break
                self.time_sleep(1)
        else:
            raise Exception("此路径不存在: %s, 请检查！！！" % origin)

    def path_is_existed(self, path):
        if os.path.exists(path):
            return True
        else:
            return False

    def ota_upload_file(self):
        # 打开文件选择对话框
        ota_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)",
                                                                 options=self.options)
        if ota_file_name:
            self.ota_file_path.setText(ota_file_name)

    def aimdm_upload_file(self):
        # 打开文件选择对话框
        aimdm_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                                   "All Files (*);;Text Files (*.txt)",
                                                                   options=self.options)
        if aimdm_file_name:
            self.aimdm_file_path.setText(aimdm_file_name)

    def tpui_upload_file(self):
        # 打开文件选择对话框
        tpui_file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "",
                                                                  "All Files (*);;Text Files (*.txt)",
                                                                  options=self.options)
        if tpui_file_name:
            self.tpui_info_file_path.setText(tpui_file_name)

    def onSerialCheckboxStateChanged(self, state):
        if state == 2:  # 选中状态
            self.COM_name.setEnabled(True)
            ports = self.serial.get_current_COM()
            for port in ports:
                self.COM_name.addItem(port)
            if len(ports) == 0:
                self.err_COM_Tips.setText("没有可用的COM口, 请检查！！！")
                self.err_COM_Tips.setVisible(True)
                self.COM_name.setEnabled(True)
            elif len(ports) == 1:
                pass
            else:
                self.err_COM_Tips.setText("当前多个COM可用, 请需要需测试COM口！！！")
                self.err_COM_Tips.setVisible(True)
        else:
            self.err_COM_Tips.setVisible(False)
            self.COM_name.setDisabled(True)

    def CheckCOMBoxTextChange(self, text):
        if self.COM_name.isEnabled():
            if len(text) != 0:
                if text.strip() not in self.serial.get_current_COM():
                    self.err_COM_Tips.setText("当前COM口不可用，请重新输入！！！")
                    self.err_COM_Tips.setVisible(True)
                else:
                    self.err_COM_Tips.setVisible(False)
            else:
                self.err_COM_Tips.setText("请输入可用COM口！！！")
                self.err_COM_Tips.setVisible(True)

    def onAimdmCheckboxStateChanged(self, state):
        if state == 2:  # 选中状态
            self.aimdm_upload_button.setEnabled(True)
        else:
            self.aimdm_upload_button.setEnabled(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = tree()
    myshow.show()
    sys.exit(app.exec_())
