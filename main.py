from Designer.Login import *
from Designer.Register import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = SignInWidget()
    register_window = SignUpWidget()
    #点击注册按钮，打开注册界面窗口
    login_window.register.clicked.connect(lambda:{register_window.show()})
    login_window.show()

    sys.exit(app.exec_())

