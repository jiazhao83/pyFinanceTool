# encoding: UTF-8
#
# Project: pyFinanceTool
# Author: borlittle
# CreateDate: 2017/12/10
"""
  BriefIntroduction:
    
    
  Update:
    
    
  Reference:
    
  RunningEnvironment: python 3.5 and above  
"""

import ctypes
# import packages
import sys

import PyQt5.QtSql as sql
from ConfigFile import ConfigFileUseConfigParser
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox
from Ui_foundsCodeList import Ui_FoundsCodeListDialog

global contentList
contentList = []


class WorkThread(QThread):
    # 后台链接数据库并从数据库读取基金数据
    trigger = pyqtSignal()

    def __init__(self, config, parent):
        super(WorkThread, self).__init__(parent)

        self.configure = config
        self.selectCode = ""

    def run(self):

        try:
            ctypes.windll.LoadLibrary('K:/mysql-5.7.20-winx64/lib/libmysql.dll')

            if sql.QSqlDatabase.isDriverAvailable('QMYSQL'):
                db = sql.QSqlDatabase.addDatabase('QMYSQL')
                db.setHostName(self.configure['dataBase']['host'])
                # db.setPort(int(self.config.configParamsDit['dataBase']['port']))
                db.setUserName(self.configure['dataBase']['user'])
                db.setPassword(self.configure['dataBase']['password'])
                db.setDatabaseName('foundation_code_company')
                result = db.open()
                if result:
                    contentList.clear()
                    print('Open Mysql ok.')
                    query = sql.QSqlQuery('select 代码,名称 from code_list')
                    query.first()
                    for i in range(query.size()):
                        content = str(query.value(0)) + ':' + str(query.value(1))
                        contentList.append(content)
                        query.next()

                    db.close()
                else:
                    print(db.lastError().driverText())
                    print(db.lastError().databaseText())
                    print('Open Mysql failed.')
            else:
                print('Mysql driver is not ok')
        except Exception as e:
            print(e)

        self.trigger.emit()  # 循环完毕后发出信号


# class SelectFoundForAnalyse
class SelectFoundForAnalyse(QDialog, Ui_FoundsCodeListDialog):
    selectFish = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SelectFoundForAnalyse, self).__init__(parent)
        self.setupUi(self)
        self.config = ConfigFileUseConfigParser()
        self.config.readConfigParams()
        self.pushConfirmSelectedCodeButton.clicked.connect(self.confirmSelectedCode)
        self.getCodeListFromSql()

    def confirmSelectedCode(self):
        # 确认选择的基金编码
        list = self.foundCodeListWidget.currentItem().text()
        self.selectCode = list.split(':')[0]
        reply = QMessageBox.question(self, '确认', "已选择了一只基金：%s，是否确认选择" % list, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.selectFish.emit(self.selectCode)
        else:
            pass



    def getCodeListFromSql(self):

        self.thread = WorkThread(self.config.configParamsDit, self)
        self.thread.trigger.connect(self.refreshListWidget)
        self.thread.start()
        self.labelStatus.setText("正在加载数据，请稍等...")
        self.foundCodeListWidget.clear()

    def refreshListWidget(self):

        for each in contentList:
            print(each)
            self.foundCodeListWidget.addItem(each)
        self.labelStatus.setText("加载数据完成，请选择一只需要分析的基金并单击OK按钮...")


# just for unit test       
if __name__ == '__main__':
    # TODO
    app = QtWidgets.QApplication(sys.argv)
    ui = SelectFoundForAnalyse()
    ui.getCodeListFromSql()
    ui.show()

    sys.exit(app.exec_())
