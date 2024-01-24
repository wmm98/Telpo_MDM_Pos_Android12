from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tree_widget = QTreeWidget()
        self.tree_widget.setSelectionMode(QTreeWidget.ExtendedSelection)  # 设置多选模式

        self.setCentralWidget(self.tree_widget)

        # 添加树节点
        parent_item = QTreeWidgetItem(self.tree_widget)
        parent_item.setText(0, "Parent 1")

        child_item1 = QTreeWidgetItem(parent_item)
        child_item1.setText(0, "Child 1")

        child_item2 = QTreeWidgetItem(parent_item)
        child_item2.setText(0, "Child 2")

        child_item3 = QTreeWidgetItem(parent_item)
        child_item3.setText(0, "Child 3")

        # 连接信号和槽函数
        self.tree_widget.selectionModel().selectionChanged.connect(self.handle_selection_changed)

    def handle_selection_changed(self, selected, deselected):
        selected_indexes = selected.indexes()
        if selected_indexes:
            selected_items = [index.data() for index in selected_indexes]
            print("被选中的项：", selected_items)
        else:
            print("没有选中项")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()