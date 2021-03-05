# pylint: disable=E0611
# pylint: disable=E1101
#pyi-makespec --onefile --icon=icon.ico --noconsole VEZRead.py
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,\
    QScrollArea,QSizePolicy, QTableWidgetItem,QSplitter, QFrame, QSizePolicy, QListView, QTableWidget, qApp, QAction,\
     QMessageBox,QFileDialog, QErrorMessage, QDoubleSpinBox, QSpacerItem, QLineEdit, QItemDelegate, QProgressBar,\
     QTabWidget
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QImage, QIcon, QTransform, QStandardItemModel,QStandardItem,\
     QDoubleValidator, QValidator, QCloseEvent, QColor
from PyQt5.QtCore import QPersistentModelIndex, Qt,  QSize, QModelIndex, QThread, pyqtSignal

import sys
import os

from calc_okgt import k_supports, k_conductors, main_calc





class TableTempalte(QTableWidget):
    def __init__(self,set_colums = [],parent=None):
        super().__init__(parent)
        self.closeEditorSignal = None
        self.children = None
        self.pairs = None
        self.previousItem = None
        self.rows = 0

        #self.itemEntered.connect(lambda x: print(x.text()))
        self.cellDoubleClicked[int,int].connect(self.setPreviousItem)

    def setPreviousItem(self,x,y):
        #print(self.item(x,y).text())
        self.previousItem = self.item(x,y)
        
    def setcloseEditorSignal(self,metod):
        self.closeEditorSignal = metod

    def closeEditor(self, editor, hint):
        if self.closeEditorSignal is not None:
            self.closeEditorSignal()

        #i = self.currentRow()
        #j = self.currentColumn()
        #item = self.currentItem().text()
        
        QTableWidget.closeEditor(self, editor, hint)


    def add_row(self):
        self.rows+=1
        ind = self.currentRow()+1 if self.currentRow() != -1 else self.rows-1
        self.insertRow(ind)
        self.setItem(ind,0, QTableWidgetItem("Test"+str(self.rows)))
        self.selectionModel().clearSelection()
        self.setCurrentCell(-1,-1)
        
        
    def remove_row(self):
        if self.rows>0:
            ind = self.currentRow() if self.currentRow() != -1 else self.rows-1
            self.rows-=1
            self.removeRow(ind)
            self.selectionModel().clearSelection()
            self.setCurrentCell(-1,-1)

    def setLinkToChildren(self,children,pairs):
        self.children = children
        self.pairs = pairs

    


class OkgtNodeTable(TableTempalte):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setColumnCount(1)
        self.setHorizontalHeaderLabels(["Название узла"])
        self.setColumnWidth(0,200)

        #self.setcloseEditorSignal(lambda:self.WriteTable(who_edited = "table"))
        #self.itemChanged(lambda:print("change2"))
        #self.cellClicked[int,int].connect(lambda x, y: print(x,y))
        #self.setItemDelegate(DownloadDelegate(self))

    


    


class MyWindow(QMainWindow):
    def __init__(self,parent=None):
        super(MyWindow,self).__init__(parent)

        try:
            self.path_home = os.path.expanduser("~\\Desktop\\")
        except Exception:
            self.path_home = ""

        desktop = QApplication.desktop()
        wd = desktop.width()
        hg = desktop.height()
        ww = 1000
        wh = 500
        if ww>wd: ww = int(0.7*wd)
        if wh>hg: wh = int(0.7*hg)
        x = (wd-ww)//2
        y = (hg-wh)//2
        self.setGeometry(x, y, ww, wh)

        topVBoxLayout = QVBoxLayout(self)
        mainTabWidget = QTabWidget()
        topVBoxLayout.addWidget(mainTabWidget) 
        central_widget = QWidget()
        central_widget.setLayout(topVBoxLayout)
        self.setCentralWidget(central_widget) 

        self.statusBar()
        menubar = self.menuBar()

        self.Okgt_Widget = QWidget()
        Vl_Tabs = QTabWidget()
        Ps_Widget = QWidget()
        Rpa_Tabs = QTabWidget()
        Rez_Tabs = QTabWidget()

        mainTabWidget.addTab(self.Okgt_Widget,"ОКГТ")
        mainTabWidget.addTab(Vl_Tabs,"ВЛ")
        mainTabWidget.addTab(Ps_Widget,"ПС")
        mainTabWidget.addTab(Rpa_Tabs,"РЗА")
        mainTabWidget.addTab(Rez_Tabs,"Результаты")


        self.okgt_tab_maker()

        exitAction = QAction( '&Выход', self) #QIcon('exit.png'),
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Выход и программы')
        exitAction.triggered.connect(lambda:self.closeEvent(QCloseEvent()))

        add_row = QAction( '&Добавить', self) #QIcon('exit.png'),
        add_row.setShortcut('Ctrl+W')
        add_row.setStatusTip('Добавить строку в таблицу')
        add_row.triggered.connect(self.Okgt_node_table.add_row)

        remove_row = QAction( '&Удалить', self) #QIcon('exit.png'),
        remove_row.setShortcut('Ctrl+E')
        remove_row.setStatusTip('Удалить строку из таблицу')
        remove_row.triggered.connect(self.Okgt_node_table.remove_row)


        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(add_row)
        fileMenu.addAction(remove_row)


        


    def okgt_tab_maker(self):
        self.Okgt_node_table = OkgtNodeTable()
        self.Okgt_sector_table = TableTempalte()
        self.Okgt_left_panel = QWidget()
        self.Okgt_left_panel.setMinimumWidth(300)
        
        okgt_spltV = QSplitter(Qt.Vertical)
        okgt_spltH = QSplitter(Qt.Horizontal)
        okgt_spltV.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        okgt_spltH.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        okgt_spltV.addWidget(self.Okgt_node_table)
        okgt_spltV.addWidget(self.Okgt_sector_table)
        okgt_spltV.setStretchFactor(1, 3) 

        
        okgt_spltH.addWidget(okgt_spltV)
        okgt_spltH.addWidget(self.Okgt_left_panel)
        okgt_spltH.setStretchFactor(10, 1)

        okgt_vbl = QVBoxLayout()
        okgt_vbl.addWidget(okgt_spltH)
        self.Okgt_Widget.setLayout(okgt_vbl)

        
       
        


        #self.TWGr.addTab(self.Tabs[self.vkl],self.nm_ivl[i]) # Добавляем закладку в QTabWidget
    def closeEvent(self, event):
        Message = QMessageBox(QMessageBox.Question,  'Выход из программы',
            "Вы дейстивлеьно хотите выйти?", parent=self)
        Message.addButton('Да', QMessageBox.YesRole)
        Message.addButton('Нет', QMessageBox.NoRole)
        #Message.addButton('Сохранить', QMessageBox.ActionRole)
        reply = Message.exec()
        if reply == 0:  
            qApp.quit()
        elif reply == 1:
            event.ignore()


if __name__=='__main__':
    app=QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())