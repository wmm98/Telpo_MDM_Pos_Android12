# -*- coding: utf-8 -*-
import subprocess
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
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

    ROOT_OTHER_CHILD = 130
    ROOT_OTHER_RATE = 131
    ROOT_OTHER_MAX = ROOT_OTHER_RATE + 1

    # max
    TREE_MAX = ROOT_OTHER_MAX + 1


DictCommandInfo = {

    "A": AllCertCaseValue.ROOT_PROTOCON,
    # STA test case
    "立项测试": AllCertCaseValue.ROOT_PROTOCON_STA_CHILD,
    "登录连网-辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_0,
    "添加ota升级包--辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_1,
    "添加APK包--辅助测试用例": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0_2,
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
    "登录连网-辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_0,
    "添加ota升级包--辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_1,
    "添加APK包--辅助测试用例 ": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0_2,
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
    "登录连网-辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_0,
    "添加ota升级包--辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_1,
    "添加APK包--辅助测试用例  ": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD_2,
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
    "登录连网 - 辅助测试用例": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B0,
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
    "稳定性测试": AllCertCaseValue.ROOT_OTHER_CHILD,
    "待定": AllCertCaseValue.ROOT_OTHER_RATE,
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

        # 使能aimdm 上传按钮
        self.checkbox_mdm.stateChanged.connect(self.onCheckboxStateChanged)

        # 连接信号和槽
        self.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):

        print("==================")
        print(self.checkbox_serial.isChecked())

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

        # # 拷贝上传的 ota文件
        package_path = self.project_path + "\\Param\\Package\\"
        work_path = self.project_path + "\\Param\\Work_APP\\"
        # print(self.ota_file_path.text())
        # print(self.aimdm_file_path.text())
        # print(self.tpui_info_file_path.text())
        ota_name = self.ota_file_path.text()
        aimdm_name = self.aimdm_file_path.text()
        tpui_name = self.tpui_info_file_path.text()
        if "/" in ota_name:
            print(ota_name.split("/")[-1])
            self.copy_file(ota_name, package_path + ota_name.split("/")[-1])
        elif "/" in aimdm_name:
            if self.checkbox_mdm.isChecked():
                self.copy_file(aimdm_name, work_path + aimdm_name.split("/")[-1])
        elif "/" in tpui_name:
            self.copy_file(tpui_name, work_path + tpui_name.split("/")[-1])

        # 检查文本内容是否为空
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
        else:
            # 保存修改后的内容回 YAML 文件
            with open(self.yaml_file_path, 'w') as file:
                yaml.safe_dump(self.data, file)
            subprocess.run(["python", "UI_issue.py"])
            self.close()

    def get_message_box(self, text):
        QMessageBox.warning(self, "错误提示", text)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = tree()
    myshow.show()
    sys.exit(app.exec_())
