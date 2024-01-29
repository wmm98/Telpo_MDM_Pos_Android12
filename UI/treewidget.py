"""
这段代码是用于创建一个基于Qt的窗口应用程序的用户界面。它使用了Qt的QWidget、QVBoxLayout、QTreeWidget等类来创建窗口的布局和部件。

在这段代码中，窗口的主对象被命名为"MainWindow"，设置了其初始大小为618x594像素。窗口的中央部件是一个QWidget对象，命名为"centralwidget"，使用了一个QVBoxLayout垂直布局管理器来排列其中的部件。

在这个布局中，添加了一个QTreeWidget对象，命名为"treeWidget"，并设置了表头显示的文本为"1"。

接着，将"centralwidget"设置为MainWindow的中央部件，即窗口显示内容的区域。

代码中还创建了一个QMenuBar对象和一个QStatusBar对象，分别命名为"menubar"和"statusbar"，并将它们设置到MainWindow对应的位置上。

最后，通过调用retransla


"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 800)
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
        self.test_url_tips = QtWidgets.QLabel("测试地址:")
        self.test_url_edit = QtWidgets.QLineEdit()
        layout_url.addWidget(self.test_url_tips)
        layout_url.addWidget(self.test_url_edit, 1)
        self.verticalLayout.addLayout(layout_url)

        layout_test = QHBoxLayout()
        self.test_user_tips = QtWidgets.QLabel("测试用户名:")
        self.test_user_edit = QtWidgets.QLineEdit()
        self.test_psw_tips = QtWidgets.QLabel("测试密码:")
        self.test_psw = QtWidgets.QLineEdit()
        layout_test.addWidget(self.test_user_tips)
        layout_test.addWidget(self.test_user_edit)
        layout_test.addWidget(self.test_psw_tips)
        layout_test.addWidget(self.test_psw)
        self.verticalLayout.addLayout(layout_test)

        # 正式版信息
        layout_release_url = QHBoxLayout()
        self.release_user_info = QtWidgets.QLabel("\n正式版本用户信息:")
        self.verticalLayout.addWidget(self.release_user_info)
        self.release_url_tips = QtWidgets.QLabel("测试地址:")
        self.release_url_edit = QtWidgets.QLineEdit()
        layout_release_url.addWidget(self.release_url_tips)
        layout_release_url.addWidget(self.release_url_edit, 1)
        self.verticalLayout.addLayout(layout_release_url)

        layout_test = QHBoxLayout()
        self.test_user_tips = QtWidgets.QLabel("测试用户名:")
        self.test_user_edit = QtWidgets.QLineEdit()
        self.test_psw_tips = QtWidgets.QLabel("测试密码:")
        self.test_psw = QtWidgets.QLineEdit()
        layout_test.addWidget(self.test_user_tips)
        layout_test.addWidget(self.test_user_edit)
        layout_test.addWidget(self.test_psw_tips)
        layout_test.addWidget(self.test_psw)
        self.verticalLayout.addLayout(layout_test)

        layout0 = QHBoxLayout()
        # 我添加的
        self.device_info = QtWidgets.QLabel("\n设备信息：")
        self.verticalLayout.addWidget(self.device_info)
        self.label_device_name = QtWidgets.QLabel("设备名称:")
        self.edit_device_name = QtWidgets.QLineEdit()
        self.label_tips = QtWidgets.QLabel("(adb devices可查看)")
        layout0.addWidget(self.label_device_name)
        layout0.addWidget(self.edit_device_name, 2)
        layout0.addWidget(self.label_tips)
        layout0.addStretch(1)
        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout0)

        # 创建两个标签
        self.checkbox_serial = QCheckBox("串口")
        self.checkbox_screen = QCheckBox("横屏")
        self.checkbox_mdm = QCheckBox("安装mdm软件")
        self.checkbox_financial = QCheckBox("金融版本")

        # 将标签添加到水平布局中
        layout = QHBoxLayout()
        layout.addWidget(self.checkbox_serial)
        layout.addWidget(self.checkbox_screen)
        layout.addWidget(self.checkbox_mdm)
        layout.addWidget(self.checkbox_financial)
        # 添加一个拉伸因子以将水平布局放在窗口底部
        layout.addStretch(1)
        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout)

        # ota 包上传相关
        # OTA 包
        self.ota_info = QtWidgets.QLabel("\nOTA包：")
        self.verticalLayout.addWidget(self.ota_info)

        layout1 = QHBoxLayout()
        self.file_path = QtWidgets.QLineEdit()
        layout1.addWidget(self.file_path)

        # 上传按钮
        self.upload_button = QtWidgets.QPushButton("上传ota包")
        self.upload_button.clicked.connect(self.upload_file)
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

    def upload_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly

        # 打开文件选择对话框
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)",
                                                             options=options)
        if file_name:
            self.file_path.setText(file_name)

    #
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
