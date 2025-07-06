import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QScrollArea
)
from CLIENT import client  # client.py가 CLIENT 폴더 안에 있어야 함


class HttpTestApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("📡 HTTP 테스트 클라이언트")
        self.setGeometry(300, 300, 700, 450)

        # 전체 레이아웃 구성
        hbox = QHBoxLayout()

        # 왼쪽 버튼 레이아웃
        button_layout = QVBoxLayout()
        self.buttons = []
        for i in range(1, 10):
            btn = QPushButton(f"CASE{i}")
            btn.clicked.connect(lambda _, x=i: self.run_case(x))
            button_layout.addWidget(btn)
            self.buttons.append(btn)

        # 오른쪽 텍스트 출력 레이아웃
        text_layout = QVBoxLayout()

        self.req_label = QLabel("📤 Request")
        self.req_text = QTextEdit()
        self.req_text.setReadOnly(True)

        self.res_label = QLabel("📥 Response")
        self.res_text = QTextEdit()
        self.res_text.setReadOnly(True)

        text_layout.addWidget(self.req_label)
        text_layout.addWidget(self.req_text)
        text_layout.addWidget(self.res_label)
        text_layout.addWidget(self.res_text)

        hbox.addLayout(button_layout, 1)
        hbox.addLayout(text_layout, 3)

        self.setLayout(hbox)
        self.show()
    
    def run_case(self, i):
        try:
            case_func = getattr(client, f"CASE{i}")
            request, response = case_func()
            self.req_text.setPlainText(request)
            self.res_text.setPlainText(response)
        except Exception as e:
            self.req_text.setPlainText(f"[ERROR] {e}")
            self.res_text.setPlainText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HttpTestApp()
    sys.exit(app.exec_())