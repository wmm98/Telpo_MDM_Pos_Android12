import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel

# 创建应用程序实例
app = QApplication(sys.argv)

# 创建窗口
window = QWidget()

# 创建水平布局
layout = QHBoxLayout()

# 创建两个标签
label1 = QLabel("标签1")
label2 = QLabel("标签2")

# 将标签添加到水平布局中
layout.addWidget(label1)
layout.addWidget(label2)

# 将水平布局设置为窗口的布局
window.setLayout(layout)

# 显示窗口
window.show()

# 运行应用程序
sys.exit(app.exec_())