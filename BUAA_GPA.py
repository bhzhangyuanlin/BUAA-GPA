from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QMainWindow, QHeaderView, QAbstractItemView
from PyQt5 import QtCore, QtGui
from ui import Ui_MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import sys
import ctypes
import numpy as np


class CalculateGPA(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(CalculateGPA, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("北航GPA计算")
        self.binding_slot()
        self.init_set_window_and_icon()
        self.model = QStandardItemModel(0, 3)
        self.init_table()

        self.subject_arr = []
        self.score_arr = []
        self.gpa_score_arr = []
        self.total_gpa = 0

    def binding_slot(self):
        self.pushButton.clicked.connect(self.add_score)
        self.pushButton_2.clicked.connect(self.add_grade)
        self.pushButton_3.clicked.connect(self.cal_gpa)
        self.pushButton_4.clicked.connect(self.clear_all)
        self.pushButton_5.clicked.connect(self.delete_rows)

    def init_set_window_and_icon(self):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./superman.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        screenGeometry = QApplication.desktop().screenGeometry()
        size = (int(screenGeometry.width()*0.5), int(screenGeometry.height()*0.6))
        self.resize(*size)
        self.move((screenGeometry.width() - size[0])//2, (screenGeometry.height()-size[1])//2)

    def init_table(self):
        self.model.setHorizontalHeaderLabels(['课程名字', '成绩', 'GPA'])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif (e.key() == Qt.Key_Return) or (e.key() == Qt.Key_Enter):
            self.cal_gpa()

    @staticmethod
    def show_warning(s):
        msg = QMessageBox()
        msg.setWindowTitle('错误')
        msg.setText(s)
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Retry)
        reply = msg.exec()
        if reply == QMessageBox.Ok:
            pass

    def add_score(self):
        subject = self.lineEdit.text()
        score = self.lineEdit_3.text().strip()
        try:
            score = eval(score)
        except:
            self.show_warning('成绩数据输入有误！')
            return
        # if not score.isdigit():
        #     self.show_warning('成绩数据输入有误！')
        # else:
        score = float(score)
        gpa_score = self.get_gpa(score)
        self.gpa_score_arr.append(gpa_score)
        self.add_to_table(subject, score, gpa_score)
        self.lineEdit.clear()
        self.lineEdit_3.clear()

    def add_grade(self):
        subject = self.lineEdit_2.text()
        grade = self.comboBox.currentText()
        gpa_score = self.covert_mark(grade)
        self.gpa_score_arr.append(gpa_score)
        self.add_to_table(subject, grade, gpa_score)
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)

    @staticmethod
    def get_gpa(score):
        if score < 60:
            gpa_score = 0
        else:
            gpa_score = 4 - 3 * (100 - score) ** 2 / 1600
        return gpa_score

    def cal_gpa(self):
        if len(self.gpa_score_arr) > 0:
            final_gpa = sum(self.gpa_score_arr)/len(self.gpa_score_arr)
        else:
            final_gpa = 0
        self.lineEdit_4.setText(str(round(final_gpa, 2)))

    @staticmethod
    def covert_mark(score):
        if score == "优秀":
            gpa_score = 4
        elif score == "良好":
            gpa_score = 3.5
        elif score == "中等":
            gpa_score = 2.8
        elif score == "及格":
            gpa_score = 1.7
        elif score == "不及格":
            gpa_score = 0
        else:
            return None
        return gpa_score

    def add_to_table(self, subject, score, gpa_score):
        item_0 = QStandardItem()
        item_0.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item_0.setText(subject)
        item_1 = QStandardItem()
        item_1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item_1.setText(str(score))
        item_2 = QStandardItem()
        item_2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item_2.setText(str(round(gpa_score, 3)))
        self.model.appendRow([item_0, item_1, item_2])
        self.lineEdit_4.clear()

    def delete_rows(self):
        msg = QMessageBox()
        msg.setWindowTitle('警告')
        msg.setIcon(QMessageBox.Warning)
        msg.setText('该操作将删除对应行')
        msg.setInformativeText('是否确定删除？')
        clear = msg.addButton('删除', QMessageBox.AcceptRole)
        cancel = msg.addButton('取消', QMessageBox.RejectRole)
        msg.setDefaultButton(cancel)
        reply = msg.exec()
        if reply == QMessageBox.AcceptRole:
            rows = []
            no_del_li = []
            flag = False  # 判断是否有不可以删除的内容
            input_text = self.lineEdit_5.text()
            tmp = input_text.strip()
            if not tmp:
                self.show_warning('输入的行号为空')
                return
            tmp = tmp.split(',')
            for i in tmp:
                i = i.strip()
                rows.extend(i.split('，'))
            for i in rows:
                i = i.strip()
                if i.isdigit():
                    row = int(i)
                    cur_row_num = self.model.rowCount()
                    if row > cur_row_num:
                        pass
                    else:
                        self.model.removeRow(row - 1)
                        self.gpa_score_arr.pop(row - 1)
                else:
                    flag = True
                    no_del_li.append(i)
            if flag:
                no_del_msg = ''
                for k in no_del_li:
                    no_del_msg += k
                QMessageBox.information(self, '提示', '你输入的行号为：\n' + input_text +
                                        '\n但是存在以下未能成功删除的“行号”！需核对！\n' + no_del_msg,
                                        QMessageBox.Ok, QMessageBox.Ok)
                self.lineEdit_5.clear()
                self.lineEdit_4.clear()
            else:
                QMessageBox.information(self, '提示', '已成功删除了输入的以下行号：\n' + input_text,
                                        QMessageBox.Ok, QMessageBox.Ok)
                self.lineEdit_5.clear()
                self.lineEdit_4.clear()
        else:
            pass

    def clear_all(self):
        msg = QMessageBox()
        msg.setWindowTitle('警告')
        msg.setIcon(QMessageBox.Warning)
        msg.setText('该操作将清空所有的信息')
        msg.setInformativeText('是否确定清空所有的信息？')
        clear = msg.addButton('清空', QMessageBox.AcceptRole)
        cancel = msg.addButton('取消', QMessageBox.RejectRole)
        msg.setDefaultButton(cancel)
        reply = msg.exec()
        if reply == QMessageBox.AcceptRole:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.lineEdit_5.clear()
            self.model.removeRows(0, len(self.gpa_score_arr))
            self.gpa_score_arr.clear()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cg = CalculateGPA()
    cg.show()
    sys.exit(app.exec_())