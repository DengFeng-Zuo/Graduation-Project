from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
from Designer.initDB import * # 从initDB.py文件中导入UserDbManager类



class SignUpWidget(QWidget):
    student_signup_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setWindowTitle("欢迎注册股票价格预测系统")
        self.setUpUI()
        self.userdb = UserDbManager()

    def setUpUI(self):
        font = QFont()  # 固定字体变量
        font.setPixelSize(36)  # 字体设置为36pix
        lineEditFont = QFont()  # 输入框字体变量
        lineEditFont.setPixelSize(16)  # 输入框字体大小设置为16pix

        self.layout = QVBoxLayout()  # 定义纵向布局
        self.setLayout(self.layout)  # 设置整体得布局，将纵向布局设置为整体布局
        self.signUpLabel = QLabel("注   册")  # 注册标签
        self.signUpLabel.setAlignment(Qt.AlignCenter)  # 居中显示
        # self.signUpLabel.setFixedWidth(300)
        self.signUpLabel.setFixedHeight(100)  # 设置高度
        self.signUpLabel.setFont(font)  # 设置QLabel字体
        self.layout.addWidget(self.signUpLabel, Qt.AlignHCenter)  # 将控件放入到纵向布局中，居中显示

        # 表单，包括账号，姓名，密码，确认密码
        self.formlayout = QFormLayout()  # 账号，姓名，密码，确认密码按钮都放入QFormLayout布局中
        font.setPixelSize(18)

        # Row1
        self.studentIdLabel = QLabel("账    号:")  # 学号控件
        self.studentIdLabel.setFont(font)  # 设置字体
        self.studentIdLineEdit = QLineEdit()  # 输入框
        self.studentIdLineEdit.setFixedWidth(180)  # 设置输入框宽度
        self.studentIdLineEdit.setFixedHeight(32)  # 设置输入框高度
        self.studentIdLineEdit.setFont(lineEditFont)  # 设置输入框字体
        self.studentIdLineEdit.setMaxLength(10)  # 设置输入框最大长度限制
        self.formlayout.addRow(self.studentIdLabel, self.studentIdLineEdit)  # 将两个控件添加到QFormLayout布布点 。

        # Row2
        self.studentNameLabel = QLabel("姓    名:")
        self.studentNameLabel.setFont(font)
        self.studentNameLineEdit = QLineEdit()
        self.studentNameLineEdit.setFixedHeight(32)
        self.studentNameLineEdit.setFixedWidth(180)
        self.studentNameLineEdit.setFont(lineEditFont)
        self.studentNameLineEdit.setMaxLength(10)
        self.formlayout.addRow(self.studentNameLabel, self.studentNameLineEdit)

        lineEditFont.setPixelSize(10)

        # Row3
        self.passwordLabel = QLabel("密    码:")
        self.passwordLabel.setFont(font)
        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setFixedWidth(180)
        self.passwordLineEdit.setFixedHeight(32)
        self.passwordLineEdit.setFont(lineEditFont)
        # self.passwordLineEdit.setEchoMode(QLineEdit.Password)          #QLineEdit.Password输入字符后就立马显示为星号
        self.passwordLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)  # QLineEdit.PasswordEchoOnEdit为输入时为字符，失去焦点为星号
        self.passwordLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordLabel, self.passwordLineEdit)

        # Row4
        self.passwordConfirmLabel = QLabel("确认密码:")
        self.passwordConfirmLabel.setFont(font)
        self.passwordConfirmLineEdit = QLineEdit()
        self.passwordConfirmLineEdit.setFixedWidth(180)
        self.passwordConfirmLineEdit.setFixedHeight(32)
        self.passwordConfirmLineEdit.setFont(lineEditFont)
        # self.passwordConfirmLineEdit.setEchoMode(QLineEdit.Password)
        self.passwordConfirmLineEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.passwordConfirmLineEdit.setMaxLength(16)
        self.formlayout.addRow(self.passwordConfirmLabel, self.passwordConfirmLineEdit)

        # Row5
        self.signUpbutton = QPushButton("注 册")
        self.signUpbutton.setFixedWidth(120)
        self.signUpbutton.setFixedHeight(30)
        self.signUpbutton.setFont(font)
        self.formlayout.addRow("", self.signUpbutton)  # 第一个位置置空
        widget = QWidget()
        widget.setLayout(self.formlayout)  # 将formlayout 表格布局放入控件中
        widget.setFixedHeight(250)
        widget.setFixedWidth(300)  # 如果不显示，这个可写成320，或者把Label的文字宽度调小点
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(widget, Qt.AlignCenter)  # 将控件放入QHBoxLayout 横向布局中
        widget = QWidget()
        widget.setLayout(self.Hlayout)  # 将 QHBoxLayout 横向布局放入控件中
        self.layout.addWidget(widget, Qt.AlignHCenter)  # 将控件放入 整体的这个纵向布局中

        # 设置验证
        reg = QRegExp("PB[0~9]{8}")  # 设置输入匹配规则，PB开头，后面加8位数字
        pValidator = QRegExpValidator(self)
        pValidator.setRegExp(reg)
        self.studentIdLineEdit.setValidator(pValidator)  # 将匹配规则关联到输入框

        reg = QRegExp("[a-zA-z0-9]+$")  # 设置输入匹配规则,由数字和26个英文字母组成的字符串
        pValidator.setRegExp(reg)
        self.passwordLineEdit.setValidator(pValidator)
        self.passwordConfirmLineEdit.setValidator(pValidator)
        self.signUpbutton.clicked.connect(self.SignUp)
        self.studentIdLineEdit.returnPressed.connect(self.SignUp)
        self.studentNameLineEdit.returnPressed.connect(self.SignUp)
        self.passwordLineEdit.returnPressed.connect(self.SignUp)
        self.passwordConfirmLineEdit.returnPressed.connect(self.SignUp)

    def SignUp(self):
        userId = self.studentIdLineEdit.text()
        Name = self.studentNameLineEdit.text()
        password = self.passwordLineEdit.text()
        confirmPassword = self.passwordConfirmLineEdit.text()
        if (userId == "" or Name == "" or password == "" or confirmPassword == ""):
            print(QMessageBox.warning(self, "警告", "表单不可为空，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
            return
        else:  # 需要处理逻辑，1.账号已存在;2.密码不匹配;3.插入user表
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(dbpath)
            db.open()
            query = QSqlQuery()
            if (confirmPassword != password):  # 两次密码不匹配，直接返回
                print(QMessageBox.warning(self, "警告", "两次输入密码不一致，请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                return
            elif (confirmPassword == password):  # 两次密码一致
                # md5编码
                hl = hashlib.md5()  # 将密码进行md5加密
                hl.update(password.encode(encoding='utf-8'))
                md5password = hl.hexdigest()
                sql = "SELECT * FROM user WHERE userid='%s'" % (userId)
                query.exec_(sql)
                if (query.next()):
                    print(QMessageBox.warning(self, "警告", "该账号已存在,请重新输入", QMessageBox.Yes, QMessageBox.Yes))
                    return
                else:
                    sql = "INSERT INTO user VALUES ('%s','%s','%s','%s')" % (
                        userId, Name, md5password,0)
                    print(sql)
                    db.exec_(sql)
                    db.commit()
                    print(QMessageBox.information(self, "提醒", "您已成功注册账号!", QMessageBox.Yes, QMessageBox.Yes))
                    self.student_signup_signal.emit(userId)
                db.close()
                return

