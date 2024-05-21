import sqlite3
import hashlib


#设置数据库的路径
dbpath =r"E:\Graduation Project\Designer\db\StockPrediction.db"


createUserTableString = """
CREATE TABLE IF NOT EXISTS user(
    userid CHAR(10) PRIMARY KEY,
    Name VARCHAR(20),
    Password CHAR(32),
    IsAdmin BIT
)"""



"""
数据库类，实现数据库的基本操作，创建，删除，切换库
"""


class DbManager(object):
    def __init__(self, *args):
        self.db = sqlite3.connect(*args)
        self.cursor = self.db.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, types, value, traceback):
        self.db.commit()
        return False

    def __del__(self):
        self.db.commit()
        self.db.close()


    def createTable(self, tableString):
        self.cursor.execute(tableString)
        self.db.commit()

    def commitAndClose(self):
        self.db.commit()
        self.db.close()


"""
用户类，实现初始化数据，添加普通用户，添加管理员，查询用户信息，查询管理员，更新密码
"""


class UserDbManager(DbManager):
    def __init__(self, database=dbpath, *args):
        super().__init__(database, *args)
        self.initDb()

    def initDb(self):
        self.createTable(createUserTableString)

    def initDatabase(self):
        password = 'admin123'
        hl = hashlib.md5()  #
        hl.update(password.encode(encoding='utf-8'))
        md5password = hl.hexdigest()
        self.addAdminUser('admin', 'scott', md5password)

        password = 'user123'
        hl = hashlib.md5()  #
        hl.update(password.encode(encoding='utf-8'))
        md5password = hl.hexdigest()
        self.addUser('user000000', 'user000000', md5password)

    def addUser(self, userid, Name, Password, IsAdmin=0):
        """添加普通用户"""
        insertData = self.cursor.execute("""INSERT INTO user
                    (userid, Name, Password, IsAdmin) VALUES 
                    ('{0}', '{1}', '{2}','{3}')
                    """.format(userid, Name, Password, IsAdmin))
        self.db.commit()

    def addAdminUser(self, userid, Name, Password):
        """添加管理员用户"""
        self.addUser(userid, Name, Password, IsAdmin=1)

    def querybyUserid(self, userid):
        sql="SELECT * FROM user WHERE userid = '%s'" % (userid)
        fetchedData = self.cursor.execute(sql)
        byUserid = fetchedData.fetchall()  # 通过fetchall接受全部数据，是一个list,list的每个元素是tuple类型数据
        return byUserid

    def getAdmineUserInfo(self):
        """获取管理员用户"""
        fetchedData = self.cursor.execute("SELECT userid, Name FROM user WHERE IsAdmin = 1")
        adminUser = fetchedData.fetchall()  # 通过fetchall接受全部数据，是一个list,list的每个元素是tuple类型数据
        print(adminUser)
        return fetchedData

    def getUserinfo(self):
        """获取一般用户"""
        fetchedData = self.cursor.execute("SELECT userid, Name FROM user WHERE IsAdmin = 0")
        normalUser = fetchedData.fetchall()  # 通过fetchall接受全部数据，是一个list,list的每个元素是tuple类型数据
        print(normalUser)
        return fetchedData

    def updatePassword(self, password, userid):
        fetchedData = self.cursor.execute("UPDATE User SET Password = '%s' WHERE userid = %s" % (password, userid))
        self.db.commit()

