"""
这段代码是用于创建一个基于Qt的窗口应用程序的用户界面。它使用了Qt的QWidget、QVBoxLayout、QTreeWidget等类来创建窗口的布局和部件。

在这段代码中，窗口的主对象被命名为"MainWindow"，设置了其初始大小为618x594像素。窗口的中央部件是一个QWidget对象，命名为"centralwidget"，使用了一个QVBoxLayout垂直布局管理器来排列其中的部件。

在这个布局中，添加了一个QTreeWidget对象，命名为"treeWidget"，并设置了表头显示的文本为"1"。

接着，将"centralwidget"设置为MainWindow的中央部件，即窗口显示内容的区域。

代码中还创建了一个QMenuBar对象和一个QStatusBar对象，分别命名为"menubar"和"statusbar"，并将它们设置到MainWindow对应的位置上。

最后，通过调用retransla


"""

import os
import yaml
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QHBoxLayout, QCheckBox
import UI_Serial


class Ui_MainWindow(object):
    serial = UI_Serial.Serial()
    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.ReadOnly
    project_path = str(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
    yaml_file_path = project_path + "\\Conf\\test_ui.yaml"
    # 加载 YAML 文件
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)

        # 创建水平布局
        # 测试信息
        layout_url = QHBoxLayout()
        self.test_user_info = QtWidgets.QLabel("当前测试用户信息:")
        self.verticalLayout.addWidget(self.test_user_info)
        self.test_url_tips = QtWidgets.QLabel("地址:")
        self.test_url_edit = QtWidgets.QLineEdit()
        # 默认显示为上次的URL
        self.test_url_edit.setText(self.data["MDMTestData"]["website_info"]["test_url"])
        layout_url.addWidget(self.test_url_tips)
        layout_url.addWidget(self.test_url_edit, 1)
        self.verticalLayout.addLayout(layout_url)
        # api信息
        layout_test_api = QHBoxLayout()
        self.test_api = QtWidgets.QLabel("服务器api:")
        layout_test_api.addWidget(self.test_api)
        self.test_api_edit = QtWidgets.QLineEdit()
        self.test_api_edit.setText(self.data["MDMTestData"]["website_info"]["test_api"])
        layout_test_api.addWidget(self.test_api_edit)
        self.verticalLayout.addLayout(layout_test_api)

        layout_test = QHBoxLayout()
        self.test_user_tips = QtWidgets.QLabel("用户名:")
        self.test_user_edit = QtWidgets.QLineEdit()
        self.test_user_edit.setText(self.data["MDMTestData"]["website_info"]["test_user"])
        self.test_psw_tips = QtWidgets.QLabel("密码:")
        self.test_psw_edit = QtWidgets.QLineEdit()
        self.test_psw_edit.setText(self.data["MDMTestData"]["website_info"]["test_password"])
        layout_test.addWidget(self.test_user_tips)
        layout_test.addWidget(self.test_user_edit)
        layout_test.addWidget(self.test_psw_tips)
        layout_test.addWidget(self.test_psw_edit)
        self.verticalLayout.addLayout(layout_test)

        # 正式服信息
        layout_release_url = QHBoxLayout()
        self.release_user_info = QtWidgets.QLabel("\n正式版本用户信息:")
        self.verticalLayout.addWidget(self.release_user_info)
        self.release_url_tips = QtWidgets.QLabel("地址:")
        self.release_url_edit = QtWidgets.QLineEdit()
        self.release_url_edit.setText(self.data["MDMTestData"]["website_info"]["release_url"])
        layout_release_url.addWidget(self.release_url_tips)
        layout_release_url.addWidget(self.release_url_edit, 1)
        self.verticalLayout.addLayout(layout_release_url)

        # api信息
        layout_release_api = QHBoxLayout()
        self.release_api = QtWidgets.QLabel("服务器api:")
        self.release_api_edit = QtWidgets.QLineEdit()
        self.release_api_edit.setText(self.data["MDMTestData"]["website_info"]["release_api"])
        layout_release_api.addWidget(self.release_api)
        layout_release_api.addWidget(self.release_api_edit)
        self.verticalLayout.addLayout(layout_release_api)

        layout_test = QHBoxLayout()
        self.release_tips = QtWidgets.QLabel("用户名:")
        self.release_edit = QtWidgets.QLineEdit()
        self.release_edit.setText(self.data["MDMTestData"]["website_info"]["release_user"])
        self.release_psw_tips = QtWidgets.QLabel("密码:")
        self.release_psw_edit = QtWidgets.QLineEdit()
        self.release_psw_edit.setText(self.data["MDMTestData"]["website_info"]["release_password"])
        layout_test.addWidget(self.release_tips)
        layout_test.addWidget(self.release_edit)
        layout_test.addWidget(self.release_psw_tips)
        layout_test.addWidget(self.release_psw_edit)
        self.verticalLayout.addLayout(layout_test)

        self.device_info = QtWidgets.QLabel("\n设备信息：")
        self.verticalLayout.addWidget(self.device_info)
        # 将标签添加到水平布局中
        # 添加checkbox
        layout = QHBoxLayout()
        # 创建两个标签
        self.checkbox_screen = QCheckBox("横屏")
        self.checkbox_mdm = QCheckBox("安装mdm软件")
        self.checkbox_financial = QCheckBox("金融版本")
        self.checkbox_serial = QCheckBox("串口")
        self.COM_label = QtWidgets.QLabel("当前COM口:")
        # COM相关信息处理
        self.COM_name = QtWidgets.QLineEdit()
        self.COM_name.setDisabled(True)
        self.err_COM_Tips = QtWidgets.QLabel()
        self.err_COM_Tips.setStyleSheet("color: red;")
        self.err_COM_Tips.setVisible(False)

        layout.addWidget(self.checkbox_screen)
        layout.addWidget(self.checkbox_mdm)
        layout.addWidget(self.checkbox_financial)
        layout.addWidget(self.checkbox_serial)
        layout.addWidget(self.COM_label)
        layout.addWidget(self.COM_name)
        layout.addWidget(self.err_COM_Tips)
        # 添加一个拉伸因子以将水平布局放在窗口底部
        layout.addStretch(1)
        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout)
        # 添加设备文本框
        layout0 = QHBoxLayout()
        self.label_device_name = QtWidgets.QLabel("设备名称:")
        self.edit_device_name = QtWidgets.QLineEdit()
        self.label_tips = QtWidgets.QLabel("(adb devices可查看)")
        layout0.addWidget(self.label_device_name)
        layout0.addWidget(self.edit_device_name, 2)
        layout0.addWidget(self.label_tips)
        layout0.addStretch(1)
        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout0)

        # aimdm软件上传
        self.aimdm_info = QtWidgets.QLabel("\nAIMDM软件：")
        self.verticalLayout.addWidget(self.aimdm_info)

        layout_aimdm = QHBoxLayout()
        self.aimdm_file_path = QtWidgets.QLineEdit()
        self.aimdm_file_path.setText(self.data["MDMTestData"]["work_app"]["aidmd_apk"])
        layout_aimdm.addWidget(self.aimdm_file_path)

        self.aimdm_upload_button = QtWidgets.QPushButton("点击上传")
        self.aimdm_upload_button.clicked.connect(self.aimdm_upload_file)
        self.aimdm_upload_button.setEnabled(False)  # 默认禁用上传按钮
        layout_aimdm.addWidget(self.aimdm_upload_button)
        self.verticalLayout.addLayout(layout_aimdm)

        # tpui软件上传
        self.tpui_info = QtWidgets.QLabel("TPUI软件：")
        self.verticalLayout.addWidget(self.tpui_info)

        layout_tpui_info = QHBoxLayout()
        self.tpui_info_file_path = QtWidgets.QLineEdit()
        self.tpui_info_file_path.setText(self.data["MDMTestData"]["work_app"]["aidmd_apk"])
        layout_tpui_info.addWidget(self.tpui_info_file_path)

        self.tpui_info_upload_button = QtWidgets.QPushButton("点击上传")
        self.tpui_info_upload_button.clicked.connect(self.tpui_upload_file)
        layout_tpui_info.addWidget(self.tpui_info_upload_button)
        self.verticalLayout.addLayout(layout_tpui_info)

        # ota 包上传相关
        # OTA 包
        self.ota_info = QtWidgets.QLabel("OTA包：")
        self.verticalLayout.addWidget(self.ota_info)

        layout1 = QHBoxLayout()
        self.ota_file_path = QtWidgets.QLineEdit()
        self.ota_file_path.setText(self.data["MDMTestData"]["ota_packages_info"]["package_name"])
        layout1.addWidget(self.ota_file_path)

        # 上传按钮
        self.upload_button = QtWidgets.QPushButton("点击上传")
        self.upload_button.clicked.connect(self.ota_upload_file)
        layout1.addWidget(self.upload_button)
        self.verticalLayout.addLayout(layout1)

        # 设置多选模式
        self.treeWidget.setSelectionMode(QtWidgets.QTreeWidget.ExtendedSelection)  # 设置多选模式
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.treeWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 我添加的
        self.submit_button = QtWidgets.QPushButton("提交")
        self.verticalLayout.addWidget(self.submit_button)

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
            self.COM_name.setDisabled(False)
            COMs = self.serial.get_current_COM()
            print(COMs)
            if len(COMs) == 0:
                self.COM_name.setText("")
                self.COM_name.setDisabled(True)
                self.err_COM_Tips.setText("没有可用的COM口, 请检查！！！")
                self.err_COM_Tips.setVisible(True)
            elif len(COMs) == 1:
                self.err_COM_Tips.setVisible(False)
                self.COM_name.setText(COMs[0])
            else:
                self.err_COM_Tips.setText("当前多个COM可用, 请输入需测试COM口！！！")
                self.err_COM_Tips.setVisible(True)
        else:
            self.COM_name.setText("")
            self.err_COM_Tips.setVisible(False)
            self.COM_name.setDisabled(True)

    def CheckCOMBoxTextChange(self, text):
        if self.checkbox_serial.isChecked():
            if len(text) != 0:
                self.err_COM_Tips.setVisible(False)
                if text.strip() not in self.serial.get_current_COM():
                    self.err_COM_Tips.setText("当前COM口不可用，请重新输入！！！")
                    self.err_COM_Tips.setVisible(True)
            else:
                self.err_COM_Tips.setText("请输入可用COM口！！！")
                self.err_COM_Tips.setVisible(True)

    def onAimdmCheckboxStateChanged(self, state):
        if state == 2:  # 选中状态
            self.aimdm_upload_button.setEnabled(True)
        else:
            self.aimdm_upload_button.setEnabled(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
