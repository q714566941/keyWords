import tkinter as tk
import tkinter.ttk as ttk
import configparser

class KeywordSelector:
    def __init__(self):
        # 加载配置文件，存储不同分类的关键词
        self.config = configparser.ConfigParser()
        self.config.read('keywords.ini', encoding="utf-8")

        self.keywords = {}
        for category in self.config.sections():
            self.keywords[category] = self.config[category]['keywords'].split(',')

        # 创建GUI界面
        self.window = tk.Tk()
        self.window.title('关键词选择器')
        self.window.geometry('800x600')

        # 自定义区
        self.custom_label = ttk.Label(self.window, text='自定义关键词：')
        self.custom_label.pack(pady=10)
        self.custom_entry_var = tk.StringVar()  # 创建StringVar变量
        self.custom_entry = ttk.Entry(self.window, textvariable=self.custom_entry_var)  # 绑定StringVar变量
        self.custom_entry.pack(padx=50, pady=10, fill='x')

        # 选择区
        self.select_label = ttk.Label(self.window, text='选择关键词：')
        self.select_label.pack(pady=10)
        self.select_frame = ttk.Frame(self.window)
        self.select_frame.pack(padx=50, pady=10)
        for category, keywords in self.keywords.items():
            category_label = ttk.Label(self.select_frame, text=category)
            category_label.pack(pady=5, anchor='w')
            for keyword in keywords:
                button = ttk.Button(self.select_frame, text=keyword, command=lambda k=keyword: self.add_keyword(k))
                button.pack(side='left', padx=5, pady=5)

        # 输出区
        self.output_label = ttk.Label(self.window, text='关键词：')
        self.output_label.pack(pady=10)
        self.output_frame = ttk.Frame(self.window)
        self.output_frame.pack(padx=50, pady=10, fill='x')
        self.output_text = tk.Text(self.output_frame, height=5)
        self.output_text.pack(side='left', fill='both', expand=True)
        self.copy_button = ttk.Button(self.output_frame, text='复制', command=self.copy_keywords)
        self.copy_button.pack(side='right', padx=5)
        self.reset_button = ttk.Button(self.output_frame, text='重置', command=self.reset_keywords)
        self.reset_button.pack(side='right', padx=5)

        # 绑定自定义关键词输入框的内容变化事件
        self.custom_entry_var.trace('w', self.update_output_text)

        # 运行界面
        self.window.mainloop()

    def add_keyword(self, keyword):
        # 将选择的关键词添加到输出区
        current_keywords = self.output_text.get('1.0', tk.END).strip()
        if current_keywords:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, current_keywords + ' ' + keyword)
        else:
            self.output_text.insert(tk.END, keyword)

    def update_output_text(self, *args):
        # 更新输出区的内容
        custom_keywords = self.custom_entry_var.get()
        selected_keywords = self.get_selected_keywords()
        keywords = ' '.join([custom_keywords] + selected_keywords).strip()  # 使用strip()去除前后空格
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, keywords)

    def get_selected_keywords(self):
        # 获取选择关键词列表
        selected_keywords = []
        for category, keywords in self.keywords.items():
            selected_keywords.extend([keyword for keyword in keywords if keyword in self.output_text.get('1.0', tk.END)])
        return selected_keywords

    def copy_keywords(self):
        # 复制输出区的内容到剪贴板
        self.window.clipboard_clear()
        self.window.clipboard_append(self.output_text.get('1.0', tk.END))

    def reset_keywords(self):
        # 清空输出区的内容和自定义关键词输入框
        self.output_text.delete('1.0', tk.END)
        self.custom_entry_var.set('')

window = KeywordSelector()
