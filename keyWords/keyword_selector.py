class KeywordSelector(QMainWindow):
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
        button_layout.addWidget(self.copy_button)
        button_layout.addWidget(self.reset_button)
        layout.addLayout(button_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
