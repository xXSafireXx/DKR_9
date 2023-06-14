from PyQt5 import QtWidgets
from DCR9 import Ui_MainWindow  # импорт нашего сгенерированного файла
import sys
import mysql.connector
y=""
class mywindow(QtWidgets.QMainWindow):
    global y
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.pushButton_add.clicked.connect(self.widget_Add)
        self.ui.pushButton_red.clicked.connect(self.widget_Red)
        self.ui.pushButton_undo_1.clicked.connect(self.widget_Undo_1)
        self.ui.pushButton_undo_2.clicked.connect(self.widget_Undo_2)
        self.ui.tableWidget.cellClicked.connect(self.info)
        self.ui.pushButton_save_1.clicked.connect(self.insert)
        self.ui.pushButton_del.clicked.connect(self.delete)
        self.ui.pushButton_Save_2.clicked.connect(self.redact)
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        cur.execute("SELECT * FROM kiborgs") 
        result = cur.fetchall()
        for row in result:
            rowPosition = self.ui.tableWidget.rowCount()                               # +++
            self.ui.tableWidget.insertRow(rowPosition)                                 
            self.ui.tableWidget.setItem(rowPosition,0,QtWidgets.QTableWidgetItem(row[1]))
        myconn.close()
    def redact(self):
      if self.ui.spinBox.text!='0' and self.ui.lineName_2.text!='' and self.ui.textInfo_2.toPlainText()!='':
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        x=str(int(self.ui.spinBox.text()))
        cur.execute("update kiborgs set kiborgs="+str(self.ui.lineName_2.text())+" where id="+x)
        cur.execute("update kiborgs set info="+str(self.ui.textInfo_2.toPlainText())+" where id="+x)
        myconn.commit()
        myconn.close()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.textInfo_2.clear()
        self.ui.lineName_2.clear()
      else:
           from PyQt5.QtWidgets import QMessageBox
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Critical)
           msg.setText("Error")
           msg.setInformativeText('Для удаления есть отдельная кнопка')
           msg.setWindowTitle("Error")
           msg.exec_()
    def info(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        x=str(int(self.ui.spinBox.text()))
        cur.execute("SELECT * FROM kiborgs where id="+x) 
        result = cur.fetchall()
        for row in result:
         self.ui.textInfo.setText(row[2])
        myconn.close()
    def delete(self):
        if self.ui.spinBox.text!='':
         myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
         cur=myconn.cursor()
         x=str(int(self.ui.spinBox.text()))
         cur.execute("delete FROM kiborgs where id="+str(x))
         self.ui.spinBox.setValue(0)
         self.ui.textInfo.clear()
         myconn.commit()
         myconn.close()
         self.ui.tableWidget.setRowCount(0)
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        cur.execute("SELECT * FROM kiborgs") 
        result = cur.fetchall()
        for row in result:
            rowPosition = self.ui.tableWidget.rowCount()                               # +++
            self.ui.tableWidget.insertRow(rowPosition)                                 
            self.ui.tableWidget.setItem(rowPosition,0,QtWidgets.QTableWidgetItem(row[1]))
        myconn.close()
    def widget_Add(self):
            self.ui.stackedWidget.setCurrentIndex(1)
    def widget_Undo_1(self):
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.textInfo_1.clear()
            self.ui.lineName_1.clear()
    def insert(self):
       if self.ui.lineName_1.text!='' and self.ui.textInfo_1.toPlainText()!='':
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        x=str(int(self.ui.spinBox.text()))
        cur.execute("INSERT INTO kiborgs (id,kiborgs,info) values "+str((int(self.ui.tableWidget.rowCount())+1,self.ui.lineName_1.text(),self.ui.textInfo_1.toPlainText())))
        myconn.commit()
        myconn.close()
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        cur.execute("SELECT * FROM kiborgs") 
        result = cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for row in result:
            rowPosition = self.ui.tableWidget.rowCount()                               # +++
            self.ui.tableWidget.insertRow(rowPosition)                                 
            self.ui.tableWidget.setItem(rowPosition,0,QtWidgets.QTableWidgetItem(row[1]))
        myconn.close()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.textInfo_1.clear()
        self.ui.lineName_1.clear()

       else:
           from PyQt5.QtWidgets import QMessageBox
           msg = QMessageBox()
           msg.setIcon(QMessageBox.Critical)
           msg.setText("Error")
           msg.setInformativeText('заполните оба поля')
           msg.setWindowTitle("Error")
           msg.exec_()
    def widget_Undo_2(self):
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.textInfo_2.clear()
            self.ui.lineName_2.clear()
    def widget_Red(self):
        global y
        myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "12345",database = "kiborgs") 
        cur = myconn.cursor()
        x=str(int(self.ui.spinBox.text()))
        cur.execute("SELECT * FROM kiborgs where id="+x) 
        result = cur.fetchall()
        for row in result:
         self.ui.textInfo_2.setText(row[2])
         self.ui.lineName_2.setText(row[1])
        myconn.close()
        self.ui.stackedWidget.setCurrentIndex(2)
app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())
