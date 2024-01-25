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
        MainWindow.resize(618, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)

        # 我添加的
        self.label = QtWidgets.QLabel("设备名称（adb devices）:")
        self.line_edit = QtWidgets.QLineEdit()
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.line_edit)

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
        # self.label = QtWidgets.QLabel("姓名:")
        # self.line_edit = QtWidgets.QLineEdit()
        # self.verticalLayout.addWidget(self.label)
        # self.verticalLayout.addWidget(self.line_edit)
        # 我添加的
        self.submit_button = QtWidgets.QPushButton("提交")
        self.verticalLayout.addWidget(self.submit_button)

        # 创建水平布局
        layout = QHBoxLayout()

        # 创建两个标签
        self.checkbox1 = QCheckBox("串口")
        self.checkbox2 = QCheckBox("横屏")
        self.checkbox3 = QCheckBox("安装mdm软件")

        # 将标签添加到水平布局中
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)


        # 将标签放入水平布局
        # horizontal_layout.addWidget(label)

        # 添加一个拉伸因子以将水平布局放在窗口底部
        layout.addStretch(1)

        # 将水平布局放入垂直布局
        self.verticalLayout.addLayout(layout)

        # # 将垂直布局设置为窗口的布局
        # self.treeWidget.setLayout(self.verticalLayout)

    #
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


