# -*- coding: utf-8 -*-
import subprocess
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from treewidget import Ui_MainWindow


class AllCertCaseValue:
    ROOT_PROTOCON = 0
    # STA 协议一致性所有case
    ROOT_PROTOCON_STA_CHILD = 1
    # sta scan tmi band0/1/2/3
    ROOT_PROTOCON_STA_TMISCAN_B0 = 2
    ROOT_PROTOCON_STA_TMISCAN_B1 = 3
    ROOT_PROTOCON_STA_TMISCAN_B2 = 4
    ROOT_PROTOCON_STA_TMISCAN_B3 = 5
    # sta tonemask band0/1/2/3
    ROOT_PROTOCON_STA_TM_B0 = 6
    ROOT_PROTOCON_STA_TM_B1 = 7
    ROOT_PROTOCON_STA_TM_B2 = 8
    ROOT_PROTOCON_STA_TM_B3 = 9

    ROOT_PROTOCON_STA_MAX = ROOT_PROTOCON_STA_TM_B3 + 1

    # CCO 协议一致性所有case
    ROOT_PROTOCON_CCO_CHILD = 40
    # cco scan tmi band0/1/2/3
    ROOT_PROTOCON_CCO_TMISCAN_B0 = 41
    ROOT_PROTOCON_CCO_TMISCAN_B1 = 42
    ROOT_PROTOCON_CCO_TMISCAN_B2 = 43
    ROOT_PROTOCON_CCO_TMISCAN_B3 = 44
    # sta tonemask band0/1/2/3
    ROOT_PROTOCON_CCO_TM_B0 = 45
    ROOT_PROTOCON_CCO_TM_B1 = 46
    ROOT_PROTOCON_CCO_TM_B2 = 47
    ROOT_PROTOCON_CCO_TM_B3 = 48

    ROOT_PROTOCON_CCO_MAX = ROOT_PROTOCON_CCO_TM_B3 + 1

    # 通信性能测试
    ROOT_PERFORMANCE_CHILD = 80
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
    "C": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B0,
    "D": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B1,
    "E": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B2,
    "F": AllCertCaseValue.ROOT_PROTOCON_STA_TMISCAN_B3,
    "G": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B0,
    "H": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B1,
    "I": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B2,
    "J": AllCertCaseValue.ROOT_PROTOCON_STA_TM_B3,

    # CCO test case
    "一般性测试": AllCertCaseValue.ROOT_PROTOCON_CCO_CHILD,
    "L": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B0,
    "M": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B1,
    "N": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B2,
    "O": AllCertCaseValue.ROOT_PROTOCON_CCO_TMISCAN_B3,
    "P": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B0,
    "Q": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B1,
    "R": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B2,
    "S": AllCertCaseValue.ROOT_PROTOCON_CCO_TM_B3,

    # communication performance
    "专项测试": AllCertCaseValue.ROOT_PERFORMANCE_CHILD,
    "U": AllCertCaseValue.ROOT_PERFORMANCE_STA_CHILD,
    "V": AllCertCaseValue.ROOT_PERFORMANCE_STA_WN_B1,
    "W": AllCertCaseValue.ROOT_PERFORMANCE_STA_WN_B2,
    "X": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPPM_B1,
    "Y": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPPM_B2,
    "Z": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIATT_B1,
    "a": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIATT_B2,
    "b": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTINARROW_B1,
    "c": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTINARROW_B2,
    "d": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPULSE_B1,
    "e": AllCertCaseValue.ROOT_PERFORMANCE_STA_ANTIPULSE_B2,
    "f": AllCertCaseValue.ROOT_PERFORMANCE_STA_PSD_B1,
    "g": AllCertCaseValue.ROOT_PERFORMANCE_STA_PSD_B2,
    "h": AllCertCaseValue.ROOT_PERFORMANCE_STA_RATE_B1,
    "i": AllCertCaseValue.ROOT_PERFORMANCE_STA_RATE_B2,

    "回归测试": AllCertCaseValue.ROOT_PERFORMANCE_CCO_CHILD,

    "k": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B1,
    "l": AllCertCaseValue.ROOT_PERFORMANCE_CCO_WN_B2,
    "m": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPPM_B1,
    "n": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPPM_B2,
    "o": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIATT_B1,
    "p": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIATT_B2,
    "q": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTINARROW_B1,
    "r": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTINARROW_B2,
    "s": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPULSE_B1,
    "t": AllCertCaseValue.ROOT_PERFORMANCE_CCO_ANTIPULSE_B2,
    "u": AllCertCaseValue.ROOT_PERFORMANCE_CCO_PSD_B1,
    "v": AllCertCaseValue.ROOT_PERFORMANCE_CCO_PSD_B2,
    "w": AllCertCaseValue.ROOT_PERFORMANCE_CCO_RATE_B1,
    "x": AllCertCaseValue.ROOT_PERFORMANCE_CCO_RATE_B2,

    # other test case
    "稳定性测试": AllCertCaseValue.ROOT_OTHER_CHILD,
    "z": AllCertCaseValue.ROOT_OTHER_RATE,
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
        # 链接槽函数
        self.treeWidget.itemChanged.connect(self.handlechanged)

        # 查看复选框的状态

        # 连接信号和槽
        self.submit_button.clicked.connect(self.handle_submit)

    def handle_submit(self):

        print("==================")
        print(self.checkbox_serial.isChecked())

        # 获取文本框中的文本内容
        text = self.edit_device_name.text()
        print("提交的姓名是: %s" % text)
        tree_status = []
        for i in range(self.treeWidget.topLevelItemCount()):
            item = self.treeWidget.topLevelItem(i)

            tree_status.append(self.get_tree_item_status(item))
        print(tree_status)
        # 检查文本内容是否为空
        if len(text) == 0:
            # 显示错误消息框
            QMessageBox.warning(self, "错误提示", "设备名称不能为空!")
            return
        else:

            self.close()
            subprocess.run(["python", "UI_issue.py"])

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
        print(tree_status)

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = tree()
    myshow.show()
    sys.exit(app.exec_())
