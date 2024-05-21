import sys
from Designer.MainWindow import Ui_MainWindow
from Designer.Register import *
import main


Login_Key=False

class SignInWidget(QWidget):
    is_admin_signal = pyqtSignal(str)
    is_student_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(1000, 600)
        self.setWindowTitle("欢迎使用股票价格预测系统")
        self.setUpUI()
        self.userdb = UserDbManager()
    def setUpUI(self):
        self.Vlayout = QVBoxLayout(self)
        self.HlayoutTitle = QHBoxLayout()  # 标题
        self.HlayoutWidgetForm = QHBoxLayout()
        self.formlayout = QFormLayout()

        self.labelAccount = QLabel("帐  号：")
        labelFont = QFont()
        labelFont.setPixelSize(18)
        lineEditFont = QFont()
        lineEditFont.setPixelSize(16)
        self.labelAccount.setFont(labelFont)
        self.lineEditAccount = QLineEdit()
        self.lineEditAccount.setFixedHeight(32)
        self.lineEditAccount.setFixedWidth(180)
        self.lineEditAccount.setFont(lineEditFont)
        self.lineEditAccount.setMaxLength(10)

        self.formlayout.addRow(self.labelAccount, self.lineEditAccount)

        self.labelPassword = QLabel("密  码：")
        self.labelPassword.setFont(labelFont)
        self.lineEditPassword = QLineEdit()
        self.lineEditPassword.setFixedHeight(32)
        self.lineEditPassword.setFixedWidth(180)
        self.lineEditPassword.setMaxLength(16)

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.lineEditAccount.setValidator(pValidator)

        reg = QRegExp("[a-zA-z0-9]+$")
        pValidator.setRegExp(reg)
        self.lineEditPassword.setValidator(pValidator)

        passwordFont = QFont()
        passwordFont.setPixelSize(16)
        self.lineEditPassword.setFont(passwordFont)

        self.lineEditPassword.setEchoMode(QLineEdit.Password)  # 输入后就显示为星号
        self.lineEditPassword.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # 输入时为字符，失去焦点为星号
        self.formlayout.addRow(self.labelPassword, self.lineEditPassword)

        self.signIn = QPushButton("登 录")
        self.signIn.setFixedWidth(55)
        self.signIn.setFixedHeight(30)
        self.signIn.setFont(labelFont)

        self.signCancle = QPushButton("重 置")
        self.signCancle.setFixedWidth(55)
        self.signCancle.setFixedHeight(30)
        self.signCancle.setFont(labelFont)
        self.signCancle.setStyleSheet(
            'background-color: #505F69;border: 1px solid #32414B;color: #F0F0F0;border-radius: 4px;padding: 3px;outline: none;')

        self.register = QPushButton("注 册")
        self.register.setFixedWidth(55)
        self.register.setFixedHeight(30)
        self.register.setFont(labelFont)

        self.testlayout = QHBoxLayout()
        self.testlayout.addWidget(self.signIn)
        self.testlayout.addWidget(self.signCancle)
        self.testlayout.addWidget(self.register)
        self.testwidget = QWidget()
        self.testwidget.setLayout(self.testlayout)  # 包含登录，取消两个按钮
        self.formlayout.addRow('', self.testwidget)  # 把testwidget加入到formlayout
        # formlayout 两个label, 两个LineEdit，两个按钮

        self.labelTitle = QLabel("请登录或者注册您的账号")
        fontlabel = QFont()
        fontlabel.setPixelSize(30)
        self.labelTitle.setFixedWidth(390)
        # pixmap=QPixmap('index.jpg').scaled(self.labelTitle.width(), self.labelTitle.height())
        # self.labelTitle.setPixmap(pixmap)
        # self.labelTitle.setStyleSheet("QLabel{background-image:url(index.jpg)}")
        # self.labelTitle.setFixedHeight(80)                                            #不设置宽度了
        self.labelTitle.setFont(fontlabel)
        self.HlayoutTitle.addWidget(self.labelTitle, Qt.AlignCenter)  # 标题
        self.widgetTitle = QWidget()
        self.widgetTitle.setLayout(self.HlayoutTitle)  # 标题
        self.widgetForm = QWidget()
        self.widgetForm.setFixedWidth(300)
        self.widgetForm.setFixedHeight(150)
        self.widgetForm.setLayout(self.formlayout)
        self.widgetForm.setStyleSheet(".QWidget{border-image:url(./images/baise.png)}")  # 设置widgets背景色
        # widgetForm上存放6个控件

        self.HlayoutWidgetForm.addWidget(self.widgetForm, Qt.AlignCenter)
        self.widget = QWidget()
        self.widget.setLayout(self.HlayoutWidgetForm)

        # background-image，当背景图片宽度高度小于窗口的宽度高度时，则会加载多个背景图片
        # background-image，当背景图片的宽度高度大于窗口的宽度高度时，背景图片会平铺整个背景
        # self.widget1.setStyleSheet("QWidget{background-image:url(index.jpg);}")       #设置背景图片
        self.widget.setStyleSheet(".QWidget{border-image:url(./images/lasa.jpg)}")  # 加.号表示只对当前控件有效，否则对子控件也有效
        self.widgetTitle.setStyleSheet("color:green")  # 设置字体颜色
        # self.widgetTitle.setStyleSheet("color:red; background:yellow")                 #设置字体颜色和背景颜色
        self.Vlayout.addWidget(self.widgetTitle)  # Vlayout层包含两个Widget垂直布局
        self.Vlayout.addWidget(self.widget, Qt.AlignTop)
        # self.Vlayout.addWidget(self.widgetForm, Qt.AlignTop)

        self.signIn.clicked.connect(self.signInCheck)
        self.signCancle.clicked.connect(self.signInCancleReset)
        self.lineEditPassword.returnPressed.connect(self.signInCheck)
        self.lineEditAccount.returnPressed.connect(self.signInCheck)

    #重置按钮的槽函数
    def signInCancleReset(self):
        self.lineEditAccount.clear()
        self.lineEditPassword.clear()



    def signInCheck(self):
        studentId = self.lineEditAccount.text()
        password = self.lineEditPassword.text()
        if (studentId == "" or password == ""):
            print(QMessageBox.warning(self, "警告", "学号和密码不可为空!", QMessageBox.Yes, QMessageBox.Yes))
            return

        hl = hashlib.md5()  # md5加密对象
        hl.update(password.encode(encoding='utf-8'))  # 将密码更新为MD5加密对象
        #获取查询userid的值
        userdata = self.userdb.querybyUserid(studentId)
        if (not userdata):
            # QMessageBox.information()返回值是一个整形变量,是点击按钮所代表的值
            # QMessageBox.Yes       =   16384
            # QMessageBox.No        =   65536
            # QMessageBox.Close     =   2097152
            # QMessageBox.Abort     =   262144
            # QMessageBox.Help     =   16777216
            print(QMessageBox.information(self, "提示", "该账号不存在,请重新输入!", QMessageBox.Yes))
            self.signInCancleReset()
        else:
            # 将输入的密码经过MD5加密之后，重新跟数据库中的值对比
            if (studentId == userdata[0][0] and hl.hexdigest() == userdata[0][2]):
                # 如果是管理员， 再在数据库中，第三项代表是否是管理员，1为管理员，0不是
                if (userdata[0][3] == 1):
                    self.is_admin_signal.emit("studentId")
                    Ui_MainWindow.admin_signal = True
                    #管理员标识设为TRUE
                    print('admin login success')
                    QMessageBox.information(self, "提示", studentId + " 管理员登录成功", QMessageBox.Yes, QMessageBox.Yes)
                    # 打开主窗口界面
                    main_window = Ui_MainWindow()
                    main_window.show()
                    self.close()
                else:
                    self.is_student_signal.emit(studentId)
                    print(studentId + ' login success')
                    QMessageBox.information(self, "提示", studentId + "用户登录成功", QMessageBox.Yes, QMessageBox.Yes)
                    #打开主窗口界面
                    main_window = Ui_MainWindow()
                    main_window.show()
                    self.close()
            else:
                print(QMessageBox.information(self, "提示", "密码错误!", QMessageBox.Yes, QMessageBox.Yes))
        return

