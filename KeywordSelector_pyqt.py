import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QMessageBox, QGroupBox, QGridLayout, QScrollArea, QFrame
from PyQt5.QtCore import Qt
import configparser
from PyQt5.QtGui import QFont, QPalette, QColor


class KeywordSelector(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载配置文件，存储不同分类的关键词
        self.config = configparser.ConfigParser()
        self.config.read('keywords.ini', encoding="utf-8")

        self.similar_keywords = {}
        self.keywords = {}
        # 初始化keywords、similar_keywords
        for category in self.config.sections():
            similar_keywords = {}
            keywords_str = self.config[category]['keywords']
            keywords_list = keywords_str.split(',')

            processed_keywords = []
            for keyword in keywords_list:
                if '（' in keyword:
                    main_keyword = keyword.split('（')[0]
                    similars = keyword.split('（')[1].replace('）', '').split('、')
                    similar_keywords[main_keyword] = similars
                    processed_keywords.append(main_keyword)
                else:
                    processed_keywords.append(keyword)

            self.keywords[category] = processed_keywords
            self.similar_keywords[category] = similar_keywords

        self.selected_keywords = []  # 存储已选中的关键词

        self.initUI()

    def initUI(self):
        # 初始化界面和布局
        self.setWindowTitle('关键词生成器')
        self.setGeometry(100, 100, 800, 600)

        # 自定义区
        self.custom_entry = QLineEdit(self)
        self.custom_entry.setFixedHeight(50)
        self.custom_entry.textChanged.connect(self.update_output_text)

        # 分割线
        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFrameShadow(QFrame.Sunken)
        separator_line.setLineWidth(1)

        # 选择区
        self.select_widget = QGroupBox(self)
        self.select_widget.setStyleSheet('QGroupBox { border: 0px; }')

        self.category_list = QVBoxLayout()
        self.category_buttons = []

        for category in self.keywords.keys():
            category_button = QPushButton(category, self.select_widget)
            category_button.setCheckable(True)
            category_button.setStyleSheet('''
                # QPushButton {
                #     background-color: transparent;
                #     color: black;
                # }
                QPushButton:checked {
                    background-color: #DCEAFB;
                    color: black;
                }
            ''')
            category_button.setFont(QFont('Arial', 9, QFont.Bold))
            category_button.clicked.connect(lambda checked, b=category_button: self.toggle_category_buttons(b))
            self.category_buttons.append(category_button)
            self.category_list.addWidget(category_button)

        self.select_layout = QHBoxLayout()
        self.select_layout.addLayout(self.category_list)
        self.select_layout.addWidget(separator_line)

        self.keywords_widget = QWidget(self.select_widget)

        self.keywords_layout = QGridLayout(self.keywords_widget)
        self.keywords_layout.setAlignment(Qt.AlignTop)
        self.keywords_layout.setHorizontalSpacing(10)
        self.keywords_layout.setVerticalSpacing(5)

        self.keywords_layout.setContentsMargins(0, 0, 0, 0)

        self.select_layout.addWidget(self.keywords_widget)
        self.select_widget.setLayout(self.select_layout)
        self.select_widget.setStyleSheet('QGroupBox { border: 1px solid black; }')

        # 使用滚动区域包装关键词区域
        scroll_area = QScrollArea(self.select_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.keywords_widget)
        self.select_layout.addWidget(scroll_area)
        # 设置关键字区样式表
        scroll_area.setStyleSheet('QScrollArea { border: 0px; }')

        # 输出区
        self.output_label = QLabel('关键词', self)
        self.output_label.setFont(QFont('Arial', 10, QFont.Bold))
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_text = QTextEdit(self)
        self.output_text.setFixedHeight(100)
        self.copy_button = QPushButton('复制', self)
        self.copy_button.setFont(QFont('Arial', 9, QFont.Bold))
        self.copy_button.setFixedWidth(80)
        self.copy_button.setMinimumHeight(30)
        self.copy_button.clicked.connect(self.copy_keywords)
        self.reset_button = QPushButton('重置', self)
        self.reset_button.setFont(QFont('Arial', 9, QFont.Bold))
        self.reset_button.setFixedWidth(80)
        self.reset_button.setMinimumHeight(30)
        self.reset_button.clicked.connect(self.reset_keywords)

        # 布局
        layout = QVBoxLayout()

        layout.addWidget(self.custom_entry)
        layout.addWidget(self.select_widget)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        # 状态栏
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignCenter)
        self.statusBar().addWidget(self.status_label)
        # self.statusBar().setStyleSheet('QStatusBar::item {border: none;}')
        self.statusBar().setFixedHeight(30)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.status_label.setAlignment(Qt.AlignCenter)

        # 点击展示关键字
        for category_button in self.category_buttons:
            category_button.clicked.connect(lambda checked, b=category_button: self.toggle_keywords(b))

        # 默认选中第一个分类名按钮，并展开其关键字
        if self.category_buttons:
            self.category_buttons[0].setChecked(True)
            self.toggle_keywords(self.category_buttons[0])

    def toggle_category_buttons(self, clicked_button):
        # 切换分类按钮状态
        for button in self.category_buttons:
            if button is not clicked_button:
                button.setChecked(False)

    def toggle_keywords(self, category_button):
        # 切换展示关键词
        category = category_button.text()
        self.clear_keywords()

        if category_button.isChecked():
            keywords = self.keywords[category]
            max_cols = 4
            for i, keyword in enumerate(keywords):
                row = i // max_cols
                col = i % max_cols
                keyword_button = QPushButton(keyword, self.keywords_widget)
                keyword_button.setCheckable(True)
                keyword_button.setMinimumHeight(40)

                similar_keys = self.similar_keywords.get(category).get(keyword)

                if similar_keys is not None:
                    keyword_button.clicked.connect(lambda checked, k=keyword, s=similar_keys: self.add_keyword(k, s))
                else:
                    keyword_button.clicked.connect(lambda checked, k=keyword: self.add_keyword(k, []))

                self.keywords_layout.addWidget(keyword_button, row, col, 1, 1)
            self.keywords_layout.addWidget(QWidget(), row, col + 1, 1, max_cols - col - 1)

            # 设置当前分类按钮为淡蓝色
            category_button.setProperty('selected', True)
        else:
            # 恢复初始状态
            category_button.setProperty('selected', False)

        # 刷新样式
        category_button.setStyle(category_button.style())

    def clear_keywords(self):
        # 清空关键词布局
        while self.keywords_layout.count():
            item = self.keywords_layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def add_keyword(self, keyword, similar_keywords):
        # 添加关键词及其相关关键词
        if keyword in self.selected_keywords:
            # 关键词已存在，从列表中删除关键词及其相关关键词
            self.selected_keywords = [k for k in self.selected_keywords if k not in [keyword] + similar_keywords]
        else:
            # 关键词不存在，添加关键词及其相关关键词
            self.selected_keywords.append(keyword)
            if similar_keywords:
                self.selected_keywords.extend(similar_keywords)

        self.update_output_text()

    def update_output_text(self):
        # 更新输出文本
        custom_keywords = self.custom_entry.text()
        keywords = ' '.join([custom_keywords] + self.selected_keywords).strip()
        self.output_text.setPlainText(keywords)

    def copy_keywords(self):
        # 复制关键词到剪贴板
        keywords = self.output_text.toPlainText().strip()
        if not keywords:
            self.statusBar().showMessage('还没有输入或选中关键字!', 3000)  # 展示3s状态栏
        else:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.output_text.toPlainText())
            self.statusBar().showMessage('关键词已复制到剪贴板!', 3000)

    def reset_keywords(self):
        # 重置关键词选择器
        self.custom_entry.clear()
        self.selected_keywords.clear()
        self.deselect_keywords()
        self.update_output_text()

    def deselect_keywords(self):
        # 取消选中所有关键词
        for i in range(self.keywords_layout.count()):
            item = self.keywords_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, QPushButton):
                widget.setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeywordSelector()
    window.show()
    sys.exit(app.exec_())
